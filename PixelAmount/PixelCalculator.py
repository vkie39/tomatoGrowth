import cv2
import numpy as np
import matplotlib.pyplot as plt

def pixelDetector(img):
    roi = img

    # A 채널 추출
    _, A, _ = cv2.split(roi)

    # 빨간색과 초록색 픽셀 개수 초기화
    red_area = np.nansum(A > 128+14)   #128+21 
    green_area = np.nansum(A < 128-6) #128-10
    if np.isnan(red_area): red_area = 0
    if np.isnan(green_area): green_area = 0
    red_area = int(red_area)
    green_area = int(green_area)
    remain_area = A.size - red_area - green_area

    height, width = A.shape

    # 면적 비율 계산
    # total_area = height * width
    # green_ratio = green_area / total_area if total_area != 0 else 0
    # red_ratio = red_area / total_area if total_area != 0 else 0
    # remain_ratio = remain_area / total_area if total_area != 0 else 0

    if (red_area + green_area != 0):
        growth_ratio = (red_area / (red_area + green_area)) * 100
    else:
        growth_ratio = -1
    if growth_ratio <= 5:    #25
        growth_level = 1
    elif growth_ratio <= 35: #50
        growth_level = 2
    elif growth_ratio <= 75: 
        growth_level = 3
    elif growth_ratio >75:   #else:
        growth_level = 4
    
    return [growth_ratio, growth_level]
    # return [red_area, green_area]

    # print(f"Green:{green_ratio:.2%}, Red:{red_ratio:.2%}")
    # print(f"Green to total Area Ratio : {green_ratio:.2%}")
    # print(f"Red to total Area Ratio : {red_ratio:.2%}")
    # print(f"Remain to total Area Ratio : {remain_ratio:.2%}")

    # print("total_area = ", total_area)
    # print("red_area = ", red_area)
    # print("green_area = ", green_area)
    # print("remain_area = ", remain_area)
