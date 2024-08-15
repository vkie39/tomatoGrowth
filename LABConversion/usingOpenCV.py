import os

import cv2

def process_folder_images(input_folder, output_folder):
    
    file_names = os.listdir(input_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for file_name in file_names:
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            try:
                rgb_image = cv2.imread(input_path)
                
                # RGB -> LAB
                lab_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2LAB)
                
                # LAB 이미지 저장 (RGB로 다시 변환 후 png로 변환해야 함)
                cv2.imwrite(output_path,lab_image)
                
                print(f"{file_name} 변환 완료.")
            
            except Exception as e:
                print(f"파일 {file_name} 처리 중 오류 발생: {e}")

input_folder = 'Riped and Unriped tomato Dataset\Images' 
output_folder = 'output\output_cv2' 
process_folder_images(input_folder, output_folder)