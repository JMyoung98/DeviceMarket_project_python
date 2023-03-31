#!/bin/bash
remote_script='/home/pi/Desktop/collect_IMU_GPS.sh &'
remote_user='pi'
remote_host='192.168.51.200'
remote_password='raspberry'
# 원격 서버에서 스크립트 실행
sshpass -p "$remote_password" ssh "$remote_user@$remote_host" "$remote_script"
/home/jetson/Desktop/send2PI.sh
