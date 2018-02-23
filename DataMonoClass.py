import numpy as np
from scipy.interpolate import interp1d

class DataMono:

    def __init__(self, xdata, ydata, iniRatio=0.4):
        (self.xdata, self.ydata) = (xdata, ydata);
        self.iniRatio = iniRatio

        self.initial()

    def initial(self):
        self.dataNum = self.xdata.size
        self.Kini = self.getInitialTangent(self.iniRatio)
        self.getArea()
        self.f = interp1d(self.xdata, self.ydata, bounds_error=False, fill_value=(self.ydata[0], self.ydata[-1]))

    def getArea(self):
        tempx = self.xdata[1:] - self.xdata[:-1]
        tempy = (self.ydata[1:] + self.ydata[:-1]) / 2.0
        self.A = np.sum(tempx * tempy)
    
    def getInitialTangent(self, ratio=0.4):
        Ymax = self.ydata.max()
        threhold = ratio * Ymax
        for i in range(self.dataNum-1):
            if self.ydata[i] >= threhold:
                break
        k = self.ydata[i] / self.xdata[i]
        return k

    def cutMax(self):
        maxId = self.ydata.argmax()
        self.xdatabackup = self.xdata.copy()
        self.ydatabackup = self.ydata.copy()
        self.xdata = self.xdata[:maxId+1]
        self.ydata = self.ydata[:maxId+1]
        self.initial()

    def revert(self):
        self.xdata = self.xdatabackup
        self.ydata = self.ydatabackup
        self.initial()

    def findYield(self):
        self.cutMax()
        y = (2.0 * self.A - self.xdata[-1] * self.ydata[-1]) / (self.xdata[-1] - self.ydata[-1] / self.Kini)
        x = y / self.Kini
        
        self.revert()
        return (x,y)

    def findY(self, x):
        return self.f(x)

    def cutBeforeY(self, ratio=0.4):
        self.xdatabackup = self.xdata.copy()
        self.ydatabackup = self.ydata.copy()
        Ymax = self.ydata.max()
        threhold = ratio * Ymax
        for i in range(self.dataNum-1):
            if self.ydata[i] >= threhold:
                break
        self.xdata = np.append(0.0, self.xdata[i:])
        self.ydata = np.append(0.0, self.ydata[i:])
        self.initial()


    



        
        
