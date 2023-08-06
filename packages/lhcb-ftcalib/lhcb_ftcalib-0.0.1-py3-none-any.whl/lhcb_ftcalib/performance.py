import numpy as np
import pandas as pd
from uncertainties import ufloat


def p_conversion_matrix(npar):
    r""" Returns matrix :math:`C` that converts internal representation of
        parameters into the traditional form
        :math:`C\cdot (p^+_0,\cdots, p^+_n, p^-_0,\cdots,p^-_n) = (p_0,\cdots, p_n, \Delta p_0,\cdots,\Delta p_n)`

        :param npar: number of calibration parameters per flavour
        :type npar: int
        :return: parameter transformation
        :rtype: numpy.ndarray
    """
    upper = np.concatenate([0.5 * np.eye(npar), 0.5 * np.eye(npar)]).T
    lower = np.concatenate([np.eye(npar), -np.eye(npar)]).T
    return np.concatenate([upper, lower])


def tagging_rate(stats, selected=True):
    r""" Returns the tagging efficiency :math:`\epsilon_{\mathrm{tag}}=N_t/N`

        :param stats: Tagger stats
        :type stats: TaggingData
        :return: Tagging efficiency
        :rtype: ufloat
    """
    if selected:
        rate = stats.Nwts / stats.Nws
        untagged = stats.Nws - stats.Nwts
        return ufloat(rate, np.sqrt(stats.Nwts * untagged / stats.Neffs) / stats.Nws)
    else:
        rate = stats.Nwt / stats.Nw
        untagged = stats.Nw - stats.Nwt
        return ufloat(rate, np.sqrt(stats.Nwt * untagged / stats.Neff) / stats.Nw)


def raw_mistag_rate(stats, selected=True):
    r""" Returns mistag rate :math:`\langle\omega\rangle=N_{\mathrm{wrong}} / N`

        :param stats: Tagger stats
        :type stats: TaggingData
        :return: Mistag rate
        :rtype: ufloat
    """
    if selected:
        tag_right = np.sum(stats.weights[stats.correct_tags])
        tag_wrong = np.sum(stats.weights[stats.wrong_tags])
        return ufloat(tag_wrong / stats.Nwts, np.sqrt(tag_right * tag_wrong / stats.Nwts) / stats.Nwts)
    else:
        raise NotImplementedError


def tagging_power(tagger, tagrate, calibrated, selected=True):
    r""" Computes the effective tagging efficiency :math:`\epsilon_{\mathrm{tag},\mathrm{eff}}`

        :param tagger: Tagger
        :type tagger: Tagger
        :param tagrate: Tagging rate
        :type tagrate: ufloat
        :param calibrated: Whether to use calibrated mistag instead of raw mistag
        :type calibrated: bool
        :return: Tagging power
        :rtype: tuple
    """

    if selected:
        if calibrated:
            assert tagger.is_calibrated()
            D = np.array(1 - 2 * tagger.cstats.eta)
            mean_D_sq = np.sum(D**2 * tagger.cstats.weights) / tagger.cstats.Nwts  # tagpower of tagged events

            # Propagate errors of mean dilution squared
            grad_calib = tagger.func.gradient(tagger.params_nominal, tagger.cstats.eta, tagger.cstats.dec, tagger.stats.avg_eta)
            grad_mean_D_sq  = -4 * np.sum(grad_calib * D * np.array(tagger.cstats.weights), axis=1) / tagger.cstats.Nwts
            mean_D_sq_err = np.sqrt(grad_mean_D_sq @ tagger.minimizer.covariance.tolist() @ grad_mean_D_sq.T)

            tagpower = tagrate * ufloat(mean_D_sq, mean_D_sq_err)
        else:
            D = 1 - 2 * tagger.stats.eta
            mean_D_sq = np.sum(D**2 * tagger.stats.weights) / tagger.stats.Nwts  # tagpower of tagged events

            tagpower = tagrate * mean_D_sq
    else:
        # Events that are only tagged are not quite as accessible, but that does not really matter
        if calibrated:
            tagged = tagger.cstats.tagged
            eta    = tagger.cstats.all_eta[tagged]
            dec    = tagger.cstats.all_dec[tagged]
            weight = tagger.cstats.all_weights[tagged]

            assert tagger.is_calibrated()
            D = np.array(1 - 2 * eta)
            mean_D_sq = np.sum(D**2 * weight) / tagger.cstats.Nwt  # tagpower of tagged events

            # Propagate errors of mean dilution squared
            grad_calib = tagger.func.gradient(tagger.params_nominal, eta, dec, tagger.stats.avg_eta)  # stats.avg_eta is correct
            grad_mean_D_sq  = -4 * np.sum(grad_calib * D * np.array(weight), axis=1) / tagger.cstats.Nwt
            mean_D_sq_err = np.sqrt(grad_mean_D_sq @ tagger.minimizer.covariance.tolist() @ grad_mean_D_sq.T)

            tagpower = tagrate * ufloat(mean_D_sq, mean_D_sq_err)
        else:
            tagged = tagger.stats.tagged
            eta    = tagger.stats.all_eta[tagged]
            dec    = tagger.stats.all_dec[tagged]
            weight = tagger.cstats.all_weights[tagged]
            D = 1 - 2 * eta
            mean_D_sq = np.sum(D**2 * weight) / tagger.stats.Nwt  # tagpower of tagged events

            tagpower = tagrate * mean_D_sq
    return tagpower


def tagger_correlation(taggers, corr="all", selected=True):
    """ Compute different kinds of tagger correlations

        :param taggers: List of taggers
        :type taggers: list
        :param corr: Type of correlation to compute
        :type corr: string

        :return: Correlation matrix
        :rtype: pandas.DataFrame
    """
    if selected:
        if corr == "fire":
            decdata = pd.DataFrame({ tagger.name : tagger.stats.all_dec[tagger.stats.selected].abs() for tagger in taggers })
        elif corr == "dec":
            decdata = pd.DataFrame({ tagger.name : tagger.stats.all_dec[tagger.stats.selected] for tagger in taggers })
        elif corr == "dec_weight":
            decdata = pd.DataFrame({ tagger.name : tagger.stats.all_dec[tagger.stats.selected] * (1 - 2 * tagger.stats.all_eta[tagger.stats.selected]) for tagger in taggers })
    else:
        if corr == "fire":
            decdata = pd.DataFrame({ tagger.name : tagger.stats.all_dec.abs() for tagger in taggers })
        elif corr == "dec":
            decdata = pd.DataFrame({ tagger.name : tagger.stats.all_dec for tagger in taggers })
        elif corr == "dec_weight":
            decdata = pd.DataFrame({ tagger.name : tagger.stats.all_dec * (1 - 2 * tagger.stats.all_eta) for tagger in taggers })
    return decdata.corr()

