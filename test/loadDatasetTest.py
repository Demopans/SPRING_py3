import sys, os, pandas as pd
from data_prep.helper_functions import *
from pathlib import Path

sys.path.append("../cgi-bin")
sys.path.append("../cgi-bin/lib")
from dotdot import DotDot
from file import getDataset,loadDataset

if __name__ == '__main__':
    # set working directory
    os.chdir('../')
    # create mini set
    a = getDataset('XA23_s10','PGCs')