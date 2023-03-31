#!/bin/bash

CAM_num=$(($(ls /home/jetson/Desktop/CAM_SEND -l | wc -l)-1))
new_CAM_num=$(($(ls /home/jetson/Desktop/CAM_SEND -l | wc -l)-1))
password="raspberry"
echo $CAM_num
echo $new_CAM_num
pre=$(date +%s)
end=$(($pre+1200))
while [ $pre -lt $end ]:
do
    new_CAM_num=$(($(ls /home/jetson/Desktop/CAM_SEND -l | wc -l)-1))
    if [ $new_CAM_num -gt $CAM_num ]
    then
        echo "start to send a zip"
        sshpass -p $password scp /home/jetson/Desktop/CAM_SEND/* pi@192.168.51.200:~/Desktop/CAM # IP set
        echo "send a file"
        
        rm /home/jetson/Desktop/CAM_SEND/*
        echo "delet zip file"
    fi
    sleep 1
done
