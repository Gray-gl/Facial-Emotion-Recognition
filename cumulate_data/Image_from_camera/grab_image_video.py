import csv

import dlib
import os
import cv2
import numpy
from numpy import random

from Tools import GenJson
from cumulate_data.Image_from_camera.cumulate_image_video_file import draw_plot
from Tools import feature_point_distance
'''
主要运行的逻辑：
    1、读取视频
    2、获取每一帧
    3-21、处理每一帧：获取128维度特征向量，保存为对应dict的item
    4、将整个dict保存为对应的json文件
'''
# 当需要将当前的py文件以命令行的形式执行时打开
# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-o", "--output_dir", required=True,
#                 help="path to input image")
# ap.add_argument("-m", "--mode", required=True,
#                 help="0 use your camera in your computer and 1 represents the video you update")
# ap.add_argument("-i", "--input_video", required=True,
#                 help="the video you want to analyse")
# args = vars(ap.parse_args())

# Dlib 正向人脸检测器
detector = dlib.get_frontal_face_detector()

# Dlib 人脸预测器
predictor = dlib.shape_predictor(r"C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\Tools\shape_predictor_68_face_landmarks.dat")

# Dlib 人脸识别模型
# Face recognition model, the object maps human faces into 128D vectors
face_rec = dlib.face_recognition_model_v1(r"C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\Tools\dlib_face1.dat")



# 改变图片的亮度与对比度
def relight(img, light=1, bias=0):
    w = img.shape[1]
    h = img.shape[0]
    for i in range(0, w):
        for j in range(0, h):
            for c in range(3):
                tmp = int(img[j, i, c] * light + bias)
                if tmp > 255:
                    tmp = 255
                elif tmp < 0:
                    tmp = 0
                img[j, i, c] = tmp
    return img


# 返回单张图像的 128D 特征
def return_128d_features(path_img):
    # img_rd = io.imread(path_img)
    img_gray = cv2.cvtColor(path_img, cv2.COLOR_BGR2RGB)
    faces = detector(img_gray, 1)

    print("%-40s %-20s" % ("检测到人脸的图像 / image with faces detected:", path_img), '\n')

    # 因为有可能截下来的人脸再去检测，检测不出来人脸了
    # 所以要确保是 检测到人脸的人脸图像 拿去算特征
    if len(faces) != 0:
        shape = predictor(img_gray, faces[0])
        face_descriptor = face_rec.compute_face_descriptor(img_gray, shape)
        print(face_descriptor)
    else:
        face_descriptor = 0
        print("no face")

    return face_descriptor


def grab_frame_video(
        video_file: str,
        output_dir: str,
        size=64
):
    '''
	处理视频，并抓取每一帧，并生成对应json文件，同时绘制出所有帧的特征向量
	:param video_file: 需要加载的视频的路径
	:param output_dir: 将视频的关键帧进行保存的路径
	:return:
	'''

    # 初始化帧对应json文件和特征距离集合
    global feature_mean_distance
    if size is None:
        size = [64, 64]
    feature_distance = list()

    # 在输出目录中创建保存关键帧文件
    peakframe = os.path.join(output_dir,'peakframe')
    os.mkdir(peakframe)
    # 创建commonframe临时保存中间帧
    commonframe = os.path.join(output_dir, 'commonframe')
    os.mkdir(commonframe)

    # 初始化处理帧
    capture = cv2.VideoCapture(video_file)
    success = True
    count = 1
    index = 0
    while success:
        print('处理第%d帧'%count)

        # 读取每一帧,转成灰度图片，并进行人脸检测
        success, image = capture.read()

        if image is not None:
            gray_img = cv2.cvtColor(image.astype('uint8'), cv2.COLOR_BGR2GRAY)
            dets = detector(gray_img, 0)

        # 设置帧读取的间隔
        count = count + 1
        if count % 10 != 0:
            continue

        # 遍历每一个检测出来的人脸，生成对应json文件，获取特征点
        for i, d in enumerate(dets):
            # 获得识别出的人脸框的具体坐标
            x1 = d.top() if d.top() > 0 else 0
            y1 = d.bottom() if d.bottom() > 0 else 0
            x2 = d.left() if d.left() > 0 else 0
            y2 = d.right() if d.right() > 0 else 0
            face = image[x1:y1, x2:y2]

            # 调整图片的对比度与亮度，对比度与亮度值都取随机数，这样能增加样本的多样性
            # face = relight(face, random.uniform(0.5, 1.5), random.randint(-50, 50))
            face = cv2.resize(face, (size, size))
            feature_128d = return_128d_features(face)
            feature_distance.append(numpy.array(feature_128d))

            # 保存图片，并展示图片
            print("read %d frame" % count)
            frame = os.path.join(commonframe,str(index) + '.jpg')
            cv2.imwrite(frame, face)
            cv2.imshow('image', face)
            index = index + 1

    # 将当前视频的128维度的特征向量进行输出保存
    with open(output_dir + r'\a.csv',  "w+", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(map(lambda x: [x], feature_distance))

    # 将对应list画成图，首先求取128维度特征向量的均值，然后计算各个特征值到均值的距离
    if feature_distance:
        feature_mean_distance = numpy.array(feature_distance,dtype=object).mean(axis = 0)
    else:
        feature_distance = '0'

    # 计算欧式距离
    o_distance = list()
    for i in feature_distance:
        o_distance.append(feature_point_distance.return_euclidean_distance(i,feature_mean_distance))

    # 生成坐标索引，并进行的绘图
    x_index = [i for i in range(0,len(o_distance))]
    draw_plot(x_index,o_distance)

    # 遍历每一个关键帧的欧氏距离，同时比较阈值并获取关键帧
    for i in range(len(o_distance)):
        if o_distance[i] >= 0.20:
            # 获取对应的关键帧，并进行展示
            img = cv2.imread(os.path.join(commonframe,str(i) + '.jpg'),1)
            cv2.imshow('peakframe',img)
            cv2.destroyAllWindows()

            # 将图片重新保存
            frame = os.path.join(peakframe,str(i)+'.jpg')
            cv2.imwrite(frame, img)
            # os.remove(commonframe)



if __name__ == '__main__':
    # 设置重塑的大小
    size = 64
    input_video = r'C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\dataset\video\WIN_20220302_14_46_35_pro\WIN_20220319_15_01_22_Pro.mp4'
    output_dir = r'C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\dataset\video\WIN_20220302_14_46_35_pro'
    # 从视频中抓取帧，并绘制对应表情信息图
    grab_frame_video(input_video,output_dir,size)
