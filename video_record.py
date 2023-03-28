import cv2
from datetime import datetime


try:
    video = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not video.isOpened(): raise Exception("error")
    fps = video.get(cv2.CAP_PROP_FPS)
    delay = int(1000/fps)
    frame_cnt = 1
    width = 640
    height = 480
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    i=0
except Exception as e:
    print("Exception occurred:", e)

pre_time = datetime.now()
pre_time_name = pre_time.strftime('%H%M%S')
while True:
    try:
        out = cv2.VideoWriter(f'/home/jetson/Desktop/CAM/CAM_{pre_time_name}.avi',fourcc,fps,(int(width),int(height)))
        cnt = 0
        while(video.isOpened()):
            ret, frames = video.read()
            if not ret: break
            cv2.imshow('original',frames)
            out.write(frames)

            cur_time = datetime.now()
            if (cur_time.minute - pre_time.minute >= 2):
                pre_time = cur_time
                pre_time_name = pre_time.strftime('%H%M%S')
                i = i +1
                break
            if cv2.waitKey(1)&0xff==ord('q') :
                i = 10
                break
            
        if 'out' in locals():
            out.release()
            
        if(i == 10): break
    except Exception as e:
        print("Exception occurred:", e)
        break
try:
    video.release()
    cv2.destroyAllWindows()
except Exception as e:
    print("Exception occurred:", e)
        
