import sys, json, pandas as pd, pathlib


def loadDataset(dir: str, option: str) -> pd.DataFrame:
    """
    Loads dataset root directory. returns empty pd.Dataframe if directory is invalid
    """
    root, option = pathlib.Path(dir), pathlib.Path(option)
    if root not in option.parent:
        return pd.DataFrame()
    
    # load raw cell data and pred labels (if any)
    cellLabels = open(f'{dir}/cell_labels.txt')
    