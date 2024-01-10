#!/usr/bin/env python3
import os
import json

from get_stdin_data import get_stdin_data

data, running_cgi = get_stdin_data()


cwd = os.getcwd()
if cwd.endswith('cgi-bin'):
    os.chdir('../')


def check_same(d1,d2):
	out = True
	for k,v in list(d1.items()):
		if not k in d2 or d2[k] != v: out = False
	return out


filepath = data.get('path')
content = data.get('content')
if os.path.exists(filepath):
	old_data = json.load(open(filepath))
	new_data = json.loads(content)
	for d in new_data:
		already_exists = False
		for dd in old_data:
			if check_same(d,dd): already_exists = True
		if not already_exists:
			old_data.append(d)
	content = json.dumps(old_data)

open(filepath,'w').write(content)

if running_cgi:
	print("Content-Type: text/html\n")
print('sucess')
