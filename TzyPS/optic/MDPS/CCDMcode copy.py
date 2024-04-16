from CCDMIO import csv_to_Matrix, Matrix_to_csv
from CCDMFunc import SymbolSign, LOG
import numpy as np
import ctypes
from ctypes import *

def CCDMEnc(M,n,Block_Length,Block_Count,Prob_n_i):
    # Calculate some parameters
    lib = ctypes.cdll.LoadLibrary('/content/4D-PS-QAM-with-Subcarriers/TzyPS/dll/CCDMEnc.dll')
    lib.CCDM_Enc.argtypes = [c_int, c_int, c_int]
    Amp_Count = int(np.power(2, LOG(4,M) - 1))
    Amp_Data = np.arange(1, 2*(Amp_Count), 2)
    QAM_I = np.zeros((Block_Count,n))
    QAM_Q = np.zeros((Block_Count,n))
    ProbCount = int(Prob_n_i.size)
    Matrix_to_csv(Prob_n_i,'/content/4D-PS-QAM-with-Subcarriers/TzyPS/csv/Prob.csv')

    # generate shaped I-symbols
    print("Getting I-symbols...")
    for i in range(0,Block_Count):
        bitsI = np.random.randint(2, size = Block_Length)
        Matrix_to_csv(bitsI,'/content/4D-PS-QAM-with-Subcarriers/TzyPS/csv/EncPy.csv')
        lib.CCDM_Enc(Block_Length,n,ProbCount)
        ResI = csv_to_Matrix("/content/4D-PS-QAM-with-Subcarriers/TzyPS/csv/EncCpp.csv")
        # Get sign
        for j in range(0,n):
            for k in range(0,Amp_Count):
                if(ResI[j] == k+1):
                    ResI[j] = SymbolSign(Amp_Data[k])
                    QAM_I[i][j] = ResI[j]
                    break
            print(f'{i+1}/{Block_Count}',end='\r')
    print("")
    print("Done!")

    # generate shaped Q-symbols
    print("Getting Q-symbols...")
    for i in range(0,Block_Count):
        bitsQ = np.random.randint(2, size = Block_Length)
        Matrix_to_csv(bitsQ,'/content/4D-PS-QAM-with-Subcarriers/TzyPS/csv/EncPy.csv')
        lib.CCDM_Enc(Block_Length,n,ProbCount)
        ResQ = csv_to_Matrix("/content/4D-PS-QAM-with-Subcarriers/TzyPS/csv/EncCpp.csv")
        # Get sign
        for j in range(0,n):
            for k in range(0,Amp_Count):
                if(ResQ[j] == k+1):
                    ResQ[j] = SymbolSign(Amp_Data[k])
                    QAM_Q[i][j] = ResQ[j]              
                    break
        print(f'{i+1}/{Block_Count}',end='\r')  
    print("")
    print("Done!")

    # Generate QAM symbols
    print("Generating symbols...")
    CodeSymbols = np.zeros((Block_Count,n),dtype=complex)
    for i in range(0,Block_Count):
        for j in range(0,n):
            CodeSymbols[i][j] =QAM_I[i][j] + 1j*QAM_Q[i][j]  
    return CodeSymbols, Amp_Data

def CCDMDec(M,n,Block_Length,Block_Count,Prob_n_i,Sym):
    # Calculate some parameters
    lib = ctypes.cdll.LoadLibrary('/content/4D-PS-QAM-with-Subcarriers/TzyPS/dll/CCDMDec.dll')
    lib.CCDM_Dec.argtypes = [c_int, c_int, c_int]
    Amp_Count = int(np.power(2, LOG(4,M) - 1))
    Amp_Data = np.arange(1, 2*(Amp_Count), 2)
    Amp_I = np.abs(Sym.real)
    Amp_Q = np.abs(Sym.imag)
    ProbCount = int(Prob_n_i.size)
    Matrix_to_csv(Prob_n_i,'/content/4D-PS-QAM-with-Subcarriers/TzyPS/csv/Prob.csv')
    ResI = np.zeros((Block_Count,Block_Length))
    ResQ = np.zeros((Block_Count,Block_Length))

    # Decode I-bits
    print("Decoding I-bits...")
    # Get Amp for CCDM
    for h in range(0,Block_Count):
        for j in range(0,n):
            for k in range(0,Amp_Count):
                if((Amp_I[h][j] == Amp_Data[k]).all()):
                    Amp_I[h][j] = k
        Matrix_to_csv(Amp_I[h,:],'/content/4D-PS-QAM-with-Subcarriers/TzyPS/csv/DecPy.csv')
        lib.CCDM_Dec(n,ProbCount,Block_Length)
        BitI = csv_to_Matrix("/content/4D-PS-QAM-with-Subcarriers/TzyPS/csv/DecCpp.csv")
        for m in range(0,Block_Length):
            ResI[h][m] = BitI[m]
        print(f'{h+1}/{Block_Count}',end='\r')
    print("")
    print("Done!")

    # Decode Q-bits
    print("Decoding Q-bits...")
    # Get Amp for CCDM
    for i in range(0,Block_Count):
        for j in range(0,n):
            for k in range(0,Amp_Count):
                if((Amp_Q[i][j] == Amp_Data[k]).all()):
                    Amp_Q[i][j] = k
        Matrix_to_csv(Amp_Q[i,:],'/content/4D-PS-QAM-with-Subcarriers/TzyPS/csv/DecPy.csv')
        lib.CCDM_Dec(n,ProbCount,Block_Length)
        BitQ = csv_to_Matrix("/content/4D-PS-QAM-with-Subcarriers/TzyPS/csv/DecCpp.csv")
        for m in range(0,Block_Length):
            ResQ[i][m] = BitQ[m]
        print(f'{i+1}/{Block_Count}',end='\r')
    print("")
    print("Done!")

    return ResI, ResQ