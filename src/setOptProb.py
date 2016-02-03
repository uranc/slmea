"""
Create attributes for the optimization problem
"""
# Author: Cem Uran <cem.uran@uranus.uni-freiburg.de>
# License:
from setInvProb import data_out
import casadi as ca


class opt_out(data_out):
    """
    Class for the optimization problem
    Child of inverse problem
    """
    def __init__(self, *args, **kwargs):
        data_out.__init__(self, *args, **kwargs)

    @ca.pycallback
    def plot_updates(self, f):
        """
        Gets inter-optimization plots
        """
        x = f.getOutput('x')
        self.plot_data(x)
        return 0
