# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.use("TkAgg")

base_dir = "./images/"
dst_dir = "./tmp/"
min_val = 10
min_range = 30



count = 0
def extract_peek(array_vals, minimun_val, minimun_range):
    start_i = None
    end_i = None
    peek_ranges = []
    for i, val in enumerate(array_vals):
        if val > minimun_val and start_i is None:
            start_i = i
        elif val > minimun_val and start_i is not None:
            pass
        elif val < minimun_val and start_i is not None:
            if i - start_i >= minimun_range:
                end_i = i
                print(end_i - start_i)
                peek_ranges.append((start_i, end_i))
                start_i = None
                end_i = None
        elif val < minimun_val and start_i is None:
            pass
        else:
            raise ValueError("cannot parse this case...")
    return peek_ranges

#peek_range = extract_peek(horizontal_sum, min_val, min_range)
#line_seg_adaptive_threshold = np.copy(adaptive_threshold)



# cv2.rectangle(img, pt1, pt2, 0)
# cv2.rectangle(line_seg_adaptive_threshold, pt1, pt2, 255)



def work():
    img = cv2.imread("./images/1.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    horizontal_sum = np.sum(adaptive_threshold, axis=1)

    peek_range = extract_peek(horizontal_sum, min_val, min_range)
    line_seg_adaptive_threshold = np.copy(adaptive_threshold)
    
    for fileName in os.listdir(base_dir):
        img = cv2.imread("./images/1.png")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        horizontal_sum = np.sum(adaptive_threshold, axis=1)
        peek_ranges = extract_peek(horizontal_sum, min_val, min_range)
        line_seg_adaptive_threshold = np.copy(adaptive_threshold)
        
    for i, peek_range in enumerate(peek_ranges):
        x = 0
        y = peek_range[0]
        w = line_seg_adaptive_threshold.shape[1]
        h = peek_range[1] - y
        pt1 = (x, y)
        pt2 = (x + w, y + h)
        cv2.rectangle(line_seg_adaptive_threshold, pt1, pt2, 255)
        
    vertical_peek_ranges2d = []

    for peek_range in peek_ranges:
        start_y = peek_range[0]
        end_y = peek_range[1]
        line_img = adaptive_threshold[start_y:end_y, :]
        vertical_sum = np.sum(line_img, axis=0)
        vertical_peek_ranges = extract_peek(vertical_sum, min_val, min_range)
        vertical_peek_ranges2d.append(vertical_peek_ranges)
    
    cutImage(img, peek_range, horizontal_sum, vertical_peek_ranges2d)
    
    
def cutImage(img, peek_range, horizontal_sum, vertical_peek_ranges2d):
    global count
    peek_ranges = extract_peek(horizontal_sum, min_val, min_range)
    for i, peek_range in enumerate(peek_ranges):
        for vertical_range in vertical_peek_ranges2d[i]:
            x = vertical_range[0]
            y = peek_range[0]
            w = vertical_range[1] - x
            h = peek_range[1] - y
            pt1 = (x, y)
            pt2 = (x + w, y + h)
                 
            count += 1
            count = "%05d" %count
            
            img1 = img[y:peek_range[1], x:vertical_range[1]]
            new_shape = (64, 64)
            img1 = cv2.resize(img1, new_shape)  
            gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
            cv2.imwrite(dst_dir + count + ".png", adaptive_threshold)
            count = int(count)


