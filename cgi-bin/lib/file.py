import json, pandas as pd, os
from pathlib import Path

ROOTDIR = 'datasets'

def getDataset(dataset: str, opt: str) -> dict:
    """
    Loads dataset root directory. returns error dict if directory is invalid
    Returns dict of loadable references otherwise
    """
    root, option = Path(f'{ROOTDIR}/{dataset}'), Path(f'{ROOTDIR}/{dataset}/{opt}')
    if option.parent != root:
        # possible it exists in cache, but if it's deleted from the dataset root, we probably don't need it
        return {'error': 'Invalid directory'}

    # check if exists in cache
    # later
    
    # load raw cell data and pred labels (if any)
    dataset: bool
    genes: bool
    lbl: bool
    filt: bool
    data = {
        'cellLabels':"",
    }

def loadDataset(ref: dict):
    # loads dataset using reference dict, only for internal use as work is intended to be offloaded to the client
    pass
    