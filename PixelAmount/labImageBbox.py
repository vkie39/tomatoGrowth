import cv2
import numpy as np
import matplotlib.pyplot as plt

# RGB 이미지 읽기
image = cv2.imread('sampleImage/sample1.jpeg')
lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)  # OpenCV는 기본적으로 BGR이므로 LAB로 변환

# Detection 후 BBOX 출력 Code 작성
detections = [
    # 예시 바운딩 박스 (x1, y1, x2, y2)
    {"bbox": [0,0,220,220]},  # 좌상단 (x1, y1), 우하단 (x2, y2)
]

for detection in detections:
    x1, y1, x2, y2 = detection["bbox"]

    # 바운딩 박스 내의 이미지 영역 추출
    roi = lab_image[y1:y2, x1:x2]

    # A 채널 추출
    _, A, _ = cv2.split(roi)

    # 빨간색과 초록색 픽셀 개수 초기화
    red_area = 0
    green_area = 0
    remain_area = 0

    # 반복문으로 픽셀 하나씩 검사하여 빨간색, 초록색 픽셀 개수 세기
    height, width = A.shape
    for i in range(height):
        for j in range(width):
            print(A[i,j])
            if A[i, j] > 150:  # A 값이 양수인 경우 빨간색
                red_area += 1
            elif A[i, j] < 110:  # A 값이 음수인 경우 초록색
                green_area += 1
            else:
                remain_area += 1


    # 면적 비율 계산
    total_area = height * width
    green_ratio = green_area / total_area if total_area != 0 else 0
    red_ratio = red_area / total_area if total_area != 0 else 0
    remain_ratio = remain_area / total_area if total_area != 0 else 0

    # LAB 이미지에 바운딩 박스와 텍스트 그리기
    cv2.rectangle(lab_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
    cv2.putText(lab_image, f"Green Ratio: {green_ratio:.2%}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(lab_image, f"Red Ratio: {red_ratio:.2%}", (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(lab_image, f"Remain Ratio: {remain_ratio:.2%}", (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    print("BBOX", {x1}, {y1}, {x2}, {y2})
    print(f"Green to total Area Ratio : {green_ratio:.2%}")
    print(f"Red to total Area Ratio : {red_ratio:.2%}")
    print(f"Remain to total Area Ratio : {remain_ratio:.2%}")

    print("total_area = ", total_area)
    print("red_area = ", red_area)
    print("green_area = ", green_area)
    print("remain_area = ", remain_area)

plt.imshow(lab_image)
plt.show()
