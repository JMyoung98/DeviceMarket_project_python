import cv2
import LaneRecog as lr
import torch
import os
import numpy
from utils.general import scale_boxes, non_max_suppression
from utils.torch_utils import select_device, time_sync
from models.experimental import attempt_load
import datetime

#폴더 생성 함수
def createFolder(directory):
        '''
        Create folder
            create a folder if it does not exist
        '''
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print ('Error: Creating directory. ' +  directory)

# YOLOv5 weight 파일 경로
weight = '/home/jetson/Desktop/yolov5/pothol_model.pt'

# GPU or CPU 디바이스 설정
device = select_device('')

# YOLOv5 모델 로드
model = attempt_load(weight,device=device)
# YOLOv5 inference 설정값
conf_thres = 0.5
iou_thres=0.45
file='/home/jetson/Desktop/yolov5/Bike_Lane2023-03-16_17:44:51.avi'
file2 = '/home/jetson/Desktop/yolov5/Bike_Lane_151146.avi'
# 웹캠 캡쳐 객체 생성
cap = cv2.VideoCapture(0)
pothole_idx = None

# 입력 이미지 크기
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
fps = cap.get(cv2.CAP_PROP_FPS)
frame_cnt = 0
frame_cnt_save = 0
# 텍스트 출력 폰트 설정
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 3

#변수 설정
i = 0
k = 0
oldnow = 0
model_oldnow=0
minute =0
cnt = 0
frame_skip = 5
pre_time= datetime.datetime.now()
pre_HMS=pre_time.strftime('%H%M%S')
pre = pre_HMS

#폴더 및 파일을 만들기위한 루프
while True:        
    createFolder(f'/home/jetson/Desktop/CAM/{pre_HMS}') # CAM폴더 만들기
    f = open(f'/home/jetson/Desktop/CAM/{pre_HMS}/CapList_{pre_HMS}.csv','w')
    f.write('time,image,pothole\n')
    # 웹캠 프레임 읽기 루프
    while True:
        # 프레임 읽기
        ret , frame = cap.read()
        
        # 프레임이 없으면 루프 탈출
        if not ret:
            i = 20 #불피요한 while문 반복을 막기위해
            break
        fps_cnt +=1
        cur_time= datetime.datetime.now()
        top = lr.top_view(frame,width,height)
        interest = lr.InterestRegion(frame,width,height)
        canny = lr.Canny(interest)
        #cv2.imshow('can',canny)
        # 원본 이미지 RGB 색상채널 순서로 변경
        img = interest[:,:,::-1]

        # 입력 이미지 크기로 Resize
        img = cv2.resize(img,(width,height))

        # 넘파이 배열 -> 파이토치 텐서 변환
        img = torch.from_numpy(img).to(device=device)

        # 텐서의 차원 변경, 정규화
        img = img.permute(2,0,1).float().unsqueeze(0)/255.0

        # YOLOv5 inference
        with torch.no_grad():
            time1 = time_sync()
            pred = model(img)[0]
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes = None, agnostic=False)
            time2 = time_sync()
        # YOLOv5 detection 결과가 있을 경우
        if len(pred) > 0:   #len(pred) -> 인식한 객체의 갯수
            pred = pred[0]
            # 박스 좌표 스케일링
            pred[:,:4] = scale_boxes(img.shape[2:],pred[:,:4],frame.shape).round()
            # 박스 그리기와 클래스명, 신뢰도 출력
            for *xyxy, conf, cls in reversed(pred):
                label = f'{model.names[int(cls)]}{conf:.2}'                
                print(label)
                

                cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 0, 255), 2)
                cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1])-10), font, font_scale, (0, 255, 255), font_thickness)
                
                #객체가 pothole인 경우
                if model.names[int(cls)] == 'pothole':
                    now = datetime.datetime.now()
                    now_HMS=now.strftime('%H%M%S')
                    
                    # 이전 프레임에서 이미지를 저장한 마지막 frame_cnt_save와
                    # frame_cnt의 차이가 fps 이상인 경우에만 이미지를 저장합니다.
                    if (frame_cnt - frame_cnt_save >= (fps)): 
                        cv2.imwrite(f'/home/jetson/Desktop/CAM/{pre_HMS}/Capture_{now_HMS}.jpg',frame)
                        f.write(f'{now_HMS},Capture_{now_HMS}.jpg,{len(pred)}\n')
                        frame_cnt_save=frame_cnt
        #이전 시간과 현재 시간이 1분 차이가 나게되면 루프 탈출
        if cur_time.minute - pre_time.minute >=1:
            i += 1
            pre_time = cur_time
            pre_HMS = pre_time.strftime('%H%M%S')
            break

        # 프레임 출력
        cv2.imshow('frame', frame)
        
        # q를 누르면 루프 탈출
        if cv2.waitKey(1) & 0xFF == ord('q'):
            i = 20
            break
    f.close()
    #폴더가 존재하면 폴더안의 csv파일과 모든 이미지를 다른폴더에 압축
    if os.path.exists(f'/home/jetson/Desktop/CAM/{pre}'):
        os.system(f'zip -j /home/jetson/Desktop/CAM_SEND/CAM_ZIP{k}.zip /home/jetson/Desktop/CAM/{pre}/*')
        k += 1
    pre = pre_HMS

    if i == 20:
        break
            
cap.release()
cv2.destroyAllWindows()
