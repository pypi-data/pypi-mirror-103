import os
import numpy as np
import matplotlib.pyplot as plt
from uncertainties import ufloat

from lhcb_ftcalib.calibration_functions import mixing_asymmetry
from lhcb_ftcalib.performance import p_conversion_matrix


def eta_omega_binning(tagger, nbins):
    """ Determines the binning scheme used for plotting histograms

        :param tagger: tagger object
        :type tagger: Tagger
        :param nbins: Number of true mistag bins
        :type nbins: int

        :return: binning
    """

    # Divide eta range into bins of nbins equal sizes
    eta        = tagger.stats.eta
    sorted_eta = sorted(eta)
    splitting  = np.array_split(sorted_eta, nbins)
    binning    = np.array([[s[0], s[-1]] for s in splitting])

    if tagger.mode != "Bu":
        Amix = mixing_asymmetry(tagger.tau, tagger.DeltaM, tagger.DeltaGamma)
        pollution = 0.5 * (1 - np.abs(Amix))
    else:
        pollution = np.zeros(len(eta))

    def true_mistag_bin(eta_lo, eta_hi):
        # Returns true mis-classifiaction percentage in given bin bounds in the form:
        # Weighted mean of eta in bin (x axis) and true mistag estimate with simple binomial error (y axis)
        binmask = (eta >= eta_lo) & (eta < eta_hi)  # Selects bin

        binweights = tagger.stats.weights[binmask]
        oscDsq = np.sum(binweights * (1 - 2 * pollution[binmask])**2) / np.sum(binweights)

        asym  = np.sum(tagger.stats.weights[tagger.stats.correct_tags & binmask] * (1 - 2 * pollution[tagger.stats.correct_tags & binmask]))
        asym -= np.sum(tagger.stats.weights[tagger.stats.wrong_tags & binmask]   * (1 - 2 * pollution[tagger.stats.wrong_tags & binmask]))
        asym /= np.sum(binweights) * oscDsq

        effnum = np.sum(binweights)**2 / np.sum(binweights**2) * oscDsq

        Nw = 0.5 * (1 - asym) * effnum
        Nr = 0.5 * (1 + asym) * effnum
        eff = Nw / (Nw + Nr)

        return np.sum(eta[binmask] * binweights) / np.sum(binweights), ufloat(eff, np.sqrt(eff * (1 - eff) / Nw))

    omega_true = [true_mistag_bin(lo, hi) for lo, hi in binning]
    return binning, [ot[0] for ot in omega_true], [ot[1] for ot in omega_true]


def calibration_lineshape(tagger, eta_plot):
    """ Returns the lineshape of the calibration curve
        corresponding to the input eta range.

        :param tagger: Tagger object
        :type tagger: Tagger
        :param eta_plot: List of increasing eta values for plotting
        :type eta_plot: list

        :return: calibration curve points
        :return type: list
    """
    return tagger.func.eval_plotting(tagger.params_nominal, eta_plot, tagger.stats.dec, tagger.stats.avg_eta)


def confidence_bands_lineshape(tagger, eta_plot, dec_plot):
    """ Returns the lineshape of the calibration curve
        corresponding to the input eta range.

        :param tagger: Tagger object
        :type tagger: Tagger
        :param eta_plot: List of increasing eta values for plotting
        :type eta_plot: list

        :return: 1-sigma confidence band line shape
        :return type: list
    """
    assert len(eta_plot) == len(dec_plot)
    J = tagger.func.gradient(tagger.params_nominal, eta_plot, dec_plot, tagger.stats.avg_eta).T
    cov = tagger.minimizer.covariance.tolist()

    band = np.array([np.sqrt(j @ cov @ j.T) for j in J])

    return band


def print_fit_setup(ax, position, tagger, uformat="{:L}"):
    """ Print calibration parameters in flavour style to the canvas

    :param ax: matplotlib axis
    :type ax: matplotlib.pyplot.axis
    :param position: x and y coordinate of starting corner
    :type position: list
    :param tagger: Tagger object
    :type tagger: Tagger
    :param uformat: uncertainties.ufloat formatting string. Alternative suggestion: "{:1uS}"
    :type uformat: str
    """
    conv_mat = p_conversion_matrix(tagger.func.npar)
    param = tagger.func.param_names
    param = [p.replace("-", "").replace("+", "") for p in param]
    param = [p.replace("p", "p_") for p in param]
    for i, p in enumerate(param[tagger.func.npar:]):
        param[i + tagger.func.npar] = r"\Delta " + p

    cov = tagger.minimizer.covariance
    noms  = conv_mat @ tagger.params_nominal
    uncts = np.sqrt(np.diag(conv_mat @ np.array(cov.tolist()) @ conv_mat.T))

    param = ["$" + p + "=" + uformat.format(ufloat(n, s)) + "$" for n, s, p in zip(noms, uncts, param)]

    text = "\n".join(param) + "\n"
    text += tagger.func.link.__name__ + " link"
    ax.text(x=position[0], y=position[1], s=text, transform = ax.transAxes)


def get_eta_plotrange(eta_range, binning):
    if isinstance(eta_range, list) or isinstance(eta_range, tuple):
        # User chose range
        return eta_range
    if eta_range == "minimal":
        eta_range = [binning[0][0], binning[-1][1]]
        eta_interv = eta_range[1] - eta_range[0]
        # Add padding
        eta_range[0] -= eta_interv * 0.02
        eta_range[1] += eta_interv * 0.02
    elif eta_range == "full":
        eta_range = [0, 0.5]
    return eta_range


def get_omega_plotrange(omega_range, omega_true, curve):
    if isinstance(omega_range, list) or isinstance(omega_range, tuple):
        # User chose range
        return omega_range
    if omega_range == "minimal":
        # Actually, this imitates the EPM where, the curve also determines the omega range
        omega_range = [min(np.nanmin(curve), np.nanmin([o.n - o.s for o in omega_true])),
                       max(np.nanmax(curve), np.nanmax([o.n + o.s for o in omega_true]))]
        # Add padding
        omega_interv = omega_range[1] - omega_range[0]
        omega_range[0] -= omega_interv * 0.02
        omega_range[1] += omega_interv * 0.02

    return omega_range


def draw_calibration_curve(tagger, nbins=10, eta_range="minimal", omega_range="minimal", print_params=True, params_position="auto", title=None, samples=100, nsigma=2, sigma_color=[0.1, 0.7, 0.1], nsigmaoutline=False, etabins=100, savepath="."):
    """ Plots the calibration curve of a tagger including the confidence bands,
        true mistag and binned measured mistag distribution

        :param tagger: Tagger object
        :type tagger: Tagger
        :param nbins: Number of true mistag bins to plot
        :type nbins: int
        :param eta_range: measured mistag plot range
        :type eta_range: "minimal" or list
        :param omega_range: true mistag range
        :type omega_range: "minimal" or list
        :param print_params: Whether to plot the calibration parameters
        :type print_params: bool
        :param params_position: Text box position
        :type params_position: "auto" or [x, y] pair list
        :param title: Title to use instead of tagger name (default)
        :type title: str
        :param sample: How many curve points to plot (Plotting precision)
        :type sample: int
        :param nsigma: how many sigma intervals to plot
        :type nsigma: int
        :param sigma_color: R,G,B list
        :type sigma_color: list
        :param nsigmaoutline: whether to outline the last sigma interval
        :type nsigmaoutline: bool
        :param etabins: Number of bins for the eta histogram
        :type etabins: int
        :param savepath: Path to the plot folder
        :type savepath: str
    """
    if title is None:
        title = tagger.name + " Calibration"

    # Matplotlib
    fig, ax_calib = plt.subplots()
    ax_calib.set_title(title)

    # Get binning scheme, eta x values and true mistag rates including stat. uncertainty
    binning, eta_points, omega_true = eta_omega_binning(tagger, nbins)

    eta_range = get_eta_plotrange(eta_range, binning)

    eta_plot = np.linspace(eta_range[0], eta_range[1], samples)  # "Continuous" eta for plotting

    # Plot calibration curve and mean mistag
    curve = calibration_lineshape(tagger, eta_plot)
    ax_calib.plot(eta_plot, curve, color='k', label="Calibration", linewidth=0.5)

    omega_range = get_omega_plotrange(omega_range, omega_true, curve)

    # Draw confidence bands
    bandsplus = confidence_bands_lineshape(tagger, eta_plot,  np.ones(samples))
    bandsminus = confidence_bands_lineshape(tagger, eta_plot, -np.ones(samples))
    bands = (bandsplus + bandsminus) / 2

    for ns in reversed(range(nsigma)):
        ax_calib.fill_between(eta_plot, curve - (ns + 1) * bands, curve + (ns + 1) * bands, facecolor=(sigma_color + [1 - ns / nsigma]))

    if nsigmaoutline:
        # Draw an outline
        plt.plot(eta_plot, curve + nsigma * bands, color='k', linewidth=0.05)
        plt.plot(eta_plot, curve - nsigma * bands, color='k', linewidth=0.05)

    # Plot true omega
    ax_calib.errorbar(x          = eta_points,
                      y          = [ot.n for ot in omega_true],
                      xerr       = [eta_points - binning[:, 0], binning[:, 1] - eta_points],
                      yerr       = [ot.s for ot in omega_true],
                      color      = 'k',
                      fmt        = '.',
                      capsize    = 2,
                      elinewidth = 0.7,
                      capthick   = 0.7,
                      markersize = 4,
                      label      = r"$\omega^{\mathrm{true}}$")
    ax_calib.set_xlabel(r'Predicted mistag $\eta$')
    ax_calib.set_ylabel(r'Measured mistag $\omega$')
    ax_calib.set_xlim(*eta_range)
    ax_calib.set_ylim(*omega_range)

    if print_params:
        if params_position == "auto":
            print_fit_setup(ax_calib, [0.7, 0.25], tagger)
        else:
            print_fit_setup(ax_calib, params_position, tagger)

    ax_calib.plot([0, 0.5], [0, 0.5], color='b', linestyle=(0, (5, 10)), linewidth=0.5, label="Identity")
    ax_calib.legend(loc="upper left")

    ax_etahist = ax_calib.twinx()
    etacolor = [0, 0, 0, 0.2]
    ax_etahist.hist(tagger.stats.eta, range=eta_range, bins=etabins, density=True, histtype="stepfilled", color=etacolor, label=r"$\eta$")
    ax_etahist.set_ylabel(r"$\eta\;/\;" + "{:.2}".format((eta_range[1] - eta_range[0]) / etabins) + "$")
    ax_etahist.tick_params(axis='y', labelcolor='k')
    ax_etahist.set_ylim(0, ax_etahist.get_ylim()[1] * 2)
    ax_etahist.legend(loc="center right")

    plt.savefig(os.path.join(savepath, f"{tagger.name}_Calibration.pdf"))
    return f"{tagger.name}_Calibration.pdf"


def draw_inputcalibration_curve(tagger, nbins=10, eta_range="minimal", omega_range=[0, 0.5], print_params=True, params_position="auto", title=None, samples=100, nsigma=2, sigma_color=[0.7, 0.7, 0.7], nsigmaoutline=False, etabins=100, savepath="."):
    """ Plots the input calibration curve of a loaded tagger including the confidence bands,
        true mistag and binned measured mistag distribution

        :param tagger: TargetTagger object
        :type tagger: TargetTagger
        :param nbins: Number of true mistag bins to plot
        :type nbins: int
        :param eta_range: measured mistag plot range
        :type eta_range: "minimal" or list
        :param omega_range: true mistag range
        :type omega_range: list
        :param print_params: Whether to plot the calibration parameters
        :type print_params: bool
        :param params_position: Text box position
        :type params_position: "auto" or [x, y] pair list
        :param title: Title to use instead of tagger name (default)
        :type title: str
        :param sample: How many curve points to plot (Plotting precision)
        :type sample: int
        :param nsigma: how many sigma intervals to plot
        :type nsigma: int
        :param sigma_color: R,G,B list
        :type sigma_color: list
        :param nsigmaoutline: whether to outline the last sigma interval
        :type nsigmaoutline: bool
        :param etabins: Number of bins for the eta histogram
        :type etabins: int
        :param savepath: Path to the plot folder
        :type savepath: str
    """
    if title is None:
        title = tagger.name + " Input Calibration"

    # Matplotlib
    fig, ax_calib = plt.subplots()
    ax_calib.set_title(title)

    if eta_range == "minimal":
        eta = tagger.stats.eta
        eta_range = [np.nanmin(eta), 0.5]
        eta_range[0] -= (eta_range[1] - eta_range[0]) * 0.02

    eta_plot = np.linspace(eta_range[0], eta_range[1], samples)  # "Continuous" eta for plotting

    # Plot calibration curve and mean mistag
    curve = calibration_lineshape(tagger, eta_plot)
    ax_calib.plot(eta_plot, curve, color='k', label="Input Calibration", linewidth=0.5)

    # Draw confidence bands
    bandsplus = confidence_bands_lineshape(tagger, eta_plot,  np.ones(samples))
    bandsminus = confidence_bands_lineshape(tagger, eta_plot, -np.ones(samples))
    bands = (bandsplus + bandsminus) / 2

    for ns in reversed(range(nsigma)):
        ax_calib.fill_between(eta_plot, curve - (ns + 1) * bands, curve + (ns + 1) * bands, facecolor=(sigma_color + [1 - ns / nsigma]))

    if nsigmaoutline:
        # Draw an outline
        plt.plot(eta_plot, curve + nsigma * bands, color='k', linewidth=0.05)
        plt.plot(eta_plot, curve - nsigma * bands, color='k', linewidth=0.05)

    ax_calib.set_xlabel(r'Predicted mistag $\eta$')
    ax_calib.set_ylabel(r'Measured mistag $\omega$')
    ax_calib.set_xlim(*eta_range)
    ax_calib.set_ylim(*omega_range)

    if print_params:
        if params_position == "auto":
            print_fit_setup(ax_calib, [0.05, 0.65], tagger)
        else:
            print_fit_setup(ax_calib, params_position, tagger)

    ax_calib.plot([0, 0.5], [0, 0.5], color='b', linestyle=(0, (5, 10)), linewidth=0.5, label="Identity")
    ax_calib.legend(loc="upper left")

    ax_etahist = ax_calib.twinx()
    etacolor = [0, 0, 0]
    ax_etahist.hist(tagger.stats.eta, range=eta_range, bins=etabins, density=True, histtype="step", color=etacolor, label=r"$\eta$")
    ax_etahist.set_ylabel(r"$\eta\;/\;" + "{:.2}".format((eta_range[1] - eta_range[0]) / etabins) + "$")
    ax_etahist.tick_params(axis='y', labelcolor='k')
    ax_etahist.set_ylim(0, ax_etahist.get_ylim()[1] * 2)
    ax_etahist.legend(loc="center right")

    plt.savefig(os.path.join(savepath, f"{tagger.name}_InputCalibration.pdf"))
    return f"{tagger.name}_InputCalibration.pdf"
