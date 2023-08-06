import json
import pandas as pd
import numpy as np

from lhcb_ftcalib.calibration_functions import PolynomialCalibration
from lhcb_ftcalib.TaggingData import BasicTaggingData
from lhcb_ftcalib.printing import info
import lhcb_ftcalib.link_functions as links
from lhcb_ftcalib.plotting import draw_inputcalibration_curve


class TargetTaggerCollection:
    r""" class TaggerCollection List type for grouping target taggers. Supports iteration.

        :param \*taggers: Tagger instance
        :type \*taggers: Tagger
    """
    def __init__(self, *taggers):
        self._taggers = [*taggers]
        self._index = -1
        if self._taggers:
            self._validate()

    def __str__(self):
        return "TagCollection [" + ','.join([t.name for t in self._taggers]) + "]"

    def __len__(self):
        return len(self._taggers)

    def __iter__(self):
        return self

    def __next__(self):
        if self._index == len(self._taggers) - 1:
            self._index = -1
            raise StopIteration
        self._index += 1
        return self._taggers[self._index]

    def __getitem__(self, t):
        return self._taggers[t]

    def _validate(self):
        assert all([isinstance(tagger, TargetTagger) for tagger in self]), "TaggerCollection can only story TargetTagger instances"
        assert len(set([tagger.name for tagger in self])) == len(self._taggers), "Tagger names are not unique"

    def create_tagger(self, *args, **kwargs):
        """ Adds a TargetTagger instance to the TargetTaggerCollection instance
            by passing the arguments to the TargetTagger() constructor.
        """
        self._taggers.append(TargetTagger(*args, **kwargs))
        self._validate()

    def load_calibrations(self, filename, tagger_mapping=None):
        """ Load calibrations from a file

            :param filename: Filename of the calibration file
            :type filename: str
            :param tagger_mapping: Optional dictionary of a mapping of tagger names in this list vs corresponding entry names in the calibration file. By default, the same naming is assumed (!)
            :type tagger_mapping: dict
        """
        if tagger_mapping is None:
            tagger_mapping = { t.name : t.name for t in self }
        else:
            assert len(tagger_mapping) == len(self)

        for tagger in self:
            info(f"Loading {tagger_mapping[tagger.name]} calibrations for {tagger.name}")
            tagger.load(filename, tagger_mapping[tagger.name])

    def apply(self, ignore_eta_out_of_range=False):
        """ Applies the previously loaded calibrations to a taggers

            :param ignore_eta_out_of_range: Whether to ignore mistag overflows
            :type ignore_eta_out_of_range: bool
        """
        for tagger in self:
            info(f"Applying calibration for {tagger.name}")
            tagger.apply(ignore_eta_out_of_range)

    def get_calibrated_dataframe(self):
        """ Returns a dataframe of the calibrated mistags and tagging decisions

            :return: Calibrated data
            :return type: pandas.DataFrame
        """
        calibrated = pd.DataFrame()
        for tagger in self:
            calibrated[tagger.dec_column] = tagger.cstats.all_dec.copy()
            calibrated[tagger.eta_column] = tagger.cstats.all_eta.copy()

        return calibrated

    def plot_inputcalibration_curves(self, **kwargs):
        """ Plots input calibration curves of a set of taggers, like the EPM
            does when a calibration is applied.  Plots the loaded calbration curve
            (uncertainties are loaded but ignored while applying the calibration)
            and the targeted mistag data.

            :param \**kwargs: Arguments to pass to draw_inputcalibration_curve
        """
        for tagger in self:
            print("Info: pdf file", draw_inputcalibration_curve(tagger, **kwargs), "has been created")


class TargetTagger:
    """ A variation of the tagger object which loads a calibration
        from file and applies it to some data. Like the "Tagger", 
        it contains two sets of TaggingData (BasicTaggingData) for
        before and after the calibration.

        :param name: Name of this target tagger. Ideally, try to use the same as for the calibrated tagger
        :type name: str
        :param eta: Targeted mistag data
        :type eta: list
        :param dec: Targeted tagging decisions
        :type dec: list
        :param weights: Weight variable (needed for tagging statistics information)
        :type weights: list
    """
    class __MinimizerView:
        def __init__(self):
            self.covariance = None

    def __init__(self, name, eta, dec, weight):
        self.name    = name
        self.stats   = BasicTaggingData(eta, dec, weight)
        self.cstats  = None
        self.info    = None
        self.func    = None
        self._calibrated = False
        self.minimizer = self.__MinimizerView()

        if isinstance(eta, pd.Series):
            self.eta_column = eta.name
        else:
            self.eta_column = self.name + "_OMEGA"
        if isinstance(dec, pd.Series):
            self.dec_column = dec.name
        else:
            self.dec_column = self.name + "_CDEC"

        self.dec_column = self.dec_column.replace("_DEC", "_CDEC")
        self.eta_column = self.eta_column.replace("_ETA", "_OMEGA")

    def apply(self, ignore_eta_out_of_range=False):
        """ Apply the previously loaded calibration to this tagger

            :param ignore_eta_out_of_range: Whether to ignore mistag overflows
            :type ignore_eta_out_of_range: bool
        """
        assert self._calibrated
        omega = 0.5 * np.ones(self.stats.N)

        omega[self.stats.tagged] = self.func.eval(self.params_nominal, self.stats.eta, self.stats.dec, self.stats.avg_eta)
        self.cstats = BasicTaggingData(omega, self.stats.all_dec, self.stats.all_weights.copy(), ignore_eta_out_of_range)
        self._calibrated = True

    def is_calibrated(self):
        """ Returns true if a calibration has been loaded

            :return type: bool
        """
        return self._calibrated

    def load(self, filename, tagger_name):
        """ Load a calibration entry from a calibration file

            :param filename: Filename of the calibration file
            :type filename: str
            :param tagger_name: Entry name of the calibration data you would like to load
            :type filename: str
        """
        with open(filename, "r") as F:
            calib = json.loads(F.read())

        # Reconstruct calibration function
        assert tagger_name in calib, "Tagger " + tagger_name + " not contained in calibration file"
        self.info = calib[tagger_name]

        if "PolynomialCalibration" in self.info:
            fun_info = self.info["PolynomialCalibration"]
            self.func = PolynomialCalibration(int(fun_info["degree"]) + 1, self.__get_link_by_name(fun_info["link"]))
            self.params_nominal = np.array([float(self.info["calibration"]["flavour_style"]["params"][p]) for p in self.func.param_names])
            self.params_uncerts = np.array([float(self.info["calibration"]["flavour_style"]["uncert"][p]) for p in self.func.param_names])
            self.stats.avg_eta  = float(self.info["calibration"]["avg_eta"])  # Always use avg_eta from calibrations
            cov = self.info["calibration"]["flavour_style"]["cov"]
            self.minimizer.covariance = np.array([float(e) for row in cov for e in row]).reshape((2 * self.func.npar, 2 * self.func.npar))
        else:
            raise NotImplementedError

    def __get_link_by_name(self, link):
        return {
            "mistag"   : links.mistag,
            "logit"    : links.logit,
            "rlogit"   : links.rlogit,
            "probit"   : links.probit,
            "rprobit"  : links.rprobit,
            "cauchit"  : links.cauchit,
            "rcauchit" : links.rcauchit,
        }[link]


def apply_tagger(tagger, eta, dec, ignore_eta_out_of_range=False):
    """ Apply calibration of this tagger to some data

    :param tagger: Tagger object
    :type tagger: Tagger
    :param eta: mistag data
    :type eta: list
    :param dec: tag decision data
    :type dec: list
    :param ignore_eta_out_of_range: Whether to ignore calibrated mistag values < 0 or > 0.5
    :type ignore_eta_out_of_range: bool
    :return: (calibrated mistag, calibrated tag decisions, over/underflow flags)
    :return type: tuple
    """
    assert tagger.calibrated, "tagger.run_calibration() needs to run before calibration can be applied"

    omega = tagger.func.eval(tagger.params_nominal, eta, dec, tagger.avg_eta)
    cdec  = dec.copy(deep=True)
    if not ignore_eta_out_of_range:
        overflow = omega > 0.5
        underflow = omega < 0
        omega[overflow] = 0.5
        omega[underflow] = 0

        cdec[overflow] = 0

    return omega, cdec, overflow | underflow
