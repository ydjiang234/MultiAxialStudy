# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 13:21:50 2015

@author: yjiang
"""
import os
import numpy as np

import string
import random
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def Parse_Template(Contents, file_path_name, template):
    cur_text = template
    for key in Contents:
        cur_text = cur_text.replace(key, Contents[key])
    f = open(file_path_name, 'w')
    f.write(cur_text)
    f.close()


def CFST_Rect_tcl(Condition, file_path, file_name):
    f = open('Template_Rect_CFST_MPF.tcl', 'r')
    template = f.read()
    f.close()
    B, H, t, L, N_axial, fc, bc, dc, fyt, fyn, bt, bn, Es, tol, iter_max, d_incr, drift_ratios  = Condition
    Contents = {'{{B}}':str(B),
            '{{H}}':str(H),
            '{{t}}':str(t),
            '{{L}}':str(L),
            '{{N_axial}}':str(N_axial),
            '{{fc}}':str(fc),
            '{{bc}}':str(bc),
            '{{dc}}':str(dc),
            '{{fyt}}':str(fyt),
            '{{fyn}}':str(fyn),
            '{{bt}}':str(bt),
            '{{bn}}':str(bn),
            '{{Es}}':str(Es),
            '{{tol}}':str(tol),
            '{{iter_max}}':str(iter_max),
            '{{drift_ratios}}':' '.join([str(item) for item in drift_ratios]),
            '{{d_incr}}':str(d_incr),
            '{{fileID}}':file_name+'.out'}
    Parse_Template(Contents, '{0}/{1}.tcl'.format(file_path, file_name), template)

def CFST_Cir_tcl(Condition, file_path, file_name):
    f = open('Template_Cir_CFST_MPF.tcl', 'r')
    template = f.read()
    f.close()
    D, t, L, N_axial, fc, bc, dc, fyt, fyn, bt, bn, Es, tol, iter_max, d_incr, drift_ratios  = Condition
    Contents = {'{{D}}':str(D),
            '{{t}}':str(t),
            '{{L}}':str(L),
            '{{N_axial}}':str(N_axial),
            '{{fc}}':str(fc),
            '{{bc}}':str(bc),
            '{{dc}}':str(dc),
            '{{fyt}}':str(fyt),
            '{{fyn}}':str(fyn),
            '{{bt}}':str(bt),
            '{{bn}}':str(bn),
            '{{Es}}':str(Es),
            '{{tol}}':str(tol),
            '{{iter_max}}':str(iter_max),
            '{{drift_ratios}}':' '.join([str(item) for item in drift_ratios]),
            '{{d_incr}}':str(d_incr),
            '{{fileID}}':file_name+'.out'}
    Parse_Template(Contents, '{0}/{1}.tcl'.format(file_path, file_name), template)


def CFST_Rect_spring_tcl(Condition, file_path, file_name, K_spring=22000.0):
    f = open('Template_Rect_CFST_MPF_Spring.tcl', 'r')
    template = f.read()
    f.close()
    B, H, t, L, N_axial, fc, bc, dc, fyt, fyn, bt, bn, Es, tol, iter_max, d_incr, drift_ratios  = Condition
    Contents = {'{{B}}':str(B),
            '{{H}}':str(H),
            '{{t}}':str(t),
            '{{L}}':str(L),
            '{{N_axial}}':str(N_axial),
            '{{fc}}':str(fc),
            '{{bc}}':str(bc),
            '{{dc}}':str(dc),
            '{{fyt}}':str(fyt),
            '{{fyn}}':str(fyn),
            '{{bt}}':str(bt),
            '{{bn}}':str(bn),
            '{{Es}}':str(Es),
            '{{K_spring}}':str(K_spring),
            '{{tol}}':str(tol),
            '{{iter_max}}':str(iter_max),
            '{{drift_ratios}}':' '.join([str(item) for item in drift_ratios]),
            '{{d_incr}}':str(d_incr),
            '{{fileID}}':file_name+'.out'}
    Parse_Template(Contents, '{0}/{1}.tcl'.format(file_path, file_name), template)
