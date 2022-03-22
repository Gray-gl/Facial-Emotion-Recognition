#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

中心放缩代码实现，用于去除关键帧中问题

Author: Gray_Gl
Last edited: February  2022
"""
import json
import os
import cv2
import os
import binascii
def get_min(a,b):
    if a > b:
        return b
    else:
        return a

def get_max(a,b):
    if a > b:
        return a
    else:
        return b

def read_img_from_bin_file(in_filename,list_data):
    with open(in_filename,'rb') as fd:    #open file
        fd.seek(0,0)                    #relocate fd
        while True:                        #while loop
            t_byte = fd.read(1)            #read one byte
            if len(t_byte) == 0:        #if reach the end of the file then break
                break
            else:                        #store the the t_byte into hex format
                list_data.append(ord(t_byte))
    fd.close()

def img_scale_fuc(in_list_data,srcW,srcH,dstW,dstH,out_list_data):
    rateW = (srcW*1.0 / dstW)
    rateH = (srcH*1.0 / dstH)
    data  = 0
    for i in range(0,dstH):
        temp = rateH * (i + 0.5) -0.5
        y0 = int(temp)
        u = temp - y0
        y0 = get_max(0,get_min(y0,srcH - 2))
        y1 = get_min((y0 + 1),(srcH - 1))
        for j in range(0,dstW):
            temp = rateW * (j + 0.5) - 0.5
            x0 = int(temp)
            v = temp - x0
            x0 = get_max(0,get_min(x0,srcW - 2))
            x1 = get_min((x0 + 1),(srcW - 1))
            w0 = ((1 - u)*(1 - v))
            w1 = ((1 - u)*v)
            w2 = (u*(1 - v))
            w3 = (u*v)
            p0 = in_list_data[y0*srcW + x0]
            p1 = in_list_data[y1*srcW + x0]
            p2 = in_list_data[y0*srcW + x1]
            p3 = in_list_data[y1*srcW + x1]
            #f(i+u,j+v) = (1-u)(1-v)f(i,j) + (1-u)vf(i,j+1) + u(1-v)f(i+1,j) + uvf(i+1,j+1)
            data = int(w0*p0+w1*p1+w2*p2+w3*p3)
            out_list_data.append('%.2X' % data)

def write_data_to_text(out_filename,out_list_data):
    with open(out_filename,'wb') as fd:
        fd.seek(0,0)
        for data in out_list_data:
            fd.write(binascii.a2b_hex(data))
    fd.close()

list_data = []
out_list_data = []

in_filename = raw_input("Please input src file name:\n")
out_filename = raw_input("Please input dst file name:\n")
srcH = input("Please input srcH:\n")
srcW = input("Please input srcW:\n")
dstH = input("Please input dstH:\n")
dstW = input("Please input dstW:\n")

read_img_from_bin_file(in_filename,list_data)
img_scale_fuc(list_data,srcW,srcH,dstW,dstH,out_list_data)
write_data_to_text(out_filename,out_list_data)