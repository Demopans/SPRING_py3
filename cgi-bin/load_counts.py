#!/usr/bin/env python3
import os

from get_stdin_data import get_stdin_data

data, running_cgi = get_stdin_data()

cwd = os.getcwd()
if cwd.endswith('cgi-bin'):
    os.chdir('../')

base_dir = data.get('base_dir')
gene_list = [l.strip('\n') for l in open(base_dir + '/genes.txt')]

if running_cgi:
    print("Content-Type: text/plain")
    print()

for g in gene_list:
    print(g)
