import numpy as np
from scipy.interpolate import interp1d

class DataMono:

    def __init__(self, xdata, ydata, iniRatio=0.4):
        (self.xdata, self.ydata) = (xdata, ydata);
        (self.xdatabackup, self.ydatabackup) = (xdata, ydata);
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
        self.xdata = self.xdata[:maxId+1]
        self.ydata = self.ydata[:maxId+1]
        self.initial()

    def revert(self):
        self.xdata = self.xdatabackup
        self.ydata = self.ydatabackup
        self.initial()

    def findYield1(self):
        self.cutMax()
        y = (2.0 * self.A - self.xdata[-1] * self.ydata[-1]) / (self.xdata[-1] - self.ydata[-1] / self.Kini)
        x = y / self.Kini
        
        self.revert()
        return (x,y)

    def findYield(self, ratio=0.1):
        for i in range(1, self.xdata.size):
            curK = (self.ydata[i] - self.ydata[i-1]) / (self.xdata[i] - self.xdata[i-1])
            if curK <= ratio * self.Kini:
                break
        return (self.xdata[i], self.ydata[i])

    def findY(self, x):
        return self.f(x)

    def tryFindFy(self, num):
        xdata = self.xdata[:num]
        ydata = self.ydata[:num]
        temp = DataMono(xdata,ydata, self.iniRatio)
        xxx, Fy = temp.findYield1()
        return Fy, temp.xdata.max()/xxx

    def findYieldByDuctility(self, TargetDuctility=2):
        for i in range(self.dataNum):
            Fy, ductility = self.tryFindFy(self.dataNum - i)
            if ductility<= TargetDuctility:
                break
        return ductility, Fy

    def cutBeforeY(self, ratio=0.4):
        Ymax = self.ydata.max()
        threhold = ratio * Ymax
        for i in range(self.dataNum-1):
            if self.ydata[i] >= threhold:
                break
        self.xdata = np.append(0.0, self.xdata[i:])
        self.ydata = np.append(0.0, self.ydata[i:])
        self.initial()
