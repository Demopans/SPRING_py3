#!/usr/bin/env python3
import os
import sys
import io
import urllib.parse

this_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(this_dir)


# Check that the given path leads to an existing directory
def dir_exists(path: str) -> bool:
  return os.path.exists(path) and os.path.isdir(path)


# Check if given path leads to existing directory (including in this script's
# parent directory). If it does, return path which exists. Otherwise errors out.
def validate_dir_path_exists(path: str) -> str:
  if dir_exists(path):
    return path
  _path = os.path.join(parent_dir, path)
  if dir_exists(_path):
    return _path
  raise RuntimeError(f"Unable to validate path exists as dir: {path}")


def validate_path_exists(path: str) -> str:
  if os.path.exists(path):
    return path
  _path = os.path.join(parent_dir, path)
  if os.path.exists(_path):
    return _path
  raise RuntimeError(f"Unable to validate path exists: {path}")


class stdin_data(dict[str, str]):
  def get_required(self, key: str) -> str:
    val = self.get(key)
    if val is None:
      raise RuntimeError(f"Unable to find value for required key: {key}")
    return val

  def get_required_dir(self, key: str) -> str:
    path = self.get_required(key)
    return validate_dir_path_exists(path)

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

  output: stdin_data = stdin_data()
  for key in data.keys():
    output[key] = data[key][0]

  return (output, running_cgi)
