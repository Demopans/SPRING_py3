#!/usr/bin/env python3
import os
import sys
import scipy.sparse as ssp
import numpy as np
import json
import time
from wolkit import *
import pickle
import datetime

from get_stdin_data import validate_dir_path_exists

creation_time = datetime.datetime.now()

t00 = time.time()

def sparse_var(E, axis=0):
    mean_gene = E.mean(axis=axis).A.squeeze()
    tmp = E.copy()
    tmp.data **= 2
    return tmp.mean(axis=axis).A.squeeze() - mean_gene ** 2

def update_log_html(fname, logdat, overwrite=False):
	if overwrite:
		o = open(fname, 'w')
	else:
		o = open(fname, 'a')
	o.write(logdat + '<br>\n')
	o.close()

def update_log(fname, logdat, overwrite=False):
	if overwrite:
		o = open(fname, 'w')
	else:
		o = open(fname, 'a')
	o.write(logdat + '\n')
	o.close()

def send_confirmation_email(user_email, subset_name, path):

    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText

    fromaddr = "singlecellspring@gmail.com"
    toaddr = user_email
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = 'Your download "%s" is ready' %subset_name

    body = 'Download data here:\n' + path + '\n'
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "Sequencing1")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

#######################
# Load parameters
params_dict = pickle.load(open(sys.argv[1], 'rb'))

extra_filter = params_dict['extra_filter']
base_dir = validate_dir_path_exists(params_dict['base_dir'])
current_dir = params_dict['current_dir']
user_email = params_dict['user_email']
rand_suffix = params_dict['rand_suffix']
selection_name = params_dict['selection_name']
my_url_origin = params_dict['my_url_origin']


#outdir = current_dir + '/selected_downloads/tmp_download_' + rand_suffix + '/'
outdir = os.path.join(base_dir, current_dir, "downloads",
                      selection_name + '.' + rand_suffix)
#os.makedirs(outdir)

# logf = outdir + 'logdownloadselect.txt'
# timef = outdir + 'logdownloadselecttime.txt'

#######################
# Load data

cell_filter = np.load(os.path.join(base_dir, current_dir, 'cell_filter.npy'))[
    extra_filter]
gene_list = np.loadtxt(os.path.join(base_dir, 'genes.txt'), dtype=str,
                       delimiter='\t', comments=None)

t0 = time.time()
# update_log_html(logf, 'Loading counts data...', True)
E = ssp.load_npz(os.path.join(base_dir, 'counts_norm.npz'))
E = E[cell_filter,:]
if not ssp.isspmatrix_csc(E):
    E = E.tocsc()
t1 = time.time()
# update_log(timef, 'Counts loaded from npz -- %.2f' %(t1-t0), True)
print(E.shape)
print(gene_list.shape)

E = E.T

print(E.shape)


#################
# Save expression matrix as csv
print('Saving expression')
o = open(os.path.join(outdir, 'expr.csv'), 'w')
t0 = time.time()
for iG, g in enumerate(gene_list):
    if iG % 500 == 0:
        t1 = time.time()
        #update_log(timef, 'Gene %i -- %.2f' %(iG + 1, t1-t0))
        t0 = time.time()
    counts = E[iG,:].A.squeeze()
    o.write(g + ',' + ','.join(map(str, counts)) + '\n')

o.close()
os.system('gzip "' + os.path.join(outdir, 'expr.csv') + '"')


# save coordinates
print('Saving coordinates')
coords = np.loadtxt(os.path.join(base_dir, current_dir, 'coordinates.txt'),
                    delimiter=',', comments=None)[:, 1:]
coords = coords[extra_filter,:]
np.savetxt(os.path.join(outdir, 'coordinates.csv'), np.hstack(
    (np.arange(coords.shape[0])[:, None], coords)), fmt="%i,%.5f,%.5f")

# save original cell indices of selected cells
print('Saving cell indices')
np.savetxt(os.path.join(outdir, 'original_cell_indices.txt'),
           cell_filter, fmt='%i')

# save extra categorical variables
print('Saving categorical data')
categ = json.load(
    open(os.path.join(base_dir, current_dir, 'categorical_coloring_data.json')))
o = open(os.path.join(outdir, 'cell_groupings.csv'), 'w')
for k in categ:
    v = categ[k]['label_list']
    v_filt = [v[i] for i in extra_filter]
    o.write(k + ',' + ','.join(map(str, v_filt)) + '\n')
o.close()

# save extra continuous variables
print('Saving continuous data')
o = open(os.path.join(outdir, 'custom_colors.csv'), 'w')
with open(os.path.join(base_dir, current_dir, 'color_data_gene_sets.csv')) as f:
    for l in f:
        cols = l.strip('\n').split(',')
        varname = cols[0]
        varvals = cols[1:]
        varvals_filt = [varvals[i] for i in extra_filter]
        o.write(varname + ',' + ','.join(varvals_filt) + '\n')

o.close()


####################
tar_name = outdir + '.tar.gz'
os.system('tar cfz "' + tar_name + '" "' + outdir + '"')

send_confirmation_email(user_email, selection_name,
                        my_url_origin + '/' + tar_name)
