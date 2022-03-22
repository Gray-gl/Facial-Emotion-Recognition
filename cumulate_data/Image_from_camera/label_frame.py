#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

将已经生成帧进行标注，需要传入关键帧保存的文件，并指定最终的json输出目录

Author: Gray_Gl
Last edited: February  2022
"""
import json
import os
import cv2

def label_image(
    frame_dir:str,
    prefix_path:str,
    output_dir:str
):
    '''
    读取frame_dir中的所有内容，并进行标注，生成json文件在output_dir中
    :param frame_dir: 保存帧的目录
    :param path_prefix: 单项数据的前缀文件，字典中都是从当前项目中出发的相对路径
    :param output_dir: 最终json的输出目录
    :return:
    '''

    # 遍历保存帧的目录，获取所有帧的内容
    absolute_path = os.path.join(prefix_path, frame_dir)
    result = dict()

    # 遍历当前目录下的所有文件，并生成对应json文件
    for i in os.listdir(absolute_path):

        # 输出提示信息
        print("0 is confused")
        print("1 is distracted")
        print("2 is listening")
        print("3-21 is tired")
        print("4 is understanding")
        print("5 表示未知")

        # 打开并展示每一张图片
        frame = os.path.join(absolute_path,i)
        img = cv2.imread(frame)
        cv2.imshow('image', img)
        k = cv2.waitKey(0)
        cv2.destroyAllWindows()
        key = os.path.join(frame_dir,i)
        result[key] = dict()

        # 根据分类进行标记
        if k == 48:
            # confused类
            result[key]['label'] = 'confused'
        elif k == 49:
            # distracted类
            result[key]['label'] = 'distracted'
        elif k == 50:
            # listening类
            result[key]['label'] = 'listening'
        elif k == 51:
            # tired类
            result[key]['label'] = 'tired'
        elif k == 52:
            # understanding类
            result[key]['label'] = 'understanding'
        elif k == 53:
            # 未知
            result[key]['label'] = 'unknown'


    # 将对应result保存到对应json文件中，位置应该是dirname去除六个类别的关键字之后位置
    with open(output_dir, 'w+') as f:
        json.dump(result, f)

if __name__ == '__main__':
    label_image(r'dataset/Label3/new/image.json',
                r'/')