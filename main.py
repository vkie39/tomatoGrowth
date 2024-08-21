import torch
import cv2
import numpy as np
from PixelAmount.PixelCalculator import pixelDetector
import pathlib

#윈도우 파일시스템 경로를 사용하기 위해 추가
pathlib.PosixPath = pathlib.WindowsPath


# YOLOv5 모델 로드
model = torch.hub.load('./yolov5', 'custom', 'final_model/best.pt', source='local')
model.conf = 0.02
model.max_det = 4

# 웹캠 스트림 열기
cap = cv2.VideoCapture(0)  # 0은 기본 웹캠을 의미

# 프레임 크기 설정 추가
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # 너비
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # 높이

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
else:
    print("카메라가 성공적으로 열렸습니다.")

while cap.isOpened():

    #각 레벨에 해당하는 토마토 수를 세기 위한 변수
    harvest_now = 0
    harvest_soon = 0
    harvest_after = 0

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
        
        cropped_img = lab[top: bottom, left: right]
        level = pixelDetector(cropped_img)

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  # Draw bounding box
        cv2.putText(frame, f'{results.names[int(box[5])]} {int(100 * box[4])}%',
                    (left, top - 40 if top > 40 else top + 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (255, 255, 255), 2)  # Draw label
        cv2.putText(frame, f'Ratio:{level[0]:.2f} LEVEL:{level[1]}',
                    (left, top - 10 if top > 10 else top + 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (255, 255, 255), 2)  # Draw label
        

        # 각 레벨에 해당하는 토마토 수를 세어 수확가능한 토마토 수를 터미널로 출력
        if level[1] >= 3 :
            harvest_now = harvest_now + 1
        elif level[1] >= 2 :
            harvest_soon = harvest_soon + 1
        else : 
            harvest_after = harvest_after + 1
        
        

    # OpenCV 윈도우에 이미지를 표시
    cv2.imshow('tomato growth detector', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#터미널에 출력
print("수확 가능한 토마토의 수 : ", harvest_now)
print("2주후 수확 가능한 토마토 수 : ", harvest_soon )
print("녹숙기 토마토 수 : ", harvest_after )


# 리소스 정리
cap.release()
cv2.destroyAllWindows()