import cv2
import numpy as np

#연산영역을 줄이기 위한 ROI 설정
def InterestRegion(frame, width, height):
    frame = np.array(frame, dtype=np.uint8)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0,0,0])
    upper_white = np.array([255,255,255])

    mask_white = cv2.inRange(rgb, lower_white, upper_white)
    res = cv2.bitwise_and(frame, frame, mask=mask_white)
    
    area = np.array([[(width*0.4,0),(0,height),(0,height), (width,height),(width*0.7,0)]], np.int32) # Area 지정
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, area, color=(255,255,255)) # 관심영역 내부를 색칠한 이미지 생성
    
    interestarea = cv2.bitwise_and(res, mask) # 원본 이미지와 교집합 구하기
    
    return interestarea