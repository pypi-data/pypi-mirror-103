import os
import json
import uuid
import numbers

from lhcb_ftcalib.Tagger import Tagger
from lhcb_ftcalib.performance import tagging_rate, tagging_power
from lhcb_ftcalib.printing import warning, raise_error
from lhcb_ftcalib.TaggerCollection import TaggerCollection
from lhcb_ftcalib.printing import info


def _serialize(DICT):
    serialized = {}
    if isinstance(DICT, dict):
        for key, val in DICT.items():
            if isinstance(val, dict):
                serialized[key] = _serialize(val)
            elif isinstance(val, numbers.Number):
                serialized[key] = str(val)
            elif isinstance(val, list):
                serialized[key] = [_serialize(v) for v in val]
            else:
                serialized[key] = val
    else:
        if isinstance(DICT, dict):
            return _serialize(DICT)
        elif isinstance(DICT, numbers.Number):
            return str(DICT)
        elif isinstance(DICT, list):
            return [_serialize(v) for v in DICT]
        else:
            return DICT
    return serialized


def save_calibration(taggers, title=None, protocol="json", indent=4):
    """ Writes calibrations of calibrated taggers to a file.

        :param taggers: Calibrated taggers
        :type taggers: TaggerCollection or list
        :param title: Title of calibration file. By default, filename will be assigned a uuid. If file exists, calibrations are appended.
        :type title: str
        :param protocol: Type of protocol to use for writing the calibration
        :type protocol: Must be "json", as nothing else is supported
        :param indent: Number of indentation spaces to use in the calibration file
        :type indent: int
    """
    def write_calibration_dict(tagger):
        ps_flav, nom_flav, unc_flav, cov_flav = tagger.get_fitparameters(style="flavour", tex=False, greekdelta=False)
        ps_delta, nom_delta, unc_delta, cov_delta = tagger.get_fitparameters(style="delta", tex=False, greekdelta=False)

        def serial_ufloat(uf):
            return [uf.n, uf.s]

        assert protocol == "json"

        cov_delta = cov_delta.tolist()
        cov_flav = cov_flav.tolist()

        calib = {
            tagger.name : {
                tagger.func.__class__.__name__ : {
                    "degree" : tagger.func.npar - 1,
                    "link"   : tagger.func.link.__name__
                },
                "osc" : {
                    "DeltaM"     : tagger.DeltaM,
                    "DeltaGamma" : tagger.DeltaGamma,
                    "Aprod"      : tagger.Aprod,
                },
                "calibration" : {
                    "avg_eta" : tagger.stats.avg_eta,
                    "flavour_style" : {
                        "params" : { pn : [n, s] for pn, n, s in zip(ps_flav, nom_flav, unc_flav) },
                        "cov"    : cov_flav,
                    },
                    "delta_style" : {
                        "params" : { pn : [n, s] for pn, n, s in zip(ps_delta, nom_delta, unc_delta) },
                        "cov"    : cov_delta,
                    }
                },
                "stats" : {
                    "N"    : tagger.stats.N,
                    "Nt"   : tagger.stats.Nt,
                    "Neff" : tagger.stats.Neff,
                    "Nw"   : tagger.stats.Nw,
                    "Nwt"  : tagger.stats.Nwt,
                },
                "selected_stats" : {
                    "Ns"    : tagger.stats.Ns,
                    "Nts"   : tagger.stats.Nts,
                    "Neffs" : tagger.stats.Neffs,
                    "Nws"   : tagger.stats.Nws,
                    "Nwts"  : tagger.stats.Nwts,
                },
                "uncalibrated" : {
                    "selected" : {
                        "tag_efficiency" : serial_ufloat(tagging_rate(tagger, calibrated=False, selected=True)),
                        "tag_power" :      serial_ufloat(tagging_power(tagger, calibrated=False, selected=True)),
                    },
                    "all" : {
                        "tag_efficiency" : serial_ufloat(tagging_rate(tagger, calibrated=False, selected=False)),
                        "tag_power" :      serial_ufloat(tagging_power(tagger, calibrated=False, selected=False)),
                    },
                },
                "calibrated" : {
                    "selected" : {
                        "Nts"            : tagger.cstats.Nts,
                        "Nwts"           : tagger.cstats.Nwts,
                        "tag_efficiency" : serial_ufloat(tagging_rate(tagger, calibrated=True, selected=True)),
                        "tag_power"      : serial_ufloat(tagging_power(tagger, calibrated=True, selected=True)),
                    },
                    "all" : {
                        "Nt"             : tagger.cstats.Nt,
                        "Nwt"            : tagger.cstats.Nwt,
                        "tag_efficiency" : serial_ufloat(tagging_rate(tagger, calibrated=True, selected=False)),
                        "tag_power"      : serial_ufloat(tagging_power(tagger, calibrated=True, selected=False)),
                    },
                }
            }
        }
        return _serialize(calib)

    title = str(title) if title is not None else None  # Support pathlib et al

    if isinstance(taggers, TaggerCollection) or isinstance(taggers, list):
        calib = {}
        if title is None:
            warning("Calibration file has no specific title")
            title = "Calibration-" + str(uuid.uuid1())
        for tagger in taggers:
            calib.update(write_calibration_dict(tagger))
    elif isinstance(taggers, Tagger):
        title = title or taggers.name
        calib = write_calibration_dict(taggers)
    else:
        raise_error(False, "Tagger type unknown")

    if protocol == "json":
        filename = title + ".json" if not title.endswith(".json") else title

        if os.path.exists(filename):
            info(f"Calibration file {filename} exists: Appending calibrations")
            existing = json.load(open(filename, "r"))
            existing.update(calib)
            json.dump(existing, open(filename, "w"), indent=indent)
        else:
            json.dump(calib, open(filename, "w"), indent=indent)
