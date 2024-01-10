#!/usr/bin/env python3
import os
import sys
import io
import urllib.parse


def get_stdin_data(make_like_cgi=True):
  totalBytes = int(os.environ.get('CONTENT_LENGTH', 0))
  running_cgi = totalBytes > 0

  if running_cgi:
    reqbin = io.open(sys.stdin.fileno(), "rb").read(totalBytes)
    reqstr = reqbin.decode("utf-8")
  else:
    reqstr = ''.join(sys.stdin)

  data = urllib.parse.parse_qs(reqstr, keep_blank_values=True)

  if make_like_cgi:
    # only use the first argument from the lists, treat empty as None
    for key in data.keys():
      data[key] = data[key][0]
      if data[key] == "":
        data[key] = None

  return (data, running_cgi)
