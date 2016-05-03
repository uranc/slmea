"""
Inverse optimizer example
"""
# Author: Cem Uran <cem.uran@uranus.uni-freiburg.de>
# License:
from setData import data_in
from setInvProb import data_out
from setOptProb import opt_out
from setVisualization import visualize
import casadi as ca
import numpy as np
import matplotlib.pyplot as plt
import pickle as pc
import time
import sys
import getopt


# Data path/filename
t_ind = 38
data_path = '../data/'
file_name = data_path + 'data_sim_low.hdf5'

data_options = {'flag_cell': True, 'flag_electode': False}
data = data_in(file_name, **data_options)

# Inverse solution
# localization_options = {'p_vres':20, 'p_jlen':0, 'p_erad': 5, 't_ind': 38, 'flag_depthweighted': False}
# loc = data_out(data, **localization_options)

# loc.cmp_sloreta()
# loc.xres = loc.res[:, t_ind]
# ccell = loc.evaluate_localization()

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
opts, args = getopt.getopt(sys.argv[1:], "s:h:l:m:n:p:d:")  # sol:hes:norm:sp:dyn:")
for opt, arg in opts:
    if opt in ("-m"):
        p_method = arg 
    elif opt in ("-s"):
        p_solver = arg 
    elif opt in ("-h"):
        p_hessian = arg 
    elif opt in ("-n"):
        p_norm = arg 
    elif opt in ("-p"):
        p_sparse = arg 
    elif opt in ("-d"):
        p_dynamic = arg 
    elif opt in ("-l"):
        p_linsol = arg 

print 'Method is ', p_method
print 'NLP Solver is ', p_solver
print 'Linear Solver is ', p_linsol
print 'Hessian is ', p_hessian
print 'Norm is ', bool(int(p_norm))
print 'Sparsity is ', float(p_sparse)
print 'Dynamics bound is ', float(p_dynamic)

#python -i runDebug.py -m mask -s ipopt -p 0 -d 50 -n 1 -h limited-memory -l mums

# Optimize
optimization_options = {'p_vres':10, 'p_jlen':0, 'p_erad': 5,
                        'solver': p_solver,
                        'hessian': p_hessian,
                        'linsol': p_linsol,
                        't_ind': 30, 't_int': 1, 
                        'sigma': float(p_sparse),
                        'flag_depthweighted': bool(int(p_norm)),
                        'flag_parallel': False,
                        'datafile_name': 'output_file',
                        'flag_lift_mask': False,
                        'p_dyn': float(p_dynamic)
                        }
opt = opt_out(data, **optimization_options)
if p_method == 'thesis':
	opt.solve_ipopt_multi_measurement_thesis()
elif p_method == 'mask':
	opt.solve_ipopt_multi_measurement_only_mask()

# opt.solve_ipopt_multi_measurement_slack()
# opt.solve_ipopt_multi_measurement_2p()

# visualize
# vis = visualize(data=data, loc=opt)
# vis.show_snapshot()

# opt.set_optimization_variables_slack()
# opt.w0 = opt.w(1)
# opt.res = opt.w0['x']
# opt.xres = opt.w0['x']


# aa = []
# for i in range(opt.data.electrode_rec.shape[1]):
# 	    aa.append(sum(opt.data.cell_csd[ind_cell,i])/ sum(opt.data.electrode_rec[:,i]))
