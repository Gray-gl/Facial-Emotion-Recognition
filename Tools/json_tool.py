#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
描述：
    仅仅包含所有针对文件转成json的工具

Author: Gray_Gl
Last edited: February  2022
"""
import os
import json

from numpy import random

'''
    描述：根据类别下载的图片直接转成对应的json文件
    注意：多次下载都是保存到同一个文件中，所以，每一次在过滤重复图片之后进行更新，生成统一的json文件
'''
def convert_download_json(prefix_dir,dir_name,output_dir):
    '''
    将下载的图片按照文件名进行分类
    :param prefix_dir: 项目在当前主机中的路径
    :param dir_name: 当前的文件在当前的项目中的路径，这里传入的是当前的某一个类别所代表的文件
    :param output_dir：最终生成的json文件的输出位置
    :return:
    '''

    absolute_path = os.path.join(prefix_dir,dir_name)
    result = dict()
    # 遍历当前目录下的所有文件，并生成对应json文件
    for i in os.listdir(absolute_path):
        tick = dir_name.split('\\')[-1]
        
        # 根据key生成对应json文件的item 
        key = os.path.join(dir_name,i)
        item = dict()
        item[key] = dict()
        item[key]["label"] = tick

        # 合并原来的字典
        result.update(item)

    # 将对应result保存到对应json文件中，位置应该是dirname去除六个类别的关键字之后位置
    with open(output_dir, 'w+') as f:
        json.dump(result, f)



def sample_json(source_json:str,nums:int):
    '''
    从source_json中随即提取特定数量num的样例，重命名在原来的路径中生成新json文件
    :param source_json:
    :param nums:
    :return:
    '''

    # 打开json文件，并生成字典
    all_item = dict()
    with open(source_json,'r') as f:
        all_item = json.loads(f)

    # 对字典进行随机抽样
    keys = random.sample(list(all_item), nums)
    values = [all_item[k] for k in keys]
    result = dict(zip(keys, values))

    # 将结果在原来的位置进行保存
    target_json = source_json.split('.')[0] + '-' +str(nums) + '.json'
    # 将对应result保存到对应json文件中，位置应该是dirname去除六个类别的关键字之后位置
    with open(target_json, 'w+') as f:
        json.dump(result, f)

if __name__ == '__main__':
    prefix_dir = r'C:\Users\gray\Desktop\FacialEmotion'
    dir_path = r'Facial-Emotion-Recognition\cumulate_data\download_image_online\tired'
    output_dir = r''
    convert_download_json(dir_path)
