import numpy as np
import matplotlib.pyplot as plt
from DataMonoClass import DataMono

data = np.loadtxt('./DataC/level-0/C273-10-100-690-0.out').T

(DD, M) = (data[0], data[2])
a = DataMono(DD,M)
print(a.dataNum)
print(a.findYield1()[1])
print(a.findYieldByDuctility(2.4))
'''
ratios = np.array([])
for i in range(a.dataNum):
    try:
        Fy, ratio = a.tryFindFy(a.dataNum-i)
        ratios = np.append(ratios, ratio)
    except:
        1==1
plt.plot(ratios)
plt.show()
'''


'''
plt.plot(a.xdata, a.ydata)
plt.plot(pointY[0], pointY[1], 'ko')
plt.show()
'''
