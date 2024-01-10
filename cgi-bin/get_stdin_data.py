#!/usr/bin/env python3
import os
import sys
import io
import urllib.parse


def get_stdin_data():
  totalBytes = int(os.environ.get('CONTENT_LENGTH', 0))
  running_cgi = totalBytes > 0

  if running_cgi:
    reqbin = io.open(sys.stdin.fileno(), "rb").read(totalBytes)
    reqstr = reqbin.decode("utf-8")
  else:
    reqstr = ''.join(sys.stdin)

  data: dict[str, list[str]] = urllib.parse.parse_qs(
      reqstr, keep_blank_values=True)

  output: dict[str, str] = {}
  for key in data.keys():
    output[key] = data[key][0]

  return (output, running_cgi)
