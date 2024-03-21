#!/usr/bin/env python3
import os

from shutil import move
from get_stdin_data import get_stdin_data, dir_exists

form, running_cgi = get_stdin_data()

if running_cgi:
    print("Content-Type: text/html")
    print()

base_dir = form.get_required_dir('base_dir')
sub_dir = form.get_required('sub_dir')

archive_path = os.path.join(base_dir, 'archive')
if not dir_exists(archive_path):
	os.system('mkdir '+archive_path)

move(os.path.join(base_dir, sub_dir), os.path.join(archive_path, sub_dir))
