import sys
import numpy as np
import uproot
sys.path.append('..')

from lhcb_ftcalib.TaggingData import TaggingData

F = uproot.open("../data/Data_JpsiK_2016.root")["DecayTree"]
df = F.pandas.df(["*_ETA", "*_DEC", "ID", "TAU", "TAUERR", "SWsig"])

stats = TaggingData(df.OSMuonLatest_ETA, df.OSMuonLatest_DEC, df.ID, df.SWsig, 521)

stats.set_selection_index(np.arange(100000)[::2])

print(stats._data[stats._data.tagged_sel])
