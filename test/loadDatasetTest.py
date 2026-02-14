import sys, os, pandas as pd
from data_prep.helper_functions import *
from src.lib.dataset import getDataset, loadDataset

if __name__ == '__main__':
    # set working directory
    os.chdir('../')
    # check dict
    a = getDataset('XA23_s10','PGCs')
    a
    # check output
    a = loadDataset('XA23_s10','PGCs')
    a