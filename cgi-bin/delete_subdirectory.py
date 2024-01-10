#!/usr/bin/env python3
import os

from get_stdin_data import get_stdin_data

form, running_cgi = get_stdin_data()

cwd = os.getcwd()
if cwd.endswith('cgi-bin'):
    os.chdir('../')

if running_cgi:
    print("Content-Type: text/html")
    print()

# Get filename here.
proj_dir = form.get('base_dir').strip('\n')
sub_dir = form.get('sub_dir').strip('\n')

if not os.path.exists(proj_dir+'/archive'):
	os.system('mkdir '+proj_dir+'/archive')

from shutil import move
move(proj_dir + '/' + sub_dir, proj_dir + '/archive/' + sub_dir)




