import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from DataMonoClass import DataMono
from CFST_Cir_Section_Analysis import CFST_Cir_Section_Analysis

def cutData(data, ratio=0.4, num=20):
    DD, N, M, Nc, Mc, Ns, Ms = data
    threhold = ratio * M.max()
    for i in range(M.size):
        if M[i] >= threhold:
            break
    data = data[:,i:]
    DD, N, M, Nc, Mc, Ns, Ms = data
    f = interp1d(data[0], data)
    DD_new = np.linspace(DD[0], DD[-1], num=num)
    return f(DD_new)


cutRatio = 0.8
iniRatio = 0.4
loadLevel = [0, 0.05, 0.1, 0.2, 0.3]

conditions = np.loadtxt('_CFST_Conditions.txt')
path = './DataC'


for i in range(len(loadLevel)):
    curLevel = loadLevel[i]
    dataAll = np.load('{0}/level-{1:.0f}/data_ab.npy'.format(path, curLevel*100), encoding = 'latin1')
    outputs = []
    
    for j in range(len(dataAll)):
        curData = cutData(dataAll[j].T, cutRatio, num=100)
        DD, N, M, Nc, Mc, Ns, Ms = curData

        D, t, L, fc, fy = conditions[j]
        curCFST = CFST_Cir_Section_Analysis(D, t, fc, fy,Num=20)
        fccs, hcs = curCFST.getFcAvg(Nc*1000.0, Mc*1.0e6)
        fybs, hss = curCFST.getFyAvg(Ns*1000.0, Ms*1.0e6)
        curOutputs = np.zeros((1,5))
        curOutputs = np.vstack((curOutputs, np.vstack((DD, fccs, fybs, hcs, hss)).T))
        outputs.append(curOutputs)
    np.save('{0}/level-{1:.0f}/MaterialRelation.npy'.format(path, curLevel*100), outputs)
