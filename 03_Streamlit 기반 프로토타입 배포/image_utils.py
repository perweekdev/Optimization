import numpy as np
from PIL import Image, ImageOps
import cv2

def preprocess(canvas_image_array):
    """
    캔버스 RGBA -> MNIST (1,1,28,28) 텐서
    canvas_image_array: (H,W,4) RGBA numpy array
    """
    if canvas_image_array is None:
        return None, None
    
    # PIL Image 변환 및 그레이스케일
    img = Image.fromarray(canvas_image_array.astype("uint8")).convert("L")
    
    # 크기 조정 및 이진화 (Otsu)
    img = img.resize((28, 28), Image.Resampling.LANCZOS)
    img_np = np.array(img)
    
    # Otsu 이진화로 노이즈 제거
    _, img_binary = cv2.threshold(img_np, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 색 반전 (흰 배경 검정 글씨 → 검정 배경 흰 글씨)
    img_binary = 255 - img_binary
    
    # 정규화 및 텐서 변환
    img_tensor = img_binary.astype(np.float32) / 255.0
    img_tensor = img_tensor.reshape(1, 1, 28, 28)
    
    # 시각화용 PIL 이미지
    viz_img = Image.fromarray((img_binary).astype(np.uint8))
    
    return img_tensor, viz_img
