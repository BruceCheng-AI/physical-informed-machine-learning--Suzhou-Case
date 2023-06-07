import numpy as np

def integrated_model(params, precipitation, et,Area, impervious_area=None):
    infiltration_rate, percolation_rate, baseflow_rate, upper_zone_storage, lower_zone_storage = params
    n = len(precipitation)
    runoff = np.zeros(n)
    surface_runoff = np.zeros(n)
    baseflow = np.zeros(n)
    
    # Get the start year from impervious_area if it's not None
    start_year = impervious_area.index.min() if impervious_area is not None else 1989
    
    for i in range(n):
        # 考虑城市不透水扩张的影响
        if impervious_area is not None:
            year = start_year + i // 365  # 假设起始年份为1989年，并将天数转换为年份
            impervious_area_factor = 1 / (1 + impervious_area.loc[year, 'Predicted_impervious_area']/100)
            infiltration_rate *= impervious_area_factor        
        # calculate infiltration
        infiltration = min(precipitation[i], infiltration_rate * upper_zone_storage)
        # calculate surface runoff
        surface_runoff[i] = max(0,(precipitation[i] - infiltration- et[i] )) * Area / (3.6 * 24)
        # update upper zone storage
        upper_zone_storage = upper_zone_storage + infiltration  
        # calculate percolation
        percolation = min(upper_zone_storage, percolation_rate * upper_zone_storage)
        # update upper zone storage
        upper_zone_storage -= percolation
        # update lower zone storage
        lower_zone_storage += percolation
        # calculate baseflow
        baseflow[i] = (min(lower_zone_storage, baseflow_rate * lower_zone_storage)) * Area / (3.6 * 24)
        # calculate total runoff
        runoff[i] = surface_runoff[i]+ baseflow[i]
        # update lower zone storage
        # 这里考虑苏州的特殊情况，水系复杂工业园区有很多地下水的补给，baseflow由重力流产生，不会减少地下水的储量
        # lower_zone_storage -= baseflow[i]
    return runoff, surface_runoff, baseflow

