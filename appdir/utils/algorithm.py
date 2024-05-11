from math import *

import numpy as np


def find_line_z_intersection(point1, point2, z0):
    """求解两个点构成的直线与z0平面的交点"""
    # 将坐标点转换为NumPy数组
    point1 = np.array(point1)
    point2 = np.array(point2)

    # 计算直线的方向向量
    direction_vector = point2 - point1

    # 计算直线与z平面的交点
    t = (z0 - point1[2]) / direction_vector[2]
    intersection_point = point1 + t * direction_vector
    return intersection_point.tolist()


def calculate_angle_between_lines(v1, v2):
    """求解角度"""
    v1 = np.array(v1)
    v2 = np.array(v2)
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    angle = np.arccos(np.abs(dot_product) / (norm_v1 * norm_v2))
    return angle


def calculate_line_intersection(args):
    """计算四边形对角线的交点，要求输入的均为三维坐标（4个点z轴一致），输出为交点的三维坐标"""
    a, b, c, d = args
    # 计算 a-c 直线的斜率和截距
    m1 = (c[1] - a[1]) / (c[0] - a[0] + 1e-10)  # 避免除0运算
    b1 = a[1] - m1 * a[0]
    # 计算 b-d 直线的斜率和截距
    m2 = (d[1] - b[1]) / (d[0] - b[0] + 1e-10)
    b2 = b[1] - m2 * b[0]
    # 构造方程组
    A = np.array([[1, -m1], [1, -m2]])
    B = np.array([b1, b2])
    # 求解方程组
    intersection = np.linalg.solve(A, B)
    return intersection.tolist()[::-1] + [a[2]]


# 计算杆塔倾斜度的算法
def cal(towerUpperE: str,
        towerUpperS: str,
        towerUpperW: str,
        towerUpperN: str,
        towerBottomE: str,
        towerBottomS: str,
        towerBottomW: str,
        towerBottomN: str):
    try:
        # 数据预处理
        eb = list(map(float, towerBottomE.strip().split(" ")))
        nb = list(map(float, towerBottomN.strip().split(" ")))
        wb = list(map(float, towerBottomW.strip().split(" ")))
        sb = list(map(float, towerBottomS.strip().split(" ")))
        eu = list(map(float, towerUpperE.strip().split(" ")))
        nu = list(map(float, towerUpperN.strip().split(" ")))
        wu = list(map(float, towerUpperW.strip().split(" ")))
        su = list(map(float, towerUpperS.strip().split(" ")))
        # 封装数据
        points = [[eb, nb, wb, sb], [eu, nu, wu, su]]
        # 找到最低zl和最高的zh
        zl, zh = inf, -inf
        for i in points[0]:
            zl = min(zl, i[2])
        for i in points[1]:
            zh = max(zh, i[2])
        # 获取四个棱与zl和zh平面的交点
        new_points = [[find_line_z_intersection(points[0][i], points[1][i], zl) for i in range(4)],
                      [find_line_z_intersection(points[0][i], points[1][i], zh) for i in range(4)]]  # 存放新的交点数组
        P = calculate_line_intersection(new_points[0])
        p = calculate_line_intersection(new_points[1])
        angle = calculate_angle_between_lines(v1=[0, 0, 1],
                                              v2=[P[0] - p[0], P[1] - p[1], P[2] - p[2]])
        return str(abs(np.degrees(angle)))
    except:
        return None


if __name__ == '__main__':
    towerUpperE = "34.1766216 109.1832573 756.617"
    towerUpperS = "34.1766495 109.1832546 756.521"
    towerUpperW = "34.1766474 109.1832188 756.495"
    towerUpperN = "34.1766195 109.1832208 756.579"
    towerBottomE = "34.1765715 109.1833481 704.244"
    towerBottomS = "34.1766991 109.1833288 704.255"
    towerBottomW = "34.1766853 109.1831741 703.678"
    towerBottomN = "34.1765581 109.1831908 703.656"
    res = cal(towerUpperE=towerUpperE,
              towerUpperS=towerUpperS,
              towerUpperW=towerUpperW,
              towerUpperN=towerUpperN,
              towerBottomE=towerBottomE,
              towerBottomS=towerBottomS,
              towerBottomW=towerBottomW,
              towerBottomN=towerBottomN)
    print(res)
