import torch
import cv2
import numpy as np
from PixelAmount.PixelCalculator import pixelDetector

# YOLOv5 모델 로드
model = torch.hub.load('./yolov5', 'custom', './final_model/best.pt', source='local')
model.conf = 0.02
model.max_det = 4

# 웹캠 스트림 열기
cap = cv2.VideoCapture(0)  # 0은 기본 웹캠을 의미

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
else:
    print("카메라가 성공적으로 열렸습니다.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다. 종료합니다.")
        break

    # LAB 색영역 Frame 생성
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB) # BGR -> LAB

    # YOLOv5 모델로 이미지 예측 수행
    results = model(lab)

    # 인식된 오브젝트의 xywh값 받아옴
    detections = results.xywh[0]  # xywh format: (x_center, y_center, width, height)
    for box in detections:
        left, top, right, bottom = map(int, [box[0] - box[2] / 2, box[1] - box[3] / 2,
                                               box[0] + box[2] / 2, box[1] + box[3] / 2])

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  # Draw bounding box
        cv2.putText(frame, f'{results.names[int(box[5])]} {int(100 * box[4])}%',
                    (left, top - 10 if top > 10 else top + 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (255, 255, 255), 2)  # Draw label
        cropped_img = frame[top: bottom, left: right]

    # OpenCV 윈도우에 이미지를 표시
    cv2.imshow('YOLORunner.py', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 리소스 정리
cap.release()
cv2.destroyAllWindows()