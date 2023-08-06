import json
import uuid
import numbers
import numpy as np

from lhcb_ftcalib.Tagger import Tagger
from lhcb_ftcalib.performance import tagging_rate, tagging_power, p_conversion_matrix
from lhcb_ftcalib.printing import warning, raise_error
from lhcb_ftcalib.TaggerCollection import TaggerCollection


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
    def write_calibration_dict(tagger):
        conv_mat = p_conversion_matrix(tagger.func.npar)
        paramnames = tagger.func.param_names
        paramnames_delta = [p.replace("-", "").replace("+", "") for p in paramnames]
        for i, p in enumerate(paramnames_delta[tagger.func.npar:]):
            paramnames_delta[i + tagger.func.npar] = "D" + p

        cov = tagger.minimizer.covariance

        def serial_ufloat(uf):
            return [uf.n, uf.s]

        calib = {
            tagger.name : {
                tagger.func.__class__.__name__ : {
                    "degree" : tagger.func.npar - 1,
                    "link"   : tagger.func.link.__name__
                },
                "calibration" : {
                    "avg_eta" : tagger.stats.avg_eta,
                    "flavour_style" : {
                        "params" : { pn : value for pn, value in zip(paramnames, tagger.params_nominal) },
                        "uncert" : { pn : value for pn, value in zip(paramnames, tagger.params_uncerts) },
                        "cov"    : cov.tolist(),
                    },
                    "delta_style" : {
                        "params" : { pn : value for pn, value in zip(paramnames_delta, conv_mat @ tagger.params_nominal) },
                        "uncert" : { pn : value for pn, value in zip(paramnames_delta, np.sqrt(np.diag(conv_mat @ cov.tolist() @ conv_mat.T))) },
                        "cov"    : (conv_mat @ cov @ conv_mat.T).tolist(),
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
                        "tag_efficiency" : serial_ufloat(tagging_rate(tagger.stats, selected=True)),
                        "tag_power" : serial_ufloat(tagging_power(tagger, tagging_rate(tagger.stats, selected=True), calibrated=False)),
                    },
                    "all" : {
                        "tag_efficiency" : serial_ufloat(tagging_rate(tagger.stats, selected=False)),
                        "tag_power" : serial_ufloat(tagging_power(tagger, tagging_rate(tagger.stats, selected=False), calibrated=False, selected=False)),
                    },
                },
                "calibrated" : {
                    "selected" : {
                        "Nts"   : tagger.cstats.Nts,
                        "Nwts"  : tagger.cstats.Nwts,
                        "tag_efficiency" : serial_ufloat(tagging_rate(tagger.cstats, selected=True)),
                        "tag_power" : serial_ufloat(tagging_power(tagger, tagging_rate(tagger.cstats, selected=True), calibrated=True)),
                    },
                    "all" : {
                        "Nt"   : tagger.cstats.Nt,
                        "Nwt"  : tagger.cstats.Nwt,
                        "tag_efficiency" : serial_ufloat(tagging_rate(tagger.cstats, selected=False)),
                        "tag_power" : serial_ufloat(tagging_power(tagger, tagging_rate(tagger.cstats, selected=False), calibrated=True)),
                    },
                }
            }
        }
        return _serialize(calib)

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
        json.dump(calib, open(filename, "w"), indent=indent)
