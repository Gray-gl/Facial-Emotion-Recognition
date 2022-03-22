'''
    功能：过滤所有下载的图片
    流程：
        1、将所有不能识别出人脸的都删除
        2、将所有重复的图片都删除
        3-21、
'''
import os
from os import listdir
from os.path import isfile, join
import cv2
import dlib

# 加载所有的检测，仅仅针对正脸进行检测
from PIL import Image

detector = dlib.get_frontal_face_detector()

def check_corrupt_file(filename):
    if filename.endswith('.jpg'):
        try:
            img = Image.open(filename)  # open the image file
            img.verify()  # verify that it is, in fact an image
        except (IOError, SyntaxError) as e:
            print('Bad file:', filename)
            os.remove(filename)



def detect_face(path_img):
    print(path_img,'111111111111')
    img_rd = cv2.imread(path_img)
    img_gray = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
    faces = detector(img_gray, 0)

    count = 1
    for i, d in enumerate(faces):
        # 获得识别出的人脸框的具体坐标
        x1 = d.top() if d.top() > 0 else 0
        y1 = d.bottom() if d.bottom() > 0 else 0
        x2 = d.left() if d.left() > 0 else 0
        y2 = d.right() if d.right() > 0 else 0
        face = img_rd[x1:y1, x2:y2]
        face = cv2.resize(face, (64, 64))

        # 保存图片，并进行展示
        image_path = path_img.split('.')[0] + str(count)+ '.jpg'
        cv2.imwrite(image_path,face)
        cv2.imshow('image',face)
        count = count + 1
        

    return faces


# 过滤单独的一张图片
def filter_image(file_path):
    print(file_path)
    # 判定是否为图片
    if file_path.endswith('.jpg'):
        # 检测脸部之前，先过滤坏掉的图片
        check_corrupt_file(file_path)

        # 检测人脸
        faces = detect_face(file_path)
        # 为检测到人脸
        if len(faces) == 0:
            print("[INFO]no face")
        else:
            print("[INFO] detect face and subtract the face")
        # 切割完毕人脸之后，可以删除原来的图片了
        os.remove(file_path)


# 读取文件目录下的所有的图片
def filter_image_dir(file_path):
    onlyfiles = [f for f in listdir(file_path) if isfile(join(file_path, f))]
    for i in onlyfiles:
        print(i)
        # 判定是否为图片
        filter_image(i)



#
# mypath = [r"C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\cumulate_data\download_image_online\confused",
#           r"C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\cumulate_data\download_image_online\understanding",
#           r"C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\cumulate_data\download_image_online\distracted",
#           r"C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\cumulate_data\download_image_online\tired",
#           r"C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\cumulate_data\download_image_online\listening"]
# for i in mypath:
#     filter_image_dir(i)

