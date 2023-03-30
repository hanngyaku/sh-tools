#!/bin/bash

# SMB服务器的IP地址或主机名
SERVER=192.168.0.100

# SMB用户名和密码
USERNAME=cgg
PASSWORD=123456

# 本地挂载点的路径
MOUNT_DIR=~/mnt/smb

# 创建挂载点目录
sudo mkdir -p $MOUNT_DIR

# 循环挂载所有的SMB共享文件夹
for SHARE in $(smbclient -L //$SERVER -U $USERNAME%$PASSWORD | awk '/Disk/ {print $1}' | grep -v '\$')
do
  # 创建SMB共享文件夹对应的本地目录
  sudo mkdir -p "$MOUNT_DIR/$SHARE"
  # 挂载SMB共享文件夹到本地目录
  sudo mount -t cifs //$SERVER/$SHARE "$MOUNT_DIR/$SHARE" -o username=$USERNAME,password=$PASSWORD,iocharset=utf8,rw,dir_mode=0777,file_mode=0777
done

