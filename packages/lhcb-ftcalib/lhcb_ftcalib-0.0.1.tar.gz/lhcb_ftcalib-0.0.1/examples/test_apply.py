import os
import numpy as np
import uproot
import matplotlib as mpl
mpl.rc('text', usetex=True)
import matplotlib.pyplot as plt

import lhcb_ftcalib as ft

F = uproot.open("../data/Data_JpsiKS_2016.root")["DecayTree"]

df = F.pandas.df(["*_ETA", "*_DEC", "SWsig"])

targets = ft.TargetTaggerCollection()
targets.create_tagger("OSmu", df.OSMuonLatest_ETA,     df.OSMuonLatest_DEC,     df.SWsig)
targets.create_tagger("OSk",  df.OSKaonLatest_ETA,     df.OSKaonLatest_DEC,     df.SWsig)
targets.create_tagger("OSe",  df.OSElectronLatest_ETA, df.OSElectronLatest_DEC, df.SWsig)
targets.create_tagger("OSc",  df.OSCharm_ETA,          df.OSCharm_DEC,          df.SWsig)

targets.load_calibrations("plots_Bd_data/Data_Bd2JpsiKstar_OS.json")
ft.print_tagger_statistics(targets, calibrated=False)
targets.apply()
ft.print_tagger_statistics(targets, calibrated=True)

targets.plot_inputcalibration_curves(savepath="plots_Bd_data")
