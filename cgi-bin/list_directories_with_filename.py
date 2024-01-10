#!/usr/bin/env python3
import os

from get_stdin_data import get_stdin_data

data, running_cgi = get_stdin_data()

cwd = os.getcwd()
if cwd.endswith('cgi-bin'):
    os.chdir('../')


if running_cgi:
	print("Content-Type: text/html")
	print()


path = data.get('path')
filename = data.get('filename')
out = []
for f in os.listdir(path):
	if os.path.exists(path+'/'+f+'/'+filename):
		out.append(f)
print(','.join(sorted(out,key=lambda x: x.lower())))
