import numpy as np
from scipy.interpolate import interp1d, Akima1DInterpolator
from Parse_Template import CFST_Cir_tcl
def monoData(data, col):
    target = data[:,col]
    output = data[0]
    for i in range(1, target.size):
        if target[i]>target[i-1]:
            output = np.vstack((output, data[i]))
    return output

def smoother(data, col1, col2, num1=100, num2=20):
    data = monoData(data, col1)
    target = data[:,col2]
    f1 = interp1d(target, data, axis=0)
    newX1 = np.linspace(target.min(), target.max(), num2)
    data1 = f1(newX1)
    f2 = Akima1DInterpolator(newX1, data1, axis=0)
    newX2 = np.linspace(target.min(), target.max(), num1)
    return f2(newX2)

def genTCL(file_path, conditionName):
    bc = 0.04
    dc = 0.01
    bt = 0.008
    bn = 0.008
    d_incr = 0.1
    tol = 1.0E-03
    iter_max = 100
    Es = 200.0E03
    
    file_names = np.loadtxt('./Test/file_names.txt', dtype='str')
    conditions = np.loadtxt(conditionName)
    bat_txt = ''
    for i in range(len(conditions)):
        file_name = file_names[i]
        D, t, L, fc, fy, N_axial = conditions[i]
        drift_ratios = [0.1*L]
        Condition = D, t, L, N_axial, fc, bc, dc, fy, fy, bt, bn, Es, tol, iter_max, d_incr, drift_ratios 
        CFST_Cir_tcl(Condition, file_path, file_name)
        bat_txt += 'OpenSees ' + file_name + '.tcl\n'
    f = open(file_path + '/run.bat', 'w')
    f.write(bat_txt)
    f.close()

def remove_nan(data1, data2):
    out = np.zeros((1,2))
    for i in range(data1.size):
        if not (np.isnan(data1[i]) or np.isnan(data2[i])):
            out = np.vstack((out, [data1[i], data2[i]]))
    out = out[1:].T
    return out[0], out[1]

def countUp(k, b, datax, datay):
    f = np.poly1d([k ,b])
    err = datay - f(datax)
    a = err[err>0.0]
    return len(a) / datax.size * 100