# sh-tools
整理常用的脚本

## 备忘执行命令
### nohup命令

  nohup [command] parameter
  
  nohup ./gitStore/sh-tools/scan_images.sh ~/mnt/smb/cgg_NAS-05718-08027/百度网盘/52cos

#### kill nohup
  nohup可以进行后台运行程序，不会因为会话断开而中断程序。 但是通过kill无法终止程序，必须使用kill -9 pid 使用jobs -l 查看程序列表 kill -9 pid 杀死进程
