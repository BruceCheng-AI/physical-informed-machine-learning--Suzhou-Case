import numpy as np

def tank_model_Q2_impervious_area(precip, et, k1, k2, k3, A, kc, initial_storage1=0, initial_storage2=0, impervious_area=None):
    n = len(precip)
    storage1 = np.zeros(n)
    storage2 = np.zeros(n)
    outflow = np.zeros(n)
    surface_runoff = np.zeros(n)
    baseflow = np.zeros(n)
    
    storage1[0] = initial_storage1
    storage2[0] = initial_storage2
    
    for t in range(1, n):
        # 计算实际蒸散发
        et_actual = et[t] * kc
        
        # 第一个水箱（上游水箱）处理降水和蒸散发
        storage1[t] = storage1[t-1] + precip[t] - et_actual
        
        # 当存储量小于0时，将其设置为0
        storage1[t] = max(0, storage1[t])
        
        # 考虑城市不透水扩张的影响
        if impervious_area is not None:
            year = 1989 + t // 365  # 假设起始年份为1989年，并将天数转换为年份
            impervious_area_factor = 1 / (1 + impervious_area.loc[year, 'Predicted_impervious_area']/100)
            k1 *= impervious_area_factor
        
        # 第一个水箱的出流
        surface_runoff[t] = k1 * storage1[t]
        storage1[t] -= surface_runoff[t]
        
        # 第二个水箱（下游水箱）处理出流
        inflow = k2 * storage1[t]
        storage1[t] -= inflow
        storage2[t] = storage2[t-1] + inflow
        baseflow[t] = k3 * storage2[t]
        storage2[t] -= baseflow[t]
        
        # 总出流是第一个水箱和第二个水箱的出流之和
        outflow[t] = (surface_runoff[t] + baseflow[t]) *A / (3.6 * 24)       
        
    return surface_runoff, baseflow, outflow

def sugawara_model(precip, et, k1, k2, k3, k4, d1, d2, rfcf, ecorr, DT, AREA, initial_storage1=0, initial_storage2=0):
    n = len(precip)
    storage1 = np.zeros(n)
    storage2 = np.zeros(n)
    outflow = np.zeros(n)
    
    storage1[0] = initial_storage1
    storage2[0] = initial_storage2
    
    for t in range(1, n):
        # 计算实际蒸散发
        et_actual = et[t] * ecorr
        
        # 第一个水箱（上游水箱）处理降水和蒸散发
        H1 = max(storage1[t-1] + precip[t] * rfcf - et_actual, 0)
        
        # 当存储量小于0时，将其设置为0
        storage1[t] = max(0, H1)
        
        # 第一个水箱的出流
        q1 = k1 * (H1 - d1) if H1 > d1 else 0
        q2 = k2 * (H1 - d2) if H1 > d2 else 0
        q3 = k3 * H1
        Q1 = q1 + q2
        storage1[t] -= (q1 + q2 + q3)
        
        # 第二个水箱（下游水箱）处理出流
        H2 = storage2[t-1] + q3
        Q2 = k4 * H2
        storage2[t] -= Q2
        
        # 总出流是第一个水箱和第二个水箱的出流之和
        outflow[t] = (Q1 + Q2)
        
    return outflow, storage1, storage2

# considering the groundwater level
def sugawara_model_gw(precip, et, k1, k2, k3, k4, d1, d2, rfcf, ecorr, DT, AREA, gw, initial_storage1=0, initial_storage2=0):
    n = len(precip)
    storage1 = np.zeros(n)
    storage2 = np.zeros(n)
    outflow = np.zeros(n)
    
    storage1[0] = initial_storage1
    storage2[0] = initial_storage2
    
    for t in range(1, n):
        # 计算实际蒸散发
        et_actual = et[t] * ecorr
        
        # 第一个水箱（上游水箱）处理降水和蒸散发
        H1 = max(storage1[t-1] + precip[t] * rfcf - et_actual, 0)
        
        # 当存储量小于0时，将其设置为0
        storage1[t] = max(0, H1)
        
        # 第一个水箱的出流
        q1 = k1 * (H1 - d1) if H1 > d1 else 0
        q2 = k2 * (H1 - d2) if H1 > d2 else 0
        q3 = k3 * H1
        Q1 = q1 + q2
        storage1[t] -= (q1 + q2 + q3)
        
        # 第二个水箱（下游水箱）处理出流
        H2 = storage2[t-1] + q3 + gw
        Q2 = k4 * H2
        storage2[t] -= Q2
        
        # 总出流是第一个水箱和第二个水箱的出流之和
        outflow[t] = (Q1 + Q2) * AREA / (3.6 * DT)
        
    return outflow, storage1, storage2
