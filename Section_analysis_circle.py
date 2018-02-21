def A_cm_Circular(D, h):
    import numpy as np
    theta = np.arccos(2. * h / D)
    A1 = D**2 * theta / 4.
    A2 = D * h * np.sin(theta) / 2.
    A = A1 - A2
    M = (D**2 - 4. * h**2)**1.5 / 12.
    cm = M / A
    return A, cm

def A_cm_Circular_ring(D, t, h):
    A1, cm1 = A_cm_Circular(D - 2. * t, h)
    A, cm = A_cm_Circular(D, h)
    A2 = A - A1
    cm2 = (A * cm - A1* cm1) / A2
    return A2, cm2

def find_fc_Circular(N, M, D, cov = 100):
    import numpy as np
    from scipy.interpolate import interp1d
    '''
    hs = np.linspace(-D / 2. * 0.999, D / 2. * 0.999, cov)
    Ms = np.array([])
    fcs = np.array([])
    for h in hs:
        A, cm = A_cm_Circular(D, h)
        fc = N / A
        fcs = np.append(fcs, fc)
        M1= N * cm
        Ms = np.append(Ms, M1)
    f = interp1d(Ms, hs)
    try:
        cur_h = 1.0*f(M)
        A, cm = A_cm_Circular(D, cur_h)
        fc = N / A
        return fc, cur_h
    except:
        return 0, 0
    '''
    hs = np.linspace(-D / 2. * 0.999, D / 2. * 0.999, cov)
    Ns = np.array([])
    fcs = np.array([])
    for h in hs:
        A, cm = A_cm_Circular(D, h)
        fc = M / cm / A
        fcs = np.append(fcs, fc)
        N1 = A * fc
        Ns = np.append(Ns, N1)
    f = interp1d(Ns, hs)
    try:
        cur_h = 1.0*f(N)
        A, cm = A_cm_Circular(D, cur_h)
        fc = M / cm / A
        return fc, cur_h
    except:
        return 0, 0
        
def find_fy_Circular_ring(N, M, D, t, cov = 150, base = 10):
    import numpy as np
    from scipy.interpolate import interp1d
    '''
    if N >= 0:
        hs = np.linspace(-D / 2. + t*1.0001, 0, cov)
    else:
        hs = np.linspace(0, -D / 2. + t*1.0001, cov)
    fys = np.array([])
    Ms = np.array([])
    for h in hs:
        An, cmn = A_cm_Circular_ring(D, t, h)
        At, cmt = A_cm_Circular_ring(D, t, -h)
        fy = abs(N / (An - At))
        fys = np.append(fys, fy)
        M1 = (An * cmn + At * cmt) * fy
        Ms = np.append(Ms, M1)
    f = interp1d(Ms, np.log(abs(hs)) / np.log(base))
    try:
        if N >= 0:
            cur_h = -1.0 * base**f(M)
        else:
            cur_h = base**f(M)
        An, cmn = A_cm_Circular_ring(D, t, cur_h)
        At, cmt = A_cm_Circular_ring(D, t, -cur_h)
        fy = abs(N / (An - At))
        return fy, cur_h
    except:
        return 0, 0
    '''
    if N >= 0:
        hs = np.linspace(-D / 2. + t*1.0001, 0, cov)
    else:
        hs = np.linspace(0, -D / 2. + t*1.0001, cov)
    fys = np.array([])
    Ns = np.array([])
    for h in hs:
        An, cmn = A_cm_Circular_ring(D, t, h)
        At, cmt = A_cm_Circular_ring(D, t, -h)
        fy = M / (An * cmn + At * cmt) 
        N1 = fy * abs(An - At)
        if N > 0:
            N1 = N1
        else:
            N1 = -1.0 * N1
        fys = np.append(fys, fy)
        Ns = np.append(Ns, N1)
    f = interp1d(Ns, hs)
    try:
        if N >= 0:
            cur_h = -1.0 * f(N)
        else:
            cur_h = f(N)
        An, cmn = A_cm_Circular_ring(D, t, cur_h)
        At, cmt = A_cm_Circular_ring(D, t, -cur_h)
        fy = M / (An * cmn + At * cmt)
        return fy, cur_h
    except:
        return 0, 0