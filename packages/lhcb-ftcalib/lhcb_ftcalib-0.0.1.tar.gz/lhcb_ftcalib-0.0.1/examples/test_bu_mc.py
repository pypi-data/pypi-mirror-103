import os
import sys
import numpy as np
import uproot
sys.path.append('..')
import matplotlib as mpl
mpl.rc('text', usetex=True)
mpl.use("agg")

import lhcb_ftcalib as ft

F = uproot.open("../data/MC_JpsiK_2016.root")["DecayTree"]
print("Loading data")

df = F.arrays(filter_name=["*_ETA", "*_DEC", "ID", "eventNumber"], library="pd")
outdir = "plots_Bu"
os.mkdir(outdir)

selection = df.eventNumber > -np.inf

SStaggers = ft.TaggerCollection()
SStaggers.create_tagger("SSp",   df.SSProton_ETA,         df.SSProton_DEC,         df.ID, "Bu", selection=selection)
SStaggers.create_tagger("SSpi",  df.SSPion_ETA,           df.SSPion_DEC,           df.ID, "Bu", selection=selection)

OStaggers = ft.TaggerCollection()
OStaggers.create_tagger("VtxCh", df.OSVtxCh_ETA,          df.OSVtxCh_DEC,          df.ID, "Bu", selection=selection)
OStaggers.create_tagger("OSe",   df.OSElectronLatest_ETA, df.OSElectronLatest_DEC, df.ID, "Bu", selection=selection)
OStaggers.create_tagger("OSmu",  df.OSMuonLatest_ETA,     df.OSMuonLatest_DEC,     df.ID, "Bu", selection=selection)
OStaggers.create_tagger("OSk",   df.OSKaonLatest_ETA,     df.OSKaonLatest_DEC,     df.ID, "Bu", selection=selection)
OStaggers.create_tagger("OSc",   df.OSCharm_ETA,          df.OSCharm_DEC,          df.ID, "Bu", selection=selection)


SStaggers.calibrate()
OStaggers.calibrate()

SStaggers.plot_calibration_curves(savepath=outdir)
OStaggers.plot_calibration_curves(savepath=outdir)

ft.save_calibration(SStaggers, outdir + "/MC_Bu2JpsiK_SS")
ft.save_calibration(OStaggers, outdir + "/MC_Bu2JpsiK_OS")

TagCombinations = ft.TaggerCollection(
    SStaggers.combine_taggers("SScomb", True),
    OStaggers.combine_taggers("OScomb", True)
)
print(TagCombinations)

TagCombinations.calibrate()
TagCombinations.plot_calibration_curves(savepath=outdir)
ft.save_calibration(TagCombinations, outdir + "/MC_Bu2JpsiK_Comb")
