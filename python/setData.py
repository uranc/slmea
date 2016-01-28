"""
Module for loading data from various files
"""
# Author: Cem Uran <cem.uran@uranus.uni-freiburg.de>
# License:
import h5py


class data_in(object):
    """
    Data class loaded from file
    ---------
    Arguments
    ---------
    f_name - filename
    flag_cell - flag cell morphology information  #ASSUME TRUE
    ---------
    Attributes
    ---------
    srate
    flag_pre
    data
    ---------
    Functions
    ---------
    """
    def __init__(self, *args, **kwargs):
        self.f_name = args[0]
        self.flag_cell = kwargs.get('flag_cell')
        print args, kwargs
        print self.f_name
        print self.flag_cell
        if self.flag_cell:
            (self.cell_pos, self.cell_csd, self.electrode_pos,
                self.electrode_rec, self.srate) = self.load_h5py_data(
                self.f_name, self.flag_cell)
        else:
            self.data_raw, self.srate = self.load_h5py_data(self.f_name,
                                                            self.flag_cell)

    def load_h5py_data(self, f_name, flag_cell):
        """
        load h5py data
        optionally cell and electrode positions
        """
        f = h5py.File(self.f_name, 'r')
        print "Cell data avaliable"
        if flag_cell:
            return (f['cell'][:, 0:3], f['cell'][:, 3:],
                    f['electrode'][:, 0:3], f['electrode'][:, 3:],
                    f['srate'][()])
        else:
            return f['data'][:], f['srate'][()]
    # def high_pass_data():
    # def car_data():
    # def epoch_data():
    # def cmp_cov_source():
    # def cmp_cov_meas():
