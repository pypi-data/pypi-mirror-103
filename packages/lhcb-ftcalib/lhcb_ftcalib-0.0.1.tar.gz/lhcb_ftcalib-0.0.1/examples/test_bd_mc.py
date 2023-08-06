import os
import sys
import uproot
sys.path.append('..')
import matplotlib as mpl
mpl.rc('text', usetex=True)

import lhcb_ftcalib as ft
mpl.use("agg")

F = uproot.open("../data/MC_JpsiKstar_2016.root")["DecayTree"]
print("Loading data")

df = F.arrays(filter_name=["*_ETA", "*_DEC", "ID", "TAU", "TAUERR"], library="pd")

tau_ps = df.TAU * 1000
outdir = "plots_Bd"
os.mkdir(outdir)

SStaggers = ft.TaggerCollection()
SStaggers.create_tagger("SSp",   df.SSProton_ETA,         df.SSProton_DEC,         df.ID, "Bd", tau_ps=tau_ps)
SStaggers.create_tagger("SSpi",  df.SSPion_ETA,           df.SSPion_DEC,           df.ID, "Bd", tau_ps=tau_ps)

OStaggers = ft.TaggerCollection()
OStaggers.create_tagger("VtxCh", df.OSVtxCh_ETA,          df.OSVtxCh_DEC,          df.ID, "Bd", tau_ps=tau_ps)
OStaggers.create_tagger("OSe",   df.OSElectronLatest_ETA, df.OSElectronLatest_DEC, df.ID, "Bd", tau_ps=tau_ps)
OStaggers.create_tagger("OSmu",  df.OSMuonLatest_ETA,     df.OSMuonLatest_DEC,     df.ID, "Bd", tau_ps=tau_ps)
OStaggers.create_tagger("OSk",   df.OSKaonLatest_ETA,     df.OSKaonLatest_DEC,     df.ID, "Bd", tau_ps=tau_ps)
OStaggers.create_tagger("OSc",   df.OSCharm_ETA,          df.OSCharm_DEC,          df.ID, "Bd", tau_ps=tau_ps)

SStaggers.calibrate()
OStaggers.calibrate()

ft.save_calibration(SStaggers, outdir + "/MC_Bd2JpsiKstar_SS")
ft.save_calibration(OStaggers, outdir + "/MC_Bd2JpsiKstar_OS")

SStaggers.plot_calibration_curves(savepath=outdir)
OStaggers.plot_calibration_curves(savepath=outdir)

TagCombinations = ft.TaggerCollection(
    SStaggers.combine_taggers("SScomb", True),
    OStaggers.combine_taggers("OScomb", True)
)

TagCombinations.calibrate()
TagCombinations.plot_calibration_curves(savepath=outdir)
ft.save_calibration(TagCombinations, outdir + "/MC_Bd2JpsiKstar_Comb")
