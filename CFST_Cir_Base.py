import numpy as np

class CFST_Cir:

    def __init__(self, D, t, fc, fy):
        self.D = D
        self.t = t
        self.fc = fc
        self.fy = fy
        self.initial()

    def initial(self):
        self.A = np.pi * self.D**2 /4.0
        self.Ac = np.pi * (self.D - 2.0 * self.t)**2 /4.0
        self.As = self.A - self.Ac
        
        self.I = self.Cir_I(self.D)
        self.Ic = self.Cir_I(self.D - 2.0 * self.t)
        self.Is = self.I - self.Ic

    def Cir_I(self, D):
        return np.pi * D**4 / 64.0
