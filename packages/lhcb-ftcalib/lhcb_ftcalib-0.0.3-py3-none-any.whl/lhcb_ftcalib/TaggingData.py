import numpy as np
import pandas as pd

from lhcb_ftcalib.printing import raise_error


class TaggingData:
    r"""
    TaggingData
    Type for keeping track of tagging data and basic event statistics

    :param eta_data: Uncalibrated mistags
    :type eta_data: list
    :param dec_data: Uncalibrated tagging decisions
    :type dec_data: list
    :param ID: B meson particle IDs
    :type ID: list
    :param weights: Per-event weights
    :type weights: list
    :param absid: Absolute B meson particle ID
    :type absid: int
    :param ignore_out_of_range: Whether to ignore mistag values :math:`\eta\notin [0,0.5]` (not recommended)
    :type ignore_out_of_range: bool
    """
    def __init__(self, eta_data, dec_data, ID, weights, absid, selection, ignore_eta_out_of_range=False):
        self.all_eta   = pd.Series(eta_data)   #: All eta values
        self.all_dec   = pd.Series(dec_data)   #: All dec values
        self.all_B_ID  = pd.Series(ID)         #: All B meson IDs
        self.selected  = pd.Series(selection)  #: Mask of events in selection

        if not ignore_eta_out_of_range:
            self.overflow  = (self.all_eta > 0.5)  #: Mask of events with :math:`\omega>0.5`
            self.underflow = (self.all_eta < 0)    #: Mask of events with :math:`\omega<0`
            self.noverflow = self.overflow.sum()   #: Number of calibrated mistags > 0.5

            self.all_eta[self.overflow] = 0.5
            self.all_eta[self.underflow] = 0
            self.all_dec[self.overflow] = 0

        self.tagged     = self.all_dec != 0                    #: Mask of tagged events
        self.tagged_sel = (self.all_dec != 0) & self.selected  #: Mask of selected and tagged events
        self.dec        = pd.Series(self.all_dec[self.tagged_sel], dtype=np.int32)            #: Tagging decisions != 0 for selected events
        self.dec_flav   = pd.Series(self.all_B_ID[self.tagged_sel], dtype=np.int32) // absid  #: B meson ids for tagged and selected candidates
        self.prod_flav  = self.dec_flav.copy(deep=True)  #: Production flavour estimate
        self.eta        = pd.Series(self.all_eta[self.tagged_sel])  #: Mistag of tagged and selected candidates
        self.avg_eta    = np.mean(self.eta)  #: mean mistag of selected tagged events

        self.N   = len(self.all_eta)      #: Number of events
        self.Ns  = self.selected.sum()    #: Number of selected events
        self.Nt  = self.tagged.sum()      #: Number of tagged events
        self.Nts = self.tagged_sel.sum()  #: Number of selected and tagged events

        # Set weights to 1 if not defined
        if weights is None:
            self.weights = pd.Series(np.ones(self.Nts))
        else:
            raise_error(len(weights) == self.N, "Tagging data must have matching dimensions")
            self.weights = pd.Series(weights)[self.tagged & self.selected].copy(deep=True)
        self.weights.index = self.dec.index

        self.all_weights = pd.Series(weights) if weights is not None else np.ones(self.N)
        self.Nw          = np.sum(self.all_weights)                  #: Weighted number of all events
        self.Neff        = self.Nw**2 / np.sum(self.all_weights**2)  #: Effective number of all events ((sum w)^2/(sum(w^2)))
        self.Nwt         = np.sum(self.all_weights[self.tagged])     #: Weighted number of all tagged events

        self.Nws         = np.sum(self.all_weights[self.selected])                   #: Weighted number of selected events
        self.Neffs       = self.Nws**2 / np.sum(self.all_weights[self.selected]**2)  #: Effective number selected events
        self.Nwts        = np.sum(self.weights)                                      #: Weighted number of selected and tagged events

        self.correct_tags = self.dec == self.prod_flav  #: Tag corresponds to production flavour (for selected events)
        self.wrong_tags   = ~self.correct_tags          #: Tag does not correspond to production flavour (for selected events)

        raise_error(self.Nt > 0 and self.Nts > 0 and self.Ns > 0, "No events left after cut :(")

    def __str__(self):
        return ("Tagging Statistics\n"
                f"N  = {self.N}\n"
                f"Nw = {self.Nw}\n"
                f"Nt = {self.Nt}\n"
                f"Nwt = {self.Nwt}\n"
                f"Ns  = {self.Ns}\n"
                f"Nws = {self.Nws}\n"
                f"Nts = {self.Nts}\n"
                f"Nwts = {self.Nwts}")

    def __eq__(self, other):
        """ return true if data of two TaggingData objects is identical.
            Needed for unit testing
        """
        equal = True
        equal &= self.all_eta.equals(other.all_eta)
        equal &= self.all_dec.equals(other.all_dec)
        equal &= self.all_B_ID.equals(other.all_B_ID)
        equal &= self.tagged.equals(other.tagged)
        equal &= self.dec.equals(other.dec)
        equal &= self.dec_flav.equals(other.dec_flav)
        equal &= self.prod_flav.equals(other.prod_flav)
        equal &= self.eta.equals(other.eta)
        equal &= self.avg_eta == other.avg_eta
        equal &= self.weights.equals(other.weights)
        equal &= self.all_weights.equals(other.all_weights)
        equal &= self.correct_tags.equals(other.correct_tags)
        equal &= self.wrong_tags.equals(other.wrong_tags)

        equal &= self.N     == other.N
        equal &= self.Nt    == other.Nt
        equal &= self.Nw    == other.Nw
        equal &= self.Neff  == other.Neff
        equal &= self.Nwt   == other.Nwt
        equal &= self.Ns    == other.Ns
        equal &= self.Nts   == other.Nts
        equal &= self.Nws   == other.Nws
        equal &= self.Neffs == other.Neffs
        equal &= self.Nwts  == other.Nwts
        return equal


class BasicTaggingData:
    r"""
    BasicTaggingData
    Type for keeping track of tagging data and basic event statistics of a tagger without knowledge
    about the true prodcution flavour. Used to descibe a Tagger in a target dataset

    :param eta_data: Uncalibrated mistags
    :type eta_data: list
    :param dec_data: Uncalibrated tagging decisions
    :type dec_data: list
    :param weights: Per-event weights
    :type weights: list
    :param ignore_out_of_range: Whether to ignore mistag values :math:`\eta\notin [0,0.5]` (not recommended)
    :type ignore_out_of_range: bool
    """
    def __init__(self, eta_data, dec_data, weights, ignore_eta_out_of_range=False):
        self.all_eta   = pd.Series(eta_data)  #: All eta values
        self.all_dec   = pd.Series(dec_data)  #: All dec values

        if not ignore_eta_out_of_range:
            self.overflow  = (self.all_eta > 0.5)  #: Mask of events with :math:`\omega>0.5`
            self.underflow = (self.all_eta < 0)    #: Mask of events with :math:`\omega<0`
            self.noverflow = self.overflow.sum()   #: Number of calibrated mistags > 0.5

            self.all_eta[self.overflow] = 0.5
            self.all_eta[self.underflow] = 0
            self.all_dec[self.overflow] = 0

        self.tagged    = self.all_dec != 0    #: Mask of tagged events
        self.dec       = pd.Series(self.all_dec[self.tagged], dtype=np.int32)           #: Tagging decisions != 0
        self.eta       = pd.Series(self.all_eta[self.tagged])  #: Mistag of tagged candidates

        self.N  = len(self.all_eta)  #: Number of events
        self.Nt = self.tagged.sum()  #: Number of tagged events

        # Set weights to 1 if not defined
        if weights is None:
            self.weights = pd.Series(np.ones(self.Nt))
        else:
            raise_error(len(weights) == self.N, "Tagging data must have matching dimensions")
            self.weights = pd.Series(weights)[self.tagged].copy(deep=True)
        self.weights.index = self.dec.index

        self.all_weights = pd.Series(weights) if weights is not None else np.ones(self.N)
        self.Nw          = np.sum(self.all_weights)  #: Weighted number of events
        self.Neff        = self.Nw**2 / np.sum(self.all_weights**2)  #: Effective number of total events
        self.Nwt         = np.sum(self.weights)   #: Weighted number of tagged events


