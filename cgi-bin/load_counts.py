#!/usr/bin/env python3
import os

from get_stdin_data import get_stdin_data

data, running_cgi = get_stdin_data()

this_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(this_directory)

base_dir = data.get('base_dir', '')
base_dir = os.path.join(parent_directory, base_dir)

genes_path = os.path.join(base_dir, 'genes.txt')

gene_list = [l.strip('\n') for l in open(genes_path)]

if running_cgi:
    print("Content-Type: text/plain")
    print()

for g in gene_list:
    print(g)
