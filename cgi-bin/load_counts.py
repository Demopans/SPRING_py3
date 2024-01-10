#!/usr/bin/env python3
import os
import urllib.parse
import sys

cwd = os.getcwd()
if cwd.endswith('cgi-bin'):
    os.chdir('../')

reqstr = ''.join(sys.stdin)
data = urllib.parse.parse_qs(reqstr, keep_blank_values=True)

base_dir = data.get('base_dir')[0]
gene_list = [l.strip('\n') for l in open(base_dir + '/genes.txt')]

print("Content-Type: text/plain")
print()
for g in gene_list:
    print(g)
