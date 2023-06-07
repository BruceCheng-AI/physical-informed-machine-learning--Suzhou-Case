import numpy as np

def tank_model_impervious_area(precip, et, k1, k2, k3, A, kc, initial_storage1=0, initial_storage2=0, impervious_area=None):
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
        storage1[t] = storage1[t-1] + precip[t] * A / 86.4 - et_actual * A / 86.4
        
        # 当存储量小于0时，将其设置为0
        storage1[t] = max(0, storage1[t])
        
        # 考虑城市不透水扩张的影响
        if impervious_area is not None:
            year = 1989 + t // 365  # 假设起始年份为1989年，并将天数转换为年份
            impervious_area_factor = 1 / (1 + impervious_area.loc[year, 'Predicted_impervious_area']/100)**2
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
        outflow[t] = surface_runoff[t] + baseflow[t]       
        
    return surface_runoff, baseflow, outflow