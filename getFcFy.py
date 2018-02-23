import numpy as np
import matplotlib.pyplot as plt
from DataMonoClass import DataMono
from CFST_Cir_Section_Analysis import CFST_Cir_Section_Analysis

def cutData(data, ratio=0.4):
    DD, N, M, Nc, Mc, Ns, Ms = data
    threhold = 0.4 * M.max()
    for i in range(M.size):
        if M[i] >= threhold:
            break
    return data[:,i:]

cutRatio = 0.6
iniRatio = 0.6
loadLevel = [0, 0.05, 0.1, 0.2, 0.3]

conditions = np.loadtxt('_CFST_Conditions.txt')
path = './DataC'


for i in range(len(loadLevel)):
    curLevel = loadLevel[i]
    dataAll = np.load('{0}/level-{1:.0f}/MaterialRelation.npy'.format(path, curLevel*100))
    outputs = np.zeros((1,9))
    for j in range(len(dataAll)):
        D, t, L, fc, fy = conditions[j]
        curData = dataAll[j]
        DD, fccs, fybs, hcs, hss = curData.T

        fcData = DataMono(DD, fccs, iniRatio)
        fyData = DataMono(DD, fybs, iniRatio)
        temp, fcc = fcData.findYield()
        temp, fyb = fyData.findYield()
        fcc = min(fcc, fccs[-1])
        outputs = np.vstack((outputs, [D, t, L, fc, fy, fcc, fyb, fcc/fc, fyb/fy]))
    outputs = outputs[1:]
    np.savetxt('{0}/level-{1:.0f}/fc_fy.txt'.format(path, curLevel*100), outputs)
