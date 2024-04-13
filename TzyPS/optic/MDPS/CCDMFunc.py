import numpy as np

def SymbolSign(Amp):
    Sign = np.random.randint(2, size = 1)
    Data = 0
    if(Sign[0]==1):
        Data = int(-Amp)
    else:
        Data = int(Amp)
    return Data

def LOG(base,x):
    return np.log(x)/np.log(base)
