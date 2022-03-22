# import the necessary packages
from imutils import paths
import numpy as np
import argparse
import cv2
import os

# 为每一张图片创造一个hash值，用来进行区分
def dhash(image, hashSize=8):
    # 将图片转为灰度模式，并调整大小，同时增加一单独的一列，表示宽度
    # 计算图片的水平梯度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (hashSize + 1, hashSize))
    # 计算相邻列之间的水平梯度
    diff = resized[:, 1:] > resized[:, :-1]
    # 将不同的图片转为一个hash并进行转变
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
# dataset  需要处理重复图片的数据集的路径
ap.add_argument("-d", "--dataset", required=True,
    help="path to input dataset")
# remove 指定运行模式，是真正的删除数据，还是临时测试
ap.add_argument("-r", "--remove", type=int, default=-1,
    help="whether or not duplicates should be removed (i.e., dry run)")
args = vars(ap.parse_args())

# grab the paths to all images in our input dataset directory and
# then initialize our hashes dictionary
print("[INFO] computing image hashes...")
print(args["dataset"])
imagePaths = list(paths.list_images(args["dataset"]))
print(imagePaths)
hashes = {}

# loop over our image paths
for imagePath in imagePaths:
    # load the input image and compute the hash
    image = cv2.imread(imagePath)
    h = dhash(image)
    # grab all image paths with that hash, add the current image
    # path to it, and store the list back in the hashes dictionary
    # 从原来字典中获取h对应value，如果value不存在，就返回一个空的list
    p = hashes.get(h, [])
    p.append(imagePath)
    hashes[h] = p

# 遍历字典中的每一项，并且删除特定hash值
# loop over the image hashes
for (h, hashedPaths) in hashes.items():
    # check to see if there is more than one image with the same hash
    if len(hashedPaths) > 1:
        # check to see if this is a dry run
        if args["remove"] <= 0:
            # initialize a montage to store all images with the same
            # hash
            montage = None
            # loop over all image paths with the same hash
            for p in hashedPaths:
                # load the input image and resize it to a fixed width
                # and heightG
                image = cv2.imread(p)
                image = cv2.resize(image, (150, 150))
                # if our montage is None, initialize it
                if montage is None:
                    montage = image
                # otherwise, horizontally stack the images
                else:
                    montage = np.hstack([montage, image])
            # show the montage for the hash
            print("[INFO] hash: {}".format(h))
            # 展示所有相同的图片
            cv2.imshow("Montage", montage)
            cv2.waitKey(0)
        # otherwise, we'll be removing the duplicate images
        else:
            # loop over all image paths with the same hash *except*
            # for the first image in the list (since we want to keep
            # one, and only one, of the duplicate images)
            print("[INFO] delete {}".format(p))
            for p in hashedPaths[1:]:
                os.remove(p)


##########################################
# 执行的命令,注意切换到当前python文件所在目录
# python remove_duplicate.py --dataset ./tired --remove 1
##########################################