"""
Inverse optimizer example
"""
# Author: Cem Uran <cem.uran@uranus.uni-freiburg.de>
# License:

from setData import data_in
from setOptProb import opt_out
import casadi as ca
# Data path/filename
data_path = '../data/'
file_name = data_path + 'data_sim_low.hdf5'
print "Looking for file" + file_name
data = data_in(file_name, flag_cell=True, flag_electode=False)
opt = opt_out(data.electrode_pos, p_vres=20, p_jlen=0)
fwd = ca.SX(opt.cmp_fwd_matrix(opt.electrode_pos, opt.voxels))

t_ind = 30
t_interval = 1

# Multi frame
y = ca.SX(data.electrode_rec[:, t_ind:t_ind+t_interval])
x = ca.SX.sym('x', fwd.shape[1], y.shape[1])
print y.shape, x.shape, fwd.shape
# Parameters

# Function value
f = ca.norm_1(x)
g = (y-ca.mul(fwd, x))**2
# Initialize
x0 = [0]
lbx = [-100]
ubx = [100]
lbg = [0]
ubg = [1e-5]
# Nonlinear bounds

# Create NLP
nlp = ca.SXFunction("nlp", ca.nlpIn(x=x), ca.nlpOut(f=f, g=g))

# NLP solver options
opts = {"max_iter": 10000}
# opts["compute_red_hessian"] = "yes"
# Create NLP solver
solver = ca.NlpSolver("solver", "ipopt", nlp, opts)
# Solve NLP
res = solver({"x0": x0,
              "lbx": lbx,
              "ubx": ubx,
              "lbg": lbg,
              "ubg": ubg})
