#!/bin/bash

CAM_num=$(($(ls /home/jetson/Desktop/CAM_SEND -l | wc -l)-1))
new_CAM_num=$(($(ls /home/jetson/Desktop/CAM_SEND -l | wc -l)-1))
password="raspberry"
echo $CAM_num
echo $new_CAM_num
while :
do
    new_CAM_num=$(($(ls /home/jetson/Desktop/CAM_SEND -l | wc -l)-1))
    if [ $new_CAM_num -gt $CAM_num ]
    then
        echo "start to send a zip"
        #scp -o "StrictHostKeyChecking no" -o "UserKnownHostsFile /dev/null" -o "PreferredAuthentications password" -o "PasswordAuthentication yes" /home/jetson/Desktop/CAM_SEND/* pi@10.10.141.75:~/Desktop/CAM/
        #sshpass -p $password scp /home/jetson/Desktop/CAM_SEND/* pi@10.10.141.75:~/Desktop
        sshpass -p $password scp /home/jetson/Desktop/CAM_SEND/* pi@10.10.141.219:~/Desktop/CAM
        echo "send a file"
        
        rm -r /home/jetson/Desktop/CAM_SEND/*
        echo "delet zip file"
    fi
    sleep 1
done