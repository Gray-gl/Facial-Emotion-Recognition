#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
描述：
	处理上传的视频，并保存每一帧以及对应特征距离，同时将结果使用图片进行标注


Author: Gray_Gl
Last edited: February  2022
"""
# import the necessary packages
import cv2
import os
from Tools import feature_point_distance, GenJson
import matplotlib.pyplot as plt

# construct the argument parse and parse the arguments

def draw_plot(x,y):
	'''
	绘制折现网格图
	:param x:
	:param y:
	:return:
	'''

	# 设置各个坐标轴的刻度线位置，x轴向外，y轴向内
	plt.rcParams['xtick.direction'] = 'out'
	plt.rcParams['ytick.direction'] = 'in'

	# 绘制feature_distance的折线图
	# mfc为标记的颜色
	plt.plot( x,y, color = 'm',marker = 'o',mfc = 'w',label = 'cos_distance')

	# # 根据对应的目标生成平均值，并将之画到对应图片上
	# average = sum(y) / len(y)
	# y_average = [average] * len(y)
	# plt.plot( x,y_average,color = 'r',linestyle = ':',mfc = 'w',label = 'average_distance')

	# 标记上对应坐标点
	for i,j in zip(x,y):
		plt.text(i,j+0.05,'({},{})'.format(i,round(j,2)))

	# # 上界线
	# average_up =average+10
	# y_average_up = [average_up] * len(y)
	# plt.plot(x, y_average_up, color='g', linestyle=':', mfc='w', label='average_distance_up')
	#
	# # 下界限
	# average_down =average-10
	# y_average_down = [average_down] * len(y)
	# plt.plot(x, y_average_down, color='g', linestyle=':', mfc='w', label='average_distance_down')

	# 指定标题和左右坐标题目
	plt.title("the feature distance of each frame")
	plt.xlabel('frame index')
	plt.ylabel('feature distance')

	# 打开网格线
	plt.grid(axis = 'y')
	plt.show()

def grab_frame_video(
		video_file:str,
		frame_dir:str
):
	'''
	处理视频，并抓取每一帧，并生成对应json文件
	:param video_file:
	:param frame_dir:
	:return:
	'''

	# 初始化帧对应json文件和特征距离集合
	feature_distance = list()
	video_json = dict()
	frame_index = list()

	# 初始化处理帧
	capture = cv2.VideoCapture(video_file)
	success = True
	count = 0
	while success:
		# 读取每一帧
		success,image = capture.read()
		frame_path = os.path.join(frame_dir,str(count) + '.jpg')
		print('read %d frame'%count)
		count += 1
		# 间隔十帧去一帧
		if count % 10 != 0:
			continue
		cv2.imwrite(frame_path, image)

		# 根据当前帧生成对应字典，然后保存为对应json文件



		# print(type(image))
		if image is not None:
			shape = GenJson.gen_json_item_frame(frame_path, image)
			video_json.update(shape)
			# print(shape)
			feature_distance.append(feature_point_distance.o_cos_distance(shape[frame_path]['feature_point']))
			frame_index.append(count)

	# 将feature_distance进行更新，转变为梯度
	with open(r'/cumulate_data/a.txt', 'w+') as f:
		for i in feature_distance:
			f.write(str(i) + '\n')

	# 将生成的完整json文件进行保存
	GenJson.save_json(video_json, os.path.join(frame_dir, 'video.json'))

	# 将对应list画成图
	feature_distance_grade = [feature_distance[0]]
	for i in range(1,len(feature_distance)):
		feature_distance_grade.append(feature_distance[i] - feature_distance[i-1])
	draw_plot(frame_index,feature_distance_grade)

if __name__ == '__main__':

	# ap = argparse.ArgumentParser()
	# ap.add_argument("-u", "--urls", required=True,
	# 				help="path to file containing image URLs")
	# ap.add_argument("-o", "--output", required=True,
	# 				help="path to output directory of images")
	# args = vars(ap.parse_args())
	#
	video_file = r'..\dataset\video\WIN_20220302_14_46_35_Pro.mp4'
	frame_dir = r'../../dataset/video/WIN_20220302_14_46_35_pro'
	grab_frame_video(video_file,frame_dir)
