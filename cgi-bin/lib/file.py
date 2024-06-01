import json, pandas as pd, os
from pathlib import Path

ROOTDIR = 'datasets'


def getDataset(dataset: str, opt: str) -> dict[str, str | Path]:
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
        'meta': f'{dataset}/{opt}',
        'lbl': Path(f'{ROOTDIR}/{dataset}/cell_labels.txt'),
        'genes': Path(f'{ROOTDIR}/{dataset}/genes.txt'),
        'data': Path(f'{ROOTDIR}/{dataset}/counts_norm.npz'),
        'opt': Path(f'{ROOTDIR}/{dataset}/{opt}/cell_filter.txt')
    }


def loadDataset(dataset: str, opt: str):
    """
    Loads dataset, hits cache first if possible
    """
    import scanpy, pandas as pd
    from scanpy import AnnData
    from scipy.sparse import csr_matrix
    # load functions needed for io ops from spaghetti
    from ..doublet_helper import load_npz
    # in cache? Guarrented to be valid if it is the case
    if Path(f'cache/{dataset}/{opt}.adata').is_file():
        pass
    ref: dict[str, str | Path] = getDataset(dataset, opt)

    data = load_npz(ref['data'])

    scanpy.pl.dotplot
