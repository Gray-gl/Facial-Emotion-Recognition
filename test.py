# 本份代码用于利用 Baidu 的人脸检测 API 进行表情检测
# 相关文档地址：https://ai.baidu.com/docs#/Face-Detect-V3/b7203cd6

# 作者：蒲韬，putao3@mail2.sysu.edu.cn
# 　所需依赖：Python 3
# 最后更新时间：2019.07.22

import os
import time
import json
import base64

import urllib
import urllib.request


class AverageMeter(object):
    '''Computes and stores the sum, count and average'''

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, count=1):
        self.val = val
        self.sum += val
        self.count += count
        if self.count == 0:
            self.avg = 0
        else:
            self.avg = float(self.sum) / self.count


# 获取　Access_token
def getAcessToken():
    request = urllib.request.Request(
        'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=xV1lFbF4m4vIoy1sLpRfpR1f&client_secret=8Q3nLI1dQNOx8RSjeUPQh26VfAvc4scq')  # client_id 为官网获取的AK， client_secret 为官网获取的SK
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = json.loads(response.read().decode('utf-8'))  # bytes 转　string
    return content['access_token']


# 读取目标图像并进行 Base64　编码
def getImage(imgPath):
    with open(imgPath, 'rb') as f:  # 以二进制读取图片
        data = f.read()
        encode = base64.b64encode(data)  # 得到 byte 编码的数据
        encode = str(encode, 'utf-8')  # bytes 转　string

    return encode


# 调用　API　进行人脸检测与属性分析
def useAPI(imgPath, access_token):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    params = bytes("{\"image\":\"" + getImage(imgPath) + "\",\"image_type\":\"BASE64\",\"face_field\":\"emotion\"}",
                   'utf-8')  # string 转 bytes

    request_url = request_url + "?access_token=" + access_token
    request = urllib.request.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/json')

    response = urllib.request.urlopen(request)
    content = json.loads(response.read().decode('utf-8'))

    return content


if __name__ == '__main__':

    access_token = getAcessToken()

    # 七类基本表情 -> angry:愤怒 disgust:厌恶 fear:恐惧 happy:高兴 sad:伤心 surprise:惊讶 neutral:无情绪
    Label = {'surprise': 0, 'fear': 1, 'disgust': 2, 'happy': 3, 'sad': 4, 'angry': 5, 'neutral': 6}

    acc, prec, recall = AverageMeter(), [AverageMeter() for i in range(7)], [AverageMeter() for i in range(7)]

    pathName = ['surprised', 'fear', 'disgust', 'happy', 'sad', 'angry', 'neutral']
    for i in range(7):
        Dirs = os.listdir('/media/dm/新加卷/自建数据集/Asian_FacialExpression/data_6/val_filter/' + pathName[i])
        for imgFile in Dirs:
            imgPath = '/media/dm/新加卷/自建数据集/Asian_FacialExpression/data_6/val_filter/' + pathName[i] + '/' + imgFile
            content = useAPI(imgPath, access_token)

            if 'result' not in content.keys() or content['result'] is None:
                continue

            for result in content['result']['face_list']:
                pred = Label[result['emotion']['type']]

                if pred == i:
                    acc.update(1, 1)
                    prec[i].update(1, 1)
                    recall[i].update(1, 1)
                else:
                    acc.update(0, 1)
                    prec[pred].update(0, 1)
                    recall[i].update(0, 1)

            # 免费账号的　QPS 为 ２。（QPS（query per second）指每秒向服务发送的请求数量峰值，相当于每个API每秒可以允许请求的最大上限数量。）
            time.sleep(0.6)

    print('''
    Sample {recall[0].count:d} {recall[1].count:d} {recall[2].count:d} {recall[3].count:d} {recall[4].count:d} {recall[5].count:d} {recall[6].count:d}\t
    Accuracy {acc.avg:.4f}\t
    Precision {prec[0].avg:.4f} {prec[1].avg:.4f} {prec[2].avg:.4f} {prec[3].avg:.4f} {prec[4].avg:.4f} {prec[5].avg:.4f} {prec[6].avg:.4f}\t
    Recall {recall[0].avg:.4f} {recall[1].avg:.4f} {recall[2].avg:.4f} {recall[3].avg:.4f} {recall[4].avg:.4f} {recall[5].avg:.4f} {recall[6].avg:.4f}\t
    '''.format(acc=acc, prec=prec, recall=recall))
