#!/bin/bash

# 检查参数是否正确
if [ $# -ne 3 ]; then
    echo "Usage: $0 path file mode"
    exit 1
fi

# 逐行读取文件内容，并对每行进行处理
while read line; do
  # 提取角色名和文件夹名
  role_name=$(echo $line | awk -F, '{print $1}')
  # echo $role_name
  folder_name=$(echo $line | awk -F, '{print $2}')

  #new_folder_name=$(echo $line | awk -F, '{print $2$1}')
  arr=(${line//,/ })
  new_folder_name="${arr[1]}${arr[0]}"
  echo $new_folder_name
  # echo $folder_name
  # 构造新的文件夹名
  # new_folder_name="${folder_name}${role_name}"
  # echo $new_floder_name
  # 执行重命名操作
  mv "$1/${folder_name}" "$1/${new_folder_name}"
  # echo "mv "${folder_name}" "${name}""
done < "${2}"
