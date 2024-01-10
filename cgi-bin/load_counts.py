#!/usr/bin/env python3
import cgi
import os
import io
import urllib.parse
import sys

cwd = os.getcwd()
if cwd.endswith('cgi-bin'):
    os.chdir('../')

print("test")

totalBytes = int(os.environ.get('CONTENT_LENGTH', 0))
reqbin = io.open(sys.stdin.fileno(), "rb").read(totalBytes)
reqstr = reqbin.decode("utf-8")
data = urllib.parse.parse_qs(reqstr, keep_blank_values=True)
print(data)

# # data = cgi.FieldStorage()
# base_dir = data.get('base_dir')[0]
# print(base_dir)
# gene_list = [l.strip('\n') for l in open(base_dir + '/genes.txt')]

# print("Content-Type: text/plain")
# print()
# for g in gene_list:
#     print(g)
