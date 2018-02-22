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


data = np.loadtxt('./DataC/level-30/C273-10-100-690-30.out').T
data = cutData(data)
DD, N, M, Nc, Mc, Ns, Ms = data
D, t = 273.0, 10.0
fc, fy = 100.0, 690.0

a = CFST_Cir_Section_Analysis(D, t, fc, fy)

print(Nc[-1], Mc[-1])
ans = a.getFcAvg(Nc*1000.0, Mc*1.0e6)
print(ans[1])
plt.plot(DD,Mc)
plt.show()
