import os
from pathlib import Path

"""
currently a test file relating to forming a dataset from jumbo
"""

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
        'lbl': Path(f'{ROOTDIR}/{dataset}/cell_labels.txt'),       #
        'genes': Path(f'{ROOTDIR}/{dataset}/genes.txt'),           #
        'data': Path(f'{ROOTDIR}/{dataset}/counts_norm.npz'),      #
        'expr': Path(f'{ROOTDIR}/{dataset}/expr.raw.npz'),         #
        'opt': Path(f'{ROOTDIR}/{dataset}/{opt}/cell_filter.txt')  # picks out the entries
    }


def loadDataset(dataset: str, opt: str):
    """
    Loads dataset, hits cache first if possible
    """
    import scanpy, pandas as pd, sys, numpy as np
    from scanpy import AnnData
    from scipy.sparse import csr_matrix, load_npz
    # in cache? Guarrented to be valid if it is the case
    if Path(f'cache/{dataset}/{opt}.adata').is_file():
        pass
    ref: dict[str, str | Path] = getDataset(dataset, opt)

    # create Annotated dataset
    data = AnnData(
        X=load_npz(ref['data']).tocsc(),
        var=np.loadtxt(ref['genes'], dtype=str, delimiter='\t', comments=None)
    )
    filter = pd.read_csv(ref['opt'])

    s = load_npz(ref['expr'])
    d = pd.read_csv(ref['lbl'],header=0, index_col=0)

    # filter then stitch
    data = data[filter.values]
    s = s[filter.T.values[0]]
    d = d.iloc[:,filter.T.values[0]]


    scanpy.pl.dotplot
