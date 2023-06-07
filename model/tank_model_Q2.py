import numpy as np

def _compute_outflows(t, storage1, surface_runoff, subsurface_runoff, storage2, baseflow, k1, k2, k3, k4, d1, d2):
    # Outflow from the first tank
    surface_runoff[t] = k1 * max(storage1[t] - d1, 0) if storage1[t] > d1 else 0
    subsurface_runoff[t] = k2 * max(storage1[t] - d2, 0) if storage1[t] > d2 else 0
    storage1[t] -= (surface_runoff[t] + subsurface_runoff[t])
    
    # Infiltration to the second tank
    infiltration = k3 * storage1[t]
    storage1[t] -= infiltration
    storage2[t] = storage2[t-1] + infiltration
    
    # Baseflow from the second tank
    baseflow[t] = k4 * storage2[t]
    storage2[t] -= baseflow[t]
    
    # Total outflow is the sum of outflows from the first and second tanks
    outflow = surface_runoff[t] + subsurface_runoff[t] + baseflow[t]
    
    return outflow, storage1, storage2


def tank_model(precip, et, k1, k2, k3, k4, d1, d2, A, kc, initial_storage1=0, initial_storage2=0):
    
    n = len(precip)
    storage1 = np.zeros(n)
    storage2 = np.zeros(n)
    outflow = np.zeros(n)
    surface_runoff = np.zeros(n)
    subsurface_runoff = np.zeros(n)
    baseflow = np.zeros(n)
    
    for t in range(1, n):
        # Compute actual evapotranspiration
        et_actual = et[t] * kc
        
        # First tank (upstream tank) handles precipitation and evapotranspiration
        storage1[t] = storage1[t-1] + precip[t] * A / 86.4 - et_actual * A / 86.4
        
        # Set to 0 when storage is less than 0
        storage1[t] = max(0, storage1[t])
        
        outflow[t], storage1, storage2 =  _compute_outflows(t, storage1, surface_runoff, subsurface_runoff, storage2, baseflow, k1, k2, k3, k4, d1, d2)
        
    return surface_runoff, subsurface_runoff, baseflow, outflow
