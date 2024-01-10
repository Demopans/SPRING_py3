#!/usr/bin/env python3
import cgi
import os

cwd = os.getcwd()
if cwd.endswith('cgi-bin'):
    os.chdir('../')

data = cgi.FieldStorage()
base_dir = data.getvalue('base_dir')
gene_list = [l.strip('\n') for l in open(base_dir + '/genes.txt')]

print("Content-Type: text/plain")
print()
for g in gene_list:
    print(g)
