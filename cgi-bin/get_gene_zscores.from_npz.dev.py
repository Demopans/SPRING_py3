#!/usr/bin/env python3
import scipy.sparse as ssp
import numpy as np
import json
import time
import os

from get_stdin_data import get_stdin_data

data, running_cgi = get_stdin_data()

def update_log(fname, logdat, overwrite=False):
	if overwrite:
		o = open(fname, 'w')
	else:
		o = open(fname, 'a')
	o.write(logdat + '\n')
	o.close()

def strfloat(x):
    return "%.3f" %x


base_dir = data.get_required_dir('base_dir')
sub_dir = data.get_required_dir('sub_dir')
sel_filter = data.get('selected_cells')
comp_filter = data.get('compared_cells')

logf = os.path.join(sub_dir, 'tmplogenrich')
update_log(logf, 'Enrichment log:', True)

gene_list = np.loadtxt(os.path.join(base_dir, 'genes.txt'), dtype=str,
                       delimiter='\t', comments=None)

if str(sel_filter) != "None":
    sel_filter = np.sort(np.array(list(map(int,sel_filter.split(',')))))
else:
    sel_filter = []
    sel_scores = np.zeros(len(gene_list), dtype=float)

if str(comp_filter) != "None":
    comp_filter = np.sort(np.array(list(map(int,comp_filter.split(',')))))
else:
    comp_filter = []
    comp_scores = np.zeros(len(gene_list), dtype=float)

update_log(logf, '%i selected cells; %i compared cells' %(len(sel_filter), len(comp_filter)), False)

t0 = time.time()
color_stats = json.load(open(os.path.join(sub_dir, 'color_stats.json'), 'r'))
t1 = time.time()
update_log(logf, 'got color stats -- %.3f' %(t1-t0))

t0 = time.time()
E = ssp.load_npz(os.path.join(base_dir, 'counts_norm.npz'))
t1 = time.time()
update_log(logf, 'loaded npz -- %.3f' %(t1-t0))

t0 = time.time()
cell_filter = np.load(os.path.join(sub_dir, 'cell_filter.npy'))
t1 = time.time()
update_log(logf, 'got cell filter -- %.3f' %(t1-t0))

if len(sel_filter) > 0:
    cell_filter_use = cell_filter[sel_filter]

    t0 = time.time()
    all_means = E[cell_filter_use,:].mean(0).A.squeeze()
    t1 = time.time()
    update_log(logf, 'got means -- %.3f' %(t1-t0))

    t0 = time.time()
    sel_scores = np.zeros(len(gene_list), dtype=float)
    for iG, g in enumerate(gene_list):
        m = color_stats[g][0]
        s = color_stats[g][1]
        sel_scores[iG] = (all_means[iG] - m) / (s+0.02)
    t1 = time.time()
    update_log(logf, 'got selected scores -- %.3f' %(t1-t0))

if len(comp_filter) > 0:
    cell_filter_use = cell_filter[comp_filter]

    t0 = time.time()
    all_means = E[cell_filter_use,:].mean(0).A.squeeze()
    t1 = time.time()
    update_log(logf, 'got means -- %.3f' %(t1-t0))

    t0 = time.time()
    comp_scores = np.zeros(len(gene_list), dtype=float)
    for iG, g in enumerate(gene_list):
        m = color_stats[g][0]
        s = color_stats[g][1]
        comp_scores[iG] = (all_means[iG] - m) / (s+0.02)
    t1 = time.time()
    update_log(logf, 'got compared scores -- %.3f' %(t1-t0))

scores = sel_scores - comp_scores

t0 = time.time()
o = np.argsort(-scores)[:1000]
t1 = time.time()
update_log(logf, 'sorted scores -- %.3f' %(t1-t0))
t0 = time.time()
gene_list = gene_list[o]
scores = scores[o]
t1 = time.time()
update_log(logf, 'filtered lists -- %.3f' %(t1-t0))

if running_cgi:
    print("Content-Type: text/plain")
    print()

print('\n'.join(gene_list) + '\t' + '\n'.join(map(strfloat,scores)))
