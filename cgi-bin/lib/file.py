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
        return {'error': 'Invalid directory'}

    # load raw cell data and pred labels (if any)
    filt: bool
    if not (list(root.glob('cell_labels.txt'))[0].is_file() and
            list(root.glob('counts_norm.npz'))[0].is_file() and
            list(root.glob('genes.txt'))[0].is_file() and
            list(option.glob('cell_filter.txt'))[0].is_file()):
        return {'error': 'incomplete dataset'}

    # return set of references
    return {
        'lbl': Path(f'{ROOTDIR}/{dataset}/cell_labels.txt'),
        'genes': Path(f'{ROOTDIR}/{dataset}/genes.txt'),
        'data': Path(f'{ROOTDIR}/{dataset}/counts_norm.npz'),
        'opt': Path(f'{ROOTDIR}/{dataset}/{opt}/cell_filter.txt')
    }


def loadDataset(ref: dict):
    # loads dataset using reference dict, only for internal use as work is intended to be offloaded to the client
    pass
