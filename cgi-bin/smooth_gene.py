#!/usr/bin/env python3

import time
import os

from get_stdin_data import get_stdin_data

data, running_cgi = get_stdin_data()

cwd = os.getcwd()
if cwd.endswith('cgi-bin'):
    os.chdir('../')
	
t00 = time.time()
def update_log(fname, logdat, overwrite=False):
	if overwrite:
		o = open(fname, 'w')
	else:
		o = open(fname, 'a')
	o.write(logdat + '\n')
	o.close()

def strfloat(x):
    if x == 0: return "0"
    else: return "%.1f" %x


def sparse_multiply(E, a):
    nrow = E.shape[0]
    w = ssp.lil_matrix((nrow, nrow))
    w.setdiag(a)
    return w * E

logf = 'tmplog2'

t0 = time.time()
import numpy as np
t1 = time.time()
update_log(logf, 'import numpy -- %.3f' %(t1-t0))

t0 = time.time()
import scipy.sparse as ssp
t1 = time.time()
update_log(logf, 'import scipy sparse -- %.3f' %(t1-t0))

if running_cgi:
	print("Content-Type: text/plain")
	print()

t0 = time.time()
base_dir = data.get('base_dir')
sub_dir = data.get('sub_dir')
reds = np.array(list(map(float, data.get('raw_r').split(','))))[:, None]
greens = np.array(list(map(float, data.get('raw_g').split(','))))[:, None]
blues = np.array(list(map(float, data.get('raw_b').split(','))))[:, None]
E = np.hstack((reds, greens, blues))
# E = np.array(map(float, data.get('raw_g').split(',')))[:,None]

sel = data.get('selected')[1:]
print(sel)
if len(sel)==0: 
	sel = np.arange(E.shape[0])
else: 
	sel = np.array(list(map(int, sel.split(','))),dtype=int)
	E = E[sel,:]


beta = float(data.get('beta'))
n_rounds = int(data.get('n_rounds'))
t1 = time.time()
update_log(logf, 'got cgi data -- %.3f' %(t1-t0))

##### SMOOTH

t0 = time.time()
try:
	A = ssp.load_npz(sub_dir + '/A.npz')
except:
	cell_filter =  np.load(sub_dir + '/' + 'cell_filter.npy')
	edges = np.loadtxt(sub_dir + '/edges.csv', delimiter=';', comments=None)
	A = ssp.lil_matrix((len(cell_filter), len(cell_filter)))
	for iEdge in range(edges.shape[0]):
		ii = edges[iEdge, 0]
		jj = edges[iEdge, 1]
		A[ii, jj] = 1
		A[jj, ii] = 1
	A = A.tocsc()
	ssp.save_npz(sub_dir + '/A.npz', A)
	
t1 = time.time()
update_log(logf, 'loaded adjacency matrix -- %.3f' %(t1-t0))

###########
t0 = time.time()
A = A[:,sel].tocsr()[sel,:].tocsc()
A = sparse_multiply(A, 1 / A.sum(1).A.squeeze())
for iRound in range(n_rounds):
	E = (beta * E + ((1 - beta) * A) * E)


t1 = time.time()
update_log(logf, 'smoothed data -- %.3f' %(t1-t0))

###########
# E = np.floor(E)
# E = np.array(E, dtype=int)

t0 = time.time()

print(repr(np.min(E))+'|'+repr(np.max(E))+'|' +';'.join([','.join(map(str,E[:,0])), ','.join(map(str,E[:,1])), ','.join(map(str,E[:,2]))]))
t1 = time.time()
update_log(logf, 'returned data -- %.3f' %(t1-t0))

t11 = time.time()
update_log(logf, str(t11-t00))
