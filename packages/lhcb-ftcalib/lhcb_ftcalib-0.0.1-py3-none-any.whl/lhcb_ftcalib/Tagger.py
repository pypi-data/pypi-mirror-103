import numpy as np
import iminuit
import pandas as pd
from packaging import version
from copy import deepcopy

from lhcb_ftcalib.printing import raise_warning, raise_error, warning, info, printbold
from lhcb_ftcalib.calibration_functions import PolynomialCalibration, mixing_asymmetry
from lhcb_ftcalib.TaggingData import TaggingData
from lhcb_ftcalib.performance import p_conversion_matrix
import lhcb_ftcalib.link_functions as link_functions


class Tagger:
    """LHCb Tagger object

    :param name: Custom name of the tagger
    :type name: str
    :param eta_data: All uncalibrated mistags
    :type eta_data: list
    :param dec_data: All uncalibrated tagging decisions
    :type dec_data: list
    :param B_ID: B meson ids
    :type B_ID: list
    :param calibrationMode: Which mode to use for calibration ("Bd", "Bu", "Bs")
    :type calibrationMode: str
    :param tau_ps: Decay time in picoseconds
    :type tau_ps: list
    :param tauerr_ps: Decay time uncertainty in picoseconds
    :type tauerr_ps: list
    :param weight: Event weight
    :type weight: list
    :param analytic_gradient: Whether to use the analytical gradient implementation
    :type analytic_gradient: bool

    :raises ValueError: if input data lists are not of the same length
    :raises ValueError: if decay time data is not given and calibration mode is Bd or Bs
    """
    def __init__(self, name, eta_data, dec_data, B_ID, calibrationMode, tau_ps=None, tauerr_ps=None, weight=None, selection=None, analytic_gradient=False):
        # Consistency checks
        raise_error(len(eta_data) == len(dec_data) == len(B_ID), "Tagging data must have matching dimensions")
        raise_error(calibrationMode in ("Bu", "Bd", "Bs"), "Unknown calibration mode")

        if selection is None:
            selection = pd.Series(np.full(len(dec_data), True))

        # Variables needed for minimization
        self.name      = name                                                                    #: Name of tagger
        self.mode      = calibrationMode                                                         #: Calibration mode
        self.B_absid   = {"Bu" : 521, "Bd" : 511, "Bs" : 531}[self.mode]                         #: MC particle id
        self.minimizer = None                                                                    #: iminuit minimizer
        self.func      = PolynomialCalibration(npar=2, link=link_functions.mistag)               #: Calibration function
        self.stats     = TaggingData(eta_data  = eta_data,
                                     dec_data  = dec_data,
                                     ID        = B_ID,
                                     weights   = weight,
                                     absid     = self.B_absid,
                                     selection = selection,
                                     ignore_eta_out_of_range = False)  #: Tagger statistics
        self.cstats    = None  #: Calibrated Tagger statistics (Null before calibration)
        self.analytic_gradient = analytic_gradient
        self._calibrated = False

        if self.mode == "Bd":
            self.tau        = pd.Series(tau_ps)[self.stats.tagged]  #: decay time in picoseconds
            self.tauerr     = pd.Series(tauerr_ps)[self.stats.tagged] if tauerr_ps is not None else None  #: decay time uncertainty in picoseconds
            self.DeltaM     = 0.5065  #: B oscillation frequency :math:`\Delta m`
            self.DeltaGamma = 0  #: Decay width difference of B mass eigenstates :math:`\Delta\Gamma`
            self.Aprod      = 0  #: Production asymmetry (WIP)
        elif self.mode == "Bs":
            self.tau        = pd.Series(tau_ps)[self.stats.tagged]
            self.tauerr     = pd.Series(tauerr_ps)[self.stats.tagged] if tauerr_ps is not None else None
            self.DeltaM     = 17.757
            self.DeltaGamma = 0
            self.Aprod      = 0
        elif self.mode == "Bu":
            self.tau        = None
            self.tauerr     = None
            self.DeltaM     = None
            self.DeltaGamma = None
            self.Aprod      = 0

        if self.mode in ("Bd", "Bs"):
            raise_error(self.tau is not None, "Decay time needed for calibration")
            raise_error(len(self.tau) == self.stats.Nt, "Tagging data must have matching dimensions")
            if self.tauerr is not None:
                raise_error(len(self.tauerr) == self.stats.Nt, "Tagging data must have matching dimensions")

        self.__init_oscillation_dilution()

        self.__init_minimizer()

    def __init_minimizer(self):
        """ Initializes the flavour tagging likelihood and the minimizer """
        self.minimizer = iminuit.Minuit(self.__nll if self.mode == "Bu" else self.__nll_oscil,
                                        tuple(self.func.start_params),
                                        name      = self.func.param_names,
                                        grad      = self.__nll_oscil_grad if self.analytic_gradient else None)
        self.minimizer.errordef = iminuit.Minuit.LIKELIHOOD
        self.minimizer.print_level = 2
        self.minimizer.strategy = 0

    def __init_oscillation_dilution(self):
        """ Computes flavour impurity for each measurement
            Needed for production flavour estimate
        """
        if self.mode == "Bu":
            self.osc_dilution = np.zeros(self.stats.Nts)
            Amix = None
        elif self.tauerr is not None:
            if self.DeltaGamma == 0:
                # Analytical solution exists
                Amix = mixing_asymmetry(self.tau[self.stats.selected], self.DeltaM, self.DeltaGamma)
                self.osc_dilution = 0.5 * (1 - np.exp(-self.DeltaM**2 * self.tauerr[self.stats.selected]**2) * np.abs(Amix))
            else:  # FFT
                # Assume that time resolution model is in bounds [-0.3, 0.3] ps and decaytime is in [-20, 20] ps to minimize FFT boundary effects
                raise NotImplementedError("FFT WIP")
                # res_range = np.linspace(-0.3, 0.3, 300)
                # Amix_lin = mixing_asymmetry(np.linspace(-20, 20, 300), self.DeltaM, self.DeltaGamma)
                # Amix = [fftconvolve(Amix, res_gaussian(res_range, err), mode="same")[tau] for tau, err in zip(self.tau, self.tauerr)]
        else:
            Amix = mixing_asymmetry(self.tau[self.stats.selected], self.DeltaM, self.DeltaGamma)
            self.osc_dilution = 0.5 * (1.0 - np.abs(Amix))

        # Update production asymmetry given mixing asymmetry
        if self.mode != "Bu":
            self.stats.prod_flav = self.stats.dec_flav.copy()
            self.stats.prod_flav[np.sign(Amix) == -1] *= -1

            self.stats.correct_tags = self.stats.dec == self.stats.prod_flav
            self.stats.wrong_tags   = ~self.stats.correct_tags

    def set_calibration(self, func):
        """ Override default calibration function

            :param func: Calibration function
            :type func: CalibrationFunction
        """
        self.func = deepcopy(func)
        self.__init_minimizer()

    def calibrate(self, ignore_eta_out_of_range=False):
        """ Run flavour tagging calibration and adds calibrated mistag information to TaggingData

            :param ignore_eta_out_of_range: Whether to ignore out of range values of the calibrated mistag (NOT recommended)
            :type ignore_eta_out_of_range: bool
        """
        iminuit_version = iminuit.version.iminuit_version
        printbold(20 * "-" + f" {self.name} calibration " + 20 * "-")
        info("iminuit version", iminuit_version, f"({iminuit.__version__})")
        assert version.parse(iminuit_version) >= version.parse("2.3.0"), "iminuit >= 2.3.0 required"

        info("Starting minimization for", self.name)
        info(f"Selection keeps {self.stats.Ns}({self.stats.Nws} weighted) out of {self.stats.N}({self.stats.Nw}) events ({100*np.round(self.stats.Ns/self.stats.N, 4)}%)")
        self.minimizer.migrad()
        self.minimizer.hesse()
        if self.minimizer.valid:
            info("Minimum found")
            if self.minimizer.accurate:
                info("Covariance matrix accurate")
            else:
                warning("Covariance matrix -NOT- accurate")
        else:
            raise_error(False, "Minimization did not converge")

        self.params_nominal = [self.minimizer.values[n] for n in self.func.param_names]
        self.params_uncerts = [self.minimizer.errors[n] for n in self.func.param_names]

        # Initializing calibrated tagger statistics
        omega = 0.5 * np.ones(self.stats.N)
        omega[self.stats.tagged] = self.func.eval(self.params_nominal, eta=self.stats.all_eta[self.stats.tagged], dec=self.stats.all_dec[self.stats.tagged], avg_eta=self.stats.avg_eta)
        self.cstats = TaggingData(eta_data  = omega,
                                  dec_data  = self.stats.all_dec,
                                  ID        = self.stats.all_B_ID.copy(),
                                  weights   = self.stats.all_weights.copy(),
                                  absid     = self.B_absid,
                                  selection = self.stats.selected.copy())
        raise_warning(self.cstats.noverflow == 0, f"{self.name}: {self.cstats.noverflow} events have ω > 0.5 after calibration")
        raise_warning(np.sum(self.cstats.underflow) == 0, f"{self.name}: {np.sum(self.cstats.underflow)} events have ω < 0 after calibration")

        self._calibrated = True
        print()

    def is_calibrated(self):
        """ Returns true if calibration was performed

            :return type: bool
        """
        return self._calibrated

    def get_fitparameters(self, style="delta", p1minus1=False, tex=False, greekdelta=False):
        """ Returns arrays of parameter names, nominal values
            and uncertainties and covariance matrix

            :param style: Which parameter convention to use
            :type style: str ("delta", "flavour")
            :param p1minus1: Whether to subtract 1 from p1
            :type p1minus1: bool
            :param tex: Whether to format parameter names as tex
            :type tex: bool
            :param greekdelta: Whether to use "D" or "Δ" (only if tex=False)
            :type greekdelta: bool

            :return: Tuple (parameters, nominal_values, unvertainties, covariance matrix)
            :return type: tuple
        """
        if not self._calibrated:
            return None

        noms    = self.params_nominal.copy()
        uncerts = self.params_uncerts.copy()
        params  = self.func.param_names.copy()
        cov     = self.minimizer.covariance.copy()
        npar    = self.func.npar

        if style == "delta":
            conv_mat = p_conversion_matrix(npar)
            params = [p.replace("+", "").replace("-", "") for p in params]
            for i, p in enumerate(params[npar:]):
                params[i + npar] = "D" + p

            # Transform uncertainties
            noms  = conv_mat @ noms
            cov = conv_mat @ np.array(cov.tolist()) @ conv_mat.T
            uncerts = np.sqrt(np.diag(cov))

            if not p1minus1:
                if len(noms) >= 4:
                    noms[1] += 1
        elif style == "flavour":
            if p1minus1:
                if len(noms) >= 4:
                    noms[1] -= 1
                    noms[npar + 1] -= 1

        if tex:
            params = [p.replace("p", "p_").replace("+", "^+").replace("-", "^-") for p in params]
            params = [p.replace("D", r"\Delta ") for p in params]
        else:
            if greekdelta:
                params = [p.replace("D", "Δ") for p in params]

        return params, noms, uncerts, cov

    def __nll(self, params):
        """ Likelihood for B+ modes without oscillation """
        omega = self.func.eval(params, self.stats.eta, self.stats.dec, self.stats.avg_eta)

        log_likelihood  = np.sum(np.log(np.maximum((1 - omega[self.stats.correct_tags]) * self.stats.weights[self.stats.correct_tags], 1e-5)))  # Correct tags
        log_likelihood += np.sum(np.log(np.maximum(     omega[self.stats.wrong_tags]    * self.stats.weights[self.stats.wrong_tags], 1e-5)))  # Incorrect tags

        return -log_likelihood

    def __nll_oscil(self, params):
        """ Likelihood for Bd and Bs modes with oscillation """
        omega_given = self.func.eval(params, self.stats.eta,  self.stats.dec, self.stats.avg_eta)  # Omega based on measured dec
        omega_oscil = self.func.eval(params, self.stats.eta, -self.stats.dec, self.stats.avg_eta)  # Omega for opposite prod flavour
        correct_tags = self.stats.correct_tags
        wrong_tags   = self.stats.wrong_tags

        correct_terms  = (1.0 - self.osc_dilution[correct_tags]) * (1.0 - omega_given[correct_tags])  # No mixing (tag == prod flav == decay flav)
        correct_terms +=        self.osc_dilution[correct_tags]  * omega_oscil[correct_tags]          # mixing    (tag == prod flav != decay flav)

        wrong_terms    = (1.0 - self.osc_dilution[wrong_tags]) * omega_given[wrong_tags]          # No mixing (tag != prod flav == decay flav)
        wrong_terms   +=        self.osc_dilution[wrong_tags]  * (1.0 - omega_oscil[wrong_tags])  # mixing    (tag != prod flav != decay flav)

        log_likelihood  = np.sum(np.log(np.maximum(correct_terms * self.stats.weights[correct_tags], 1e-5)))
        log_likelihood += np.sum(np.log(np.maximum(wrong_terms   * self.stats.weights[wrong_tags], 1e-5)))

        return -log_likelihood

    def __nll_oscil_grad(self, params):
        """ Likelihood gradient """
        omega_given = self.func.eval(params, self.stats.eta,      self.stats.dec, self.stats.avg_eta)
        omega_oscil = self.func.eval(params, self.stats.eta, -1 * self.stats.dec, self.stats.avg_eta)
        correct_tags = self.stats.correct_tags
        wrong_tags   = self.stats.wrong_tags

        osc_dilution_correct = self.osc_dilution[correct_tags]
        osc_dilution_wrong   = self.osc_dilution[wrong_tags]

        denom_correct  = (1.0 - osc_dilution_correct) * (1.0 - omega_given[correct_tags])
        denom_correct +=        osc_dilution_correct  *        omega_oscil[correct_tags]
        denom_wrong    = (1.0 - osc_dilution_wrong)   *        omega_given[wrong_tags]
        denom_wrong   +=        osc_dilution_wrong    * (1.0 - omega_oscil[wrong_tags])

        grad = np.zeros(self.func.npar * 2)

        for i in range(self.func.npar * 2):
            correct_terms  =      osc_dilution_correct  * self.func.derivative(i, params, self.stats.eta[correct_tags], -1 * self.stats.dec[correct_tags], self.stats.avg_eta)
            correct_terms -= (1 - osc_dilution_correct) * self.func.derivative(i, params, self.stats.eta[correct_tags],      self.stats.dec[correct_tags], self.stats.avg_eta)

            wrong_terms  = (1 - osc_dilution_wrong) * self.func.derivative(i, params, self.stats.eta[wrong_tags],      self.stats.dec[wrong_tags], self.stats.avg_eta)
            wrong_terms -=      osc_dilution_wrong  * self.func.derivative(i, params, self.stats.eta[wrong_tags], -1 * self.stats.dec[wrong_tags], self.stats.avg_eta)

            grad[i] = np.sum(correct_terms / denom_correct) + np.sum(wrong_terms / denom_wrong)

        return -grad
