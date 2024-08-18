import os
from skimage import io, color
import numpy as np
from PIL import Image

def process_folder_images(input_folder, output_folder):

    file_names = os.listdir(input_folder)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in file_names:

        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            try:
                rgb_image = io.imread(input_path)
                
                # RGB -> LAB
                lab_image = color.rgb2lab(rgb_image)
                
                # LAB 이미지 범위 변환 (0-255) 
                lab_image_normalized = (lab_image + [0, 128, 128]) / [100, 255, 255] * 255.0
                lab_image_normalized = lab_image_normalized.astype(np.uint8)
                
                # LAB 이미지 저장 (RGB로 다시 변환 후 png로 변환해야 함)
                lab_image_pil = Image.fromarray(lab_image_normalized, mode="RGB") 
                lab_image_pil.save(output_path, "PNG") #jpg로는 save되지 않음
                
                print(f"{file_name} 변환 완료.")
            
            except Exception as e:
                print(f"파일 {file_name} 처리 중 오류 발생: {e}")

input_folder = 'sampleImage'   
output_folder = 'sampleImage' 
process_folder_images(input_folder, output_folder)
