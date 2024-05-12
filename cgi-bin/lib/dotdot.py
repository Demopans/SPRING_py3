import pandas as pd

# implements data scructure as proposed https://www.biorxiv.org/content/10.1101/2024.01.02.573882v1

class DotDot:
    data: pd.DataFrame
    # axles must correspond between ro, and r1. differences will be ignored
    def __init__(self, r0: pd.DataFrame, r1: pd.DataFrame, axle1: list[str], axle2: list[str]):
        # clean
        ra0, ra1 = r0.axes, r1.axes
        rc = ra0[0].intersection(ra1[0])
        rr = ra0[1].intersection(ra1[1])
        
        # set up structure
        data = pd.DataFrame(index=rc, columns=rr)  
        # populate df
        r0s,r1s = r0.loc[rr,rc], r1.loc[rr,rc]
        
        pass
    pass

