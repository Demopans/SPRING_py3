#!/usr/bin/env python3
import os

from get_stdin_data import get_stdin_data

data, running_cgi = get_stdin_data()


cwd = os.getcwd()
if cwd.endswith('cgi-bin'):
    os.chdir('../')


filepath = data.get('path')
content = data.get('content')

if filepath.endswith('coordinates.txt'):
	if os.path.exists(filepath):
		import datetime
		dt = datetime.datetime.now().isoformat().replace(':','-').split('.')[0]
		backup = filepath.replace('coordinates.txt','coordinates_'+dt+'.txt')
		open(backup,'w').write(open(filepath).read())

open(filepath,'w').write(content)
if 'clustering_data' in filepath: 
	os.system('cp '+filepath+' '+filepath.replace('_clustmp',''))
	os.system('rm -f '+filepath)

if running_cgi:
	print("Content-Type: text/html\n")
print('sucess')
