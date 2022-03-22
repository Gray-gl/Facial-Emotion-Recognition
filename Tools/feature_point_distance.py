#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
描述：
    根据脸部特征点来计算关键帧的不同方法
Author: Gray_Gl
Last edited: February  2022
"""
import json

import numpy
import numpy as np
import imutils
import dlib
import cv2

def add_point(
        json_iten
):
    '''
    将需要标注特征点的json图片进行标注并进行显示。
    :param json_file:当前需要标注json条目路径
    :return:
    '''

# 计算两个128D的向量之间的欧氏距离
def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    return dist


def o_distance(point_a,point_b):
    '''
    通过传入的shape特征点，计算脸部主要器官关于中心特征点的相对位置移动和方向变化
    计算所有的点和中间点的欧氏距离和余弦距离，分别表示方向和距离的变化
    描述：
    :param
        point_a,point_b两个点的坐标
    :return:
    '''
    distance = numpy.sqrt(numpy.square(point_a[0]-point_b[0]) + numpy.square(point_a[1]-point_b[1]))
    return distance

def cos_distance(point_a,point_b,point_origin):
    '''
    计算三个点的余弦距离
    :param point_a:
    :param point_b:
    :param point_origin:
    :return:
    '''

    # 计算向量
    oa = numpy.array(point_a) - numpy.array(point_origin)
    ob = numpy.array(point_b) - numpy.array(point_origin)
    ab = numpy.dot(oa,ob)
    ab_abs = o_distance(point_a,point_origin) * o_distance(point_a,point_origin)
    return ab / ab_abs


def o_cos_distance(shape):
    '''
    通过传入的shape特征点，计算脸部主要器官关于选定的中心特征点的相对位置移动和方向变化
    计算所有的点和中间点的欧氏距离和余弦距离，分别表示方向和距离的变化
    :param shape:
    :return:
    '''

    # 嘴巴的角度变化
    # 横向
    mouse_x = cos_distance(shape[49],shape[55],shape[52])
    # 纵向
    mouse_y = cos_distance(shape[53],shape[57],shape[55])

    # 眼睛的角度变化
    # 横向
    eye_x = cos_distance(shape[44],shape[48],shape[43]) + cos_distance(shape[45],shape[47],shape[46]) + \
            cos_distance(shape[38],shape[42],shape[37]) + cos_distance(shape[39],shape[41],shape[40])
    eye_y = cos_distance(shape[37],shape[40],shape[39]) + cos_distance(shape[43],shape[46],shape[45])

    # 眉毛
    eyebrow_y = cos_distance(shape[18],shape[22],shape[20]) + cos_distance(shape[23],shape[27],shape[25])


    # 最简单的求和
    result = mouse_x + mouse_y + (eye_x + eye_y) * 10

    return result

if __name__ == '__main__':

    # 读取对应json文件
    with open(r'C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\dataset\data-100.json','r') as f:
        json_content = json.load(f)
    shape = json_content['FacialEmotion\\Facial-Emotion-Recognition\\dataset\\Label1\\dataset\\listening\\439.jpg']['feature_point']
    print(o_cos_distance(shape))