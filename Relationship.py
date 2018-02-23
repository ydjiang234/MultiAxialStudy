import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import FontProperties
from rdp import rdp
from CFST_Cir_Base import CFST_Cir


font_label = FontProperties(family='Times New Roman',style='normal', size = 10)
font = {'family' : 'Times New Roman',
        'weight' : 'normal',
        'size'   : 10,
        }
matplotlib.rc('font', **font)

loadLevel = [0, 0.05, 0.1, 0.2, 0.3]
path = './DataC'

point_styles = ['k^', 'r>', 'bo', 'yD', 'gs']
colors = [item + '-' for item in point_styles]
ms = 5
x_range = 1, 5
y_range = 0.9, 1.2
fig_c, ax_c = plt.subplots(1, 1, figsize=[6.2,4])
fig_s, ax_s = plt.subplots(1, 1, figsize=[6.2,4])

for i in range(len(loadLevel)):
    curLevel = loadLevel[i]
    data = np.loadtxt('{0}/level-{1:.0f}/fc_fy.txt'.format(path, curLevel*100)).T
    D, t, L, fc, fy, fcc, fyb, ratioFc, ratioFy = data
    #factor
    A = np.pi * D**2 / 4.0
    Ac = np.pi * (D - 2.0 * t)**2 / 4.0
    As = A - Ac
    factor = np.log(Ac * fc / As /fy**0.5)
    #plot
    ax_c.plot(factor, ratioFc, point_styles[i], markersize=ms)
    kc, bc = np.polyfit(factor.ravel(),ratioFc.ravel(),1)
    f_c = np.poly1d([kc ,bc])
    ax_c.plot([-1,10], f_c([-1,10]), colors[i], label =r'$\mu_n$={0:.0f}\%'.format(curLevel*100), markersize=ms, linewidth=3)


    ax_s.plot(factor, ratioFy, point_styles[i], markersize=ms)
    ks, bs = np.polyfit(factor.ravel(),ratioFy.ravel(),1)
    fs = np.poly1d([ks ,bs])
    ax_s.plot([-1,10], fs([-1,10]), colors[i], label =r'$\mu_n$={0:.0f}\%'.format(curLevel*100), markersize=ms, linewidth=3)

for ax in [ax_c, ax_s]:
    ax.set_xlim(x_range)
    #ax.set_ylim(y_range)
    ax.grid(True)
plt.show()

