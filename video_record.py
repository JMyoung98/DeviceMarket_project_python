import cv2
from datetime import datetime

# 웹캠 캡쳐 객체 생성
video = cv2.VideoCapture(0, cv2.CAP_V4L2)
if not video.isOpened(): raise Exception("error")

#변수 설정
fps = video.get(cv2.CAP_PROP_FPS)
frame_cnt = 1
width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
i=0
pre_time = datetime.now()
pre_time_name = pre_time.strftime('%H%M%S')

#비디오 파일 저장을 위한 루프
while True:
    out = cv2.VideoWriter(f'/home/jetson/Desktop/CAM/CAM_{pre_time_name}.avi',fourcc,fps,(int(width),int(height)))
    cnt = 0
    # 웹캠 프레임 읽기 루프
    while(video.isOpened()):

        ret, frames = video.read()
        if not ret: break
        
        cv2.imshow('original',frames)
        out.write(frames)
        cur_time = datetime.now()
        
        #이전 시간과 현재 시간의 차이가 2분이라면 루프문 탈출
        if (cur_time.minute - pre_time.minute >= 2):
            pre_time = cur_time
            pre_time_name = pre_time.strftime('%H%M%S')
            i = i +1
            break

        # q를 누를시 강제로 루프문 탈출
        if cv2.waitKey(1)&0xff==ord('q') :
            i = 10
            break

    #동영상파일이 있다면 조건문 실행 
    if 'out' in locals():
        out.release()
    
    #10개의 파일이 만들어지면 루프문 탈출
    if(i == 10): break

video.release()
cv2.destroyAllWindows()