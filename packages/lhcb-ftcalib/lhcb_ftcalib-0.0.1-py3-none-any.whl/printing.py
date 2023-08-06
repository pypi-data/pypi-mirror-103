import numpy as np
from lhcb_ftcalib.calibration_functions import PolynomialCalibration
from lhcb_ftcalib.performance import tagging_rate, raw_mistag_rate, tagging_power, tagger_correlation


def epmstyle_header(msg):
    print('\033[1m\033[94m' + (len(msg) + 12) * "-")
    print(f"----- {msg} -----")
    print((len(msg) + 12) * "-" + '\033[0m')


def printbold(msg, kwargs={}):
    # Blue EPM style paragraph title frame
    print('\033[1m\033[97m' + msg + "\033[0m", **kwargs)


def correlation_header(msg):
    # EPM style correlation header
    print(80 * '/' + f"\n\033[1m{msg} [%]\033[0m\n" + 80 * '/')


def section_header(msg):
    # EPM style section header
    print('\n\033[1m' + (len(msg) + 32) * "-")
    print(15 * '-' + f" {msg} " + 15 * '-')
    print((len(msg) + 32) * "-" + '\033[0m\n')


def warning(*msg):
    print("\033[1m\033[33m WARNING \033[0m", *msg)


def info(*msg):
    print("\033[1m\033[97m INFO \033[0m", *msg)


def raise_warning(cond, msg):
    if not cond:
        print(f"\033[1m\033[33m WARNING:\033[0m {msg}")


def raise_error(cond, msg):
    if not cond:
        print(f"\033[1m\033[31m ERROR:\033[0m {msg}")
        exit(1)


def print_tagger_statistics(taggers, calibrated):
    """ Prints basic statistics of the input data for each tagger

        :param taggers: List of taggers
        :type taggers: list
        :param calibrated: Whether to show calibrated tagger statistics (after calibration)
        :type taggers: bool
    """
    if calibrated:
        section_header("CALIBRATED TAGGER STATISTICS")
    else:
        section_header("TAGGER STATISTICS")

    header = "\033[1m\033[32m{:>15}   {:<15}{:<15}{:<15}{:<15}{:<15}"
    print(header.format("Tagger", "#Evts (N)", "weighted Σw", "(Σw)² / Σw²", "#Tagged", "Σ_tag * w"))
    for tagger in taggers:
        infoline = "\033[1m\033[32m{:>15}\033[0m   ".format(tagger.name)
        if calibrated:
            infoline += "{:<15}{:<15}{:<15}{:<15}{:<15}".format(tagger.cstats.N,
                                                                np.round(tagger.cstats.Nw, 2),
                                                                np.round(tagger.cstats.Neff, 2),
                                                                tagger.cstats.Nt,
                                                                np.round(tagger.cstats.Nwt, 2))
        else:
            infoline += "{:<15}{:<15}{:<15}{:<15}{:<15}".format(tagger.stats.N,
                                                                np.round(tagger.stats.Nw, 2),
                                                                np.round(tagger.stats.Neff, 2),
                                                                tagger.stats.Nt,
                                                                np.round(tagger.stats.Nwt, 2))
        print(infoline)


def print_tagger_performances(taggers, calibrated=False, round_digits=4):
    """ Prints a table with standard performance numbers like the tagging rate,
        the mistag rate and the tagging power for each tager

        :param taggers: List of taggers
        :type taggers: list
        :param calibrated: Whether to show calibrated tagger statistics (after calibration)
        :type taggers: bool
        :param round_digits: Number of digits to round to
        :type calibrated: int
    """
    def vformat(v):
        return np.round(v, round_digits)

    if not calibrated:
        section_header("TAGGING PERFORMANCES")
        header = "\033[1m\033[32m{:>15}{:>20}{:>24}{:>24}\033[0m"
        print(header.format("", "Tagging Rate", "Mistag", "Tagging Power"))
        print(header.format("Tagger", "ε = Ntag / Nall", "<η> = Nwrong / Ntag", "ε*Σw(1-2η)² / Nt"))
        for tagger in taggers:
            tagrate    = tagging_rate(tagger.stats)
            raw_mistag = raw_mistag_rate(tagger.stats)
            tagpower   = tagging_power(tagger, tagrate, calibrated)
            tagrate *= 100
            raw_mistag *= 100

            infoline  = '\033[1m\033[32m{:>15}\033[0m ({:>7} ± {:>6})'.format(tagger.name, vformat(tagrate.n), vformat(tagrate.s)) + '%'
            infoline += '     ({:>7} ± {:>6})'.format(vformat(raw_mistag.n), vformat(raw_mistag.s)) + '%'
            infoline += '     ({:>7} ± {:>6})'.format(vformat(100 * tagpower.n), vformat(100 * tagpower.s)) + '%'
            print(infoline)
    else:
        section_header("CALIBRATED TAGGING PERFORMANCES")
        header = "\033[1m\033[32m{:>15}{:>20}{:>24}{:>36}\033[0m"
        print(header.format("", "Tagging Rate", "Mistag", "Tagging Power"))
        print(header.format("Tagger", "ε = Ntag / Nall", "<ω> = Nwrong / Ntag", "ε*Σw(1-2ω)² / Nt"))
        for tagger in taggers:
            tagrate    = tagging_rate(tagger.cstats)
            raw_mistag = raw_mistag_rate(tagger.cstats)
            tagpower   = tagging_power(tagger, tagrate, calibrated)
            tagrate *= 100
            raw_mistag *= 100

            infoline  = '\033[1m\033[32m{:>15}\033[0m ({:>7} ± {:>6})'.format(tagger.name, vformat(tagrate.n), vformat(tagrate.s)) + '%'
            infoline += '     ({:>7} ± {:>6})'.format(vformat(raw_mistag.n), vformat(raw_mistag.s)) + '%'
            infoline += '     ({:>7} ± {:>6}(stat+calib))'.format(vformat(100 * tagpower.n), vformat(100 * tagpower.s)) + '%'
            print(infoline)


def print_tagger_correlation(taggers, option="all"):
    """ Print different kinds of tagger correlations

        :param taggers: List of taggers
        :type taggers: list
        :param option: Type of correlation to compute ("fire", "dec", "dec_weight")
        :type option: string
    """
    if option in ("all", "fire"):
        correlation_header("Tagger Fire Correlations")
        print(100 * tagger_correlation(taggers, "fire"), '\n' + 80 * '/', '\n')
    if option in ("all", "dec"):
        correlation_header("Tagger Decision Correlations")
        print(100 * tagger_correlation(taggers, "dec"), '\n' + 80 * '/', '\n')
    if option in ("all", "dec_weight"):
        correlation_header("Tagger Decision Correlations (dilution weighted)")
        print(100 * tagger_correlation(taggers, "dec_weight"), '\n' + 80 * '/', '\n')


def print_calibration_info(tagger):
    """ Prints the obtained calibration parameters of a tagger after it has been calibrated

        :param taggers: List of taggers
        :type taggers: list
    """
    assert tagger.is_calibrated()

    def fmt(val, uncert):
        return "{:>10} ± {:>9}".format(np.round(val, 7), np.round(uncert, 7))

    epmstyle_header(f"Calibration result of {tagger.name}")
    printbold("=== Oscillation parameters ===")
    print(f"Δm    = {tagger.DeltaM} ps^-1")
    print(f"ΔΓ    = {tagger.DeltaGamma} ps^-1")
    print(f"Aprod = {tagger.Aprod}")
    printbold("=== Result in flavour specific representation ===")
    ps, noms, uncerts, cov = tagger.get_fitparameters(style="flavour", p1minus1=True, tex=False, greekdelta=False)

    for name, val, uncert in zip(ps, noms, uncerts):
        print(f"{name}", fmt(val, uncert))
    print("<η> =", tagger.stats.avg_eta)

    if isinstance(tagger.func, PolynomialCalibration):
        printbold("=== Result in p_i, Δp_i convention ===")
        # "EPM printing convention"
        ps, noms, uncerts, cov = tagger.get_fitparameters(style="delta", p1minus1=True, tex=False, greekdelta=True)

        for name, val, uncert in zip(ps, noms, uncerts):
            print(f"{name}", fmt(val, uncert))
        print("<η> =", tagger.stats.avg_eta)
