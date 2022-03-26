import os
import time
from selenium import webdriver
# 使用测试软件打开对应浏览器，并跳转到图片搜索框
from selenium.webdriver.common.keys import Keys
# 将png图片，转为jpg图片
import cv2
from os.path import exists
from cumulate_data.download_image_online.filter_image import filter_image

def get_picture(key_word,label_file):
    '''

    :param key_word: 关键字对应的标签
    :param label_file:当前关键字对应标签文件
    :return:
    '''
    driver = webdriver.Chrome(r"D:\graduationDesign\chromedriver.exe")
    driver.get('https://www.google.ca/imghp?hl=en&tab=ri&authuser=0&ogbl')
    # driver.get('https://image.baidu.com/')

    # 获取搜索框输入的信息，并输入需要的内容
    box = driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')
    # box = driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')
    # // *[ @ id = "sbtc"] / div / div[2] / input
    # box = driver.find_element_by_xpath('//*[@id="kw"]')
    box.send_keys(key_word)
    box.send_keys(Keys.ENTER)


    #实现不停的下来网页，直到下拉到网页的底部
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:

        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)
        new_height = driver.execute_script('return document.body.scrollHeight')
        try:
            driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
            time.sleep(2)
        except:
            pass
        if new_height == last_height:
            break
        last_height = new_height

    # 爬取两百张图片
    for i in range(1,2000):
        try:
            # 在对应类别下进行创建
            base_path = os.path.join(r'C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\cumulate_data\download_image_online',label_file)
            # base_path = os.path.join(base_path,key_word)
            # 判定文件是否存在
            if not exists(base_path):
                os.mkdir(base_path)
            path =os.path.join( base_path,str(i) + '.png')
            # //*[@id="imgid"]/div[1]/ul/li[1]/div/div[2]/a/img
            # //*[@id="imgid"]/div[1]/ul/li[2]/div/div[2]/a/img
            # driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img')\
            driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img').screenshot(path)
            # driver.find_element_by_xpath('//*[@id="imgid"]/div[1]/ul/li['+str(i)+']/div/div[2]/a/img').screenshot(path)

            print(path)
            # 将png图片转为jpg图片
            png_img = cv2.imread(path)
            os.remove(path)
            path = path.split('.')[0]+'.jpg'
            # 保存为jpg格式
            cv2.imwrite(path, png_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            # 对图片进行检测
            filter_image(path)
        except:
            pass

    driver.close()

if __name__ == '__main__':
    # 下述为相关的同义词，或者相同场景的词语
    # key_word = {'distracted':['distracted']}
    key_word = {'distracted':[],
                'understanding':[],
                'tired':[],
                'listening':[],
                'confused':[]}
    for i in key_word.keys():
        for j in key_word[i]:
            print(j)
            get_picture(j,i)
