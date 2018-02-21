import numpy as np
import matplotlib.pyplot as plt
from DataMonoClass import DataMono

data = np.loadtxt('./DataC/level-0/C273-10-100-690-0.out').T

(DD, M) = (data[0], data[2])
a = DataMono(DD,M)
print(a.Kini)
print(a.dataNum)
a.cutMax()
print(a.dataNum)
a.revert()
print(a.dataNum)
pointY = a.findYield()
a.cutBeforeY()

plt.plot(a.xdata, a.ydata)
plt.plot(pointY[0], pointY[1], 'ko')
plt.show()
