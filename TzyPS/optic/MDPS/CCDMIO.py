import ctypes
from ctypes import *
from numpy.ctypeslib import ndpointer
import numpy as np 
import pandas as pd

def csv_to_Matrix(path):
    Matrix = pd.read_csv(path, header=None, dtype={'id': int})
    Matrix = np.array(Matrix)
    return Matrix

def Matrix_to_csv(Matrix,name):
    np.savetxt(name, Matrix, delimiter=None, fmt = "%d")
    return


# lib = ctypes.cdll.LoadLibrary('d:/visual studio/CCDM/x64/Debug/CCDM.dll')
# lib.test.argtypes = [c_int]
# M = 16
# count = int(np.log2(M)*10e2)
# bits = np.random.randint(2, size = count)
# print(bits)
# Matrix_to_csv(bits)
# lib.test(count)
# m = csv_to_Matrix("d:/visual studio/test.csv")
# print(m)
