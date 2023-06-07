# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 08:31:08 2015

Tank Model

Implemented By Juan Chacon
"""
from __future__ import division
import numpy as np
import scipy.io as io
import matplotlib.pyplot as plt
import scipy.optimize as opt

# Define initial states, initial flow, and initial parameters
INITIAL_STATES = [10, 10] # initial states of the two tanks
INITIAL_Q = 1.0 # initial flow
INITIAL_PARAM = [0.5, 0.2, 0.01, 0.1, 10.0, 20.0, 1, 1] # initial parameters for the model

# Define parameter bounds
PARAM_BND = ((0.0, 1.1), # k1
             (0.0, 1.1), # k2
             (0.0, 1.5), # k3
             (0.0, 1.1), # k4
             (1.0, 15.0), # d1
             (0.1, 1.0), # d2
             (0.8, 1.2), # rfcf
             (0.8, 1.2)) # ecorr

def _step(prec, evap, st, param, extra_param):
    '''
    This function takes the following arguments:
    prec: Precipitation [mm]
    evap: Evaporation [mm]
    st: System states(2)[S1, S2]
        S1: Level of the top tank [mm]
        S2: Level of the bottom tank [mm]
    param: Parameter vector(8)
        k1: Upper tank upper discharge coefficient
        k2: Upper tank lower discharge coefficient
        k3: Percolation to lower tank coefficient
        k4: Lower tank discharge coefficient
        d1: Upper tank upper discharge position
        d2: Upper tank lower discharge position
        rfcf: Rainfall correction factor
        ecorr: Evaporation correction factor
    extra_param: Extra parameters(2)
        DT: Number of hours in the time step [s]
        AREA: Catchment area [km²]
    
    Outputs:
    Q: Flow [m³/s]
    S: Updated system states(2)[S1, S2] mm
    '''

    # Old states
    S1Old = st[0]
    S2Old = st[1]

    #Parameters
    k1, k2, k3, k4, d1, d2, rfcf, ecorr = param
    
    # Extra Parameters
    DT, Area = extra_param

    ## Top tank
    H1 = np.max([S1Old + prec*rfcf - evap*ecorr, 0])

    if H1 > 0:
        #direct runoff
        q1 = k1*(H1-d1) if H1 > d1 else 0

        #Fast response component
        q2 = k2*(H1-d2) if H1 > d2 else 0

        #Percolation to bottom tank
        q3 = k3 * H1
        #Check for availability of water in upper tank
        q123 = q1+q2+q3
        if q123 > H1:
            q1, q2, q3 = q1*q123/H1, q2*q123/H1, q3*q123/H1
    else:
        q1, q2, q3 = 0, 0, 0

    Q1 = q1+q2
    #State update top tank
    S1New = max(H1 - (q1+q2+q3), 0.0)
    
    ## Bottom tank
    H2 = S2Old+q3
    Q2 = k4* H2

    #check if there is enough water
    Q2 = H2 if Q2 > H2 else Q2

    #Bottom tank update
    S2New = H2 - Q2

    ## Total Flow
    Q = (Q1+Q2)*Area/(3.6*DT) if (Q1 + Q2) >= 0 else 0

    S = [S1New, S2New]
    return Q, S

def simulate(prec, evap, param, extra_param):
    '''
    This function simulates the model for a given set of inputs and parameters.
    prec: Precipitation [mm]
    evap: Evaporation [mm]
    param: Parameter vector(8)
        k1: Upper tank upper discharge coefficient
        k2: Upper tank lower discharge coefficient
        k3: Percolation to lower tank coefficient
        k4: Lower tank discharge coefficient
        d1: Upper tank upper discharge position
        d2: Upper tank lower discharge position
        rfcf: Rainfall correction factor
        ecorr: Evaporation correction factor
    extra_param: Extra parameters(2)
        DT: Number of hours in the time step [s]
        AREA: Catchment area [km²]
    
    Outputs:
    q: Flow [m³/s]
    st: Updated system states(2)[S1, S2] mm
    '''

    st = [INITIAL_STATES,]
    q = [INITIAL_Q,]

    for i in range(len(prec)):
        step_res = _step(prec[i], evap[i], st[i], param, extra_param)
        q.append(step_res[0])
        st.append(step_res[1])

    return q, st

def calibrate(prec, evap, extra_param, q_rec, verbose=False):
    '''
    This function calibrates the model for a given set of inputs and observed flows.
    prec: Precipitation [mm]
    evap: Evaporation [mm]
    extra_param: Extra parameters(2)
        DT: Number of hours in the time step [s]
        AREA: Catchment area [km²]
    q_rec: Observed flows [m³/s]
    verbose: Whether to print the performance function value at each iteration
    
    Outputs:
    cal_res.x: Optimized parameter vector
    cal_res.fun: Performance function value
    '''

    def mod_wrap(param_cal):
        q_sim = simulate(prec[:-1], evap[:-1], param_cal, extra_param)[0]
        try:
            perf_fun = -NSE(q_sim, q_rec)
        except:
            perf_fun = 9999

        if verbose: print(-perf_fun)
        return perf_fun

    cal_res = opt.minimize(mod_wrap, INITIAL_PARAM, bounds=PARAM_BND,
                           method='L-BFGS-B')

    return cal_res.x, cal_res.fun

def NSE(x,y,q='def',j=2.0):
    """
    Performance Functions
    x - calculated value
    y - recorded value
    q - Quality tag (0-1)
    j - exponent to modify the inflation of the variance (standard NSE j=2)
    """
    x = np.array(x)
    y = np.array(y)
    a = np.sum(np.power(x-y,j))
    b = np.sum(np.power(y-np.average(y),j))
    F = 1.0 - a/b
    return F

'''
TEsting function    
'''
for i in range(1000):
    prec = np.random.uniform(0, 100)
    evap = np.random.uniform(0, 10)
    st = [np.random.uniform(0, 30), np.random.uniform(0, 30)]
    param = [0.1819, 0.0412, 0.3348, 0.0448, 3.2259, 0.3800,1,1, 1]
    extra_param = [1, 145]
    _step(prec, evap, st, param, extra_param)