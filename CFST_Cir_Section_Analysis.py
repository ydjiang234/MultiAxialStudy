import numpy as np
from CFST_Cir_Base import CFST_Cir
from scipy.interpolate import interp1d

class CFST_Cir_Section_Analysis(CFST_Cir):

    def __init__(self, D, t, fc, fy, Num=100):
        self.Num = 100
        CFST_Cir.__init__(self, D, t, fc, fy)

    def initial(self):
        self.hs = np.linspace(-(self.D - 2.0 * self.t) / 2. * 0.99, (self.D - 2.0 * self.t) / 2. * 0.99, self.Num)
        self.getFcAvg = np.vectorize(self.getfcAvg)
        self.getFyAvg = np.vectorize(self.getfyAvg)


    def A_cm_Circular(self, D, h):
        theta = np.arccos(2. * h / D)
        A1 = D**2 * theta / 4.
        A2 = D * h * np.sin(theta) / 2.
        A = A1 - A2
        M = (D**2 - 4. * h**2)**1.5 / 12.
        cm = M / A
        return A, cm

    def A_cm_Circular_ring(self, D, t, h):
        A1, cm1 = self.A_cm_Circular(D - 2. * t, h)
        A, cm = self.A_cm_Circular(D, h)
        A2 = A - A1
        cm2 = (A * cm - A1* cm1) / A2
        return A2, cm2

    def getfcAvg(self, Nc, Mc):
        A, cm = self.A_cm_Circular(self.D - 2.0 * self.t, self.hs)
        fcs = Mc / cm / A
        Ns = A * fcs
        f = interp1d(Ns, self.hs, bounds_error=False, fill_value=(self.hs[0], self.hs[-1]))
        cur_h = 1.0*f(Nc)
        A, cm = self.A_cm_Circular(self.D - 2.0 * self.t, cur_h)
        fc = Mc / cm / A
        return fc, cur_h
                   
    def getfyAvg(self, Ns, Ms):

        An, cmn = self.A_cm_Circular_ring(self.D, self.t, self.hs)
        At, cmt = self.A_cm_Circular_ring(self.D, self.t, -1.0 * self.hs)
        fys = Ms / (An * cmn + At * cmt) 
        Nss = fys * (An - At)
        f = interp1d(Nss, self.hs, bounds_error=False, fill_value=(self.hs[0], self.hs[-1]))
        cur_h = f(Ns)
        An, cmn = self.A_cm_Circular_ring(self.D, self.t, cur_h)
        At, cmt = self.A_cm_Circular_ring(self.D, self.t, -cur_h)
        fy = Ms / (An * cmn + At * cmt)
        return fy, cur_h
