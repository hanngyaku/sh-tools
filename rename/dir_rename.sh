#!/bin/bash

# 检查参数是否正确
if [ $# -ne 3 ]; then
    echo "Usage: $0 path file mode"
    exit 1
fi

# 逐行读取文件内容，并对每行进行处理
while read line; do
  # 提取角色名和文件夹名
  old_name=$(echo $line | awk -F, '{print $1}')
 
  # echo $role_name
  suf_name=$(echo $line | awk -F, '{print $2}')

  #new_folder_name=$(echo $line | awk -F, '{print $2$1}')
  # echo $folder_name
  # 构造新的文件夹名
  new_folder_name="${suf_name}${old_name:5}"
  echo $new_folder_name
  # echo $new_floder_name
  # 执行重命名操作
  mv "$1/${old_name}" "$1/${new_folder_name}"
  # echo " mv "$1/${old_name}" "$1/${new_folder_name}""

 
  #echo "mv "${folder_name}" "${name}""
done < "${2}"
