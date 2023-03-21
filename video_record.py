import cv2
import datetime as dt
#import socket
#s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#host = 'localhost'
#port = 5000
#s.connect((host,port))



try:
    video = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not video.isOpened(): raise Exception("error")
    date = dt.datetime.strftime('%H%M%S')
    
    fps = video.get(cv2.CAP_PROP_FPS)
    delay = int(1000/fps)
    frame_cnt = 1
    width = 640
    height = 480
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    i=1
    cnt=0
    out = cv2.VideoWriter(f'/home/jetson/Desktop/CAM{date}.avi',fourcc,fps,(int(width),int(height)))
except Exception as e:
    print("Exception occurred:", e)
           
while True:
    try:
        cnt = 0
        while(video.isOpened()):
            
            ret, frames = video.read()
            if not ret: break
            cv2.imshow('original',frames)
            out.write(frames)

            cnt = cnt+1
            #print(cnt)
            if(cnt == int(fps*120) or (cv2.waitKey(1)&0xff==ord('q'))):
                date = dt.datetime.now()
                i = i +1
                break
        if 'out' in locals():
            
            out.release()
            
        if(i == 11): break
        out = cv2.VideoWriter(f'/home/jetson/Desktop/CAM{date}.avi',fourcc,fps,(int(width),int(height)))
    except Exception as e:
        print("Exception occurred:", e)
        break
try:
    video.release()
    cv2.destroyAllWindows()
except Exception as e:
    print("Exception occurred:", e)
        

#num = 10
#msg = str(num)
#s.sendall(msg.encode())
#s.close()
