import numpy as np


class CalibrationFunction:
    r"""
    Calibration function base type. All calibration classes should inherit from this type.
    Calibration functions receive calibration parameters in the following order

    params :math:`= (p^+_0,\cdots, p^+_n, p^-_0,\cdots,p^-_n)`
    """
    def __init__(self, npar, link):
        self.npar = npar
        self.start_params = np.zeros(2 * self.npar)
        self.param_names  = [f"p{i}+" for i in range(npar)]
        self.param_names += [f"p{i}-" for i in range(npar)]
        self.link  = link


class PolynomialCalibration(CalibrationFunction):
    r"""
    PolynomialCalibration computes a calibration polynomial
    depending on the measured flavour

    :math:`\displaystyle\omega(\eta, d, \langle\eta\rangle, p_i^+, p_i^-)=\\\displaystyle l\left(\delta_{d,1}\left(\langle\eta\rangle+\sum_{i}p_i^+(l^{-1}(\eta)-\langle\eta\rangle)^i\right)+\delta_{d,-1}\left(\langle\eta\rangle+\sum_{i}p_i^-(l^{-1}(\eta)-\langle\eta\rangle)^i\right)\right)``

    :param npar: Number of parameters per flavour (npar = polynomial degree + 1)
    :type npar: int
    :param link: link function :math:`l`
    :type link: link_function
    """
    def __init__(self, npar, link):
        CalibrationFunction.__init__(self, npar, link)

        # Set p1 parameters to 1
        self.start_params[1] = 1
        self.start_params[self.npar + 1] = 1

    def eval(self, params, eta, dec, avg_eta):
        r"""
        Compute the calibrated mistag given the calibration parameters params,
        the raw mistag eta, the tagging decision dec and the average raw mistag avg_eta

        :param params: parameter list
        :type params: list
        :param eta: mistags
        :type eta: list
        :param dec: tagging decision
        :type dec: list
        :param avg_eta: Mean mistag
        :type avg_eta: float

        :return: calibrated mistag :math:`\omega`
        :rtype: list
        """
        omega            = np.zeros(len(eta))
        omega[dec ==  1] = avg_eta + np.polyval(params[:self.npar][::-1], self.link.InvL(eta[dec ==  1]) - avg_eta)
        omega[dec == -1] = avg_eta + np.polyval(params[self.npar:][::-1], self.link.InvL(eta[dec == -1]) - avg_eta)
        return self.link.L(omega)

    def eval_plotting(self, params, eta, dec, avg_eta):
        r"""
        Returns a single curve for both flavours by weighting it depending on how many events have been
        tagged for each flavour. Only used for plotting purposes
        :math:`\displaystyle\omega^\mathrm{plot}(\eta, d, \langle\eta\rangle, p_i^+, p_i^-)=\\\displaystyle f^+l\left(\langle\eta\rangle+\sum_{i}p_i^+(l^{-1}(\eta)-\langle\eta\rangle)^i\right)+f^-l\left(\langle\eta\rangle+\sum_{i}p_i^-(l^{-1}(\eta)-\langle\eta\rangle)^i\right)`

        whereby :math:`f^+=N_{d=1}/N, f^-=N_{d=-1}/N`

        :param params: parameter list
        :type params: list
        :param eta: mistags
        :type eta: list
        :param dec: tagging decision
        :type dec: list
        :param avg_eta: Mean mistag
        :type avg_eta: float

        :return: calibrated mistag :math:`omega`
        :rtype: list
        """
        n_pos = np.sum(dec ==  1)
        n_neg = np.sum(dec == -1)
        f = n_pos / (n_pos + n_neg)

        omega  =       f * self.link.L(avg_eta + np.polyval(params[:self.npar][::-1], self.link.InvL(eta) - avg_eta))
        omega += (1 - f) * self.link.L(avg_eta + np.polyval(params[self.npar:][::-1], self.link.InvL(eta) - avg_eta))

        return omega

    def derivative(self, partial, params, eta, dec, avg_eta):
        r""" Computes the partial derivative wrt. a calibration parameter :math:`p_m^\pm`

            :math:`\displaystyle\frac{\partial\omega}{\partial p_m^\pm}(\eta_i, d_i)=l'(\omega(\eta_i, d_i))(l^{-1}(\eta_i)-\langle\eta\rangle)^m\delta_{d=\pm 1}`

            :param partial: partial derivative index, see base type constructor
            :type params: int
            :param params: parameter list
            :type params: list
            :param eta: mistags
            :type eta: list
            :param dec: tagging decision
            :type dec: list
            :param avg_eta: Mean mistag
            :type avg_eta: float

            :return: Partial calibration function derivative of given data
            :rtype: list
        """
        D = self.link.DL(self.eval(params, eta, dec, avg_eta))
        if partial < self.npar:
            D[dec ==  1] *= (self.link.InvL(eta[dec == 1]) - avg_eta) ** partial
            D[dec == -1] = 0
        else:
            D[dec == -1] *= (self.link.InvL(eta[dec == -1]) - avg_eta) ** (partial - self.npar)
            D[dec ==  1] = 0

        return D

    def gradient(self, params, eta, dec, avg_eta):
        """ Computes the gradient of the calibration wrt. to the calibration parameters """
        return np.array([self.derivative(i, params, eta, dec, avg_eta) for i in range(self.npar * 2)])


def res_gaussian(t, s):
    """ Generates resolution model based on decay time uncertainty s.
        Used in colvolutions """
    return np.exp(-0.5 * (t / s)**2) / (np.sqrt(2 * np.pi) * s)


def mixing_asymmetry(t, DM, DG, a=0):
    r"""
    Computes the mixing asymmetry given an oscillation frequency
    and a delta gamma value

    :param DM: :math:`\Delta m`
    :param DG: :math:`\Delta\Gamma`
    :param a: :math:`1-|q/p|^2`
    :type DM: float
    :type DG: float
    :type a: float
    """
    Amix = np.cos(DM * t) / np.cosh(0.5 * DG * t)
    if a != 0:
        Amix += a / 2 * (1 - Amix**2)
    return Amix
