import numpy as np
import scipy.optimize as opt

def _step(prec, evap, st, param):

    # 旧状态
    S1Old = st[0]
    S2Old = st[1]

    # 参数
    k1, k2, k3, k4, d1, d2, rfcf, ecorr, Area = param

    ## 上层水箱
    H1 = np.max([S1Old + prec*rfcf - evap*ecorr, 0])

    if H1 > 0:
        # 直接径流
        q1 = k1*(H1-d1) if H1 > d1 else 0

        # 快速反应组分
        q2 =k2*(H1-d2) if H1 > d2 else 0

        # 渗透到下层水箱
        q3 = k3 * H1
        # 检查上层水箱中的水是否足够
        q123 = q1+q2+q3
        if q123 > H1:
            q1, q2, q3 = q1*q123/H1, q2*q123/H1, q3*q123/H1
    else:
        q1, q2, q3 = 0, 0, 0

    Q1 = q1+q2
    # 更新上层水箱状态
    S1New = max(H1 - (q1+q2+q3), 0.0)
    
    ## 下层水箱
    H2 = S2Old+q3
    Q2 = k4* H2

    # 检查是否有足够的水
    Q2 = H2 if Q2 > H2 else Q2

    # 更新下层水箱
    S2New = H2 - Q2

    ## 总流量
    Q = (Q1+Q2)* Area /86.4 if (Q1 + Q2) >= 0 else 0

    S = [S1New, S2New]
    return Q, S

def simulate(prec, evap, param, INITIAL_STATES=[10, 10], INITIAL_Q=1.0):
    '''
    这个函数模拟给定输入和参数的模型。
    prec: 降水量 [mm]
    evap: 蒸发量 [mm]
    param: 参数向量(8)
        k1: 上层水箱上部出水口系数
        k2: 上层水箱下部出水口系数
        k3: 渗透到下层水箱的系数
        k4: 下层水箱出水口系数
        d1: 上层水箱上部出水口位置
        d2: 上层水箱下部出水口位置
        rfcf: 降雨校正因子
        ecorr: 蒸发校正因子
        AREA: 流域面积 [km²]
    INITIAL_STATES: 初始状态的两个水箱
    INITIAL_Q: 初始流量
    
    输出：
    q: 流量 [m³/s]
    st: 更新的系统状态(2)[S1, S2] mm
    '''

    st = [INITIAL_STATES,]
    q = [INITIAL_Q,]

    for i in range(len(prec)):
        step_res = _step(prec[i], evap[i], st[i], param)
        q.append(step_res[0])
        st.append(step_res[1])

    return q
