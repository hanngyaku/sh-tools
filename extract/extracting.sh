#!/bin/bash

# 遍历指定目录下的所有子目录中的7z文件
dir="$1"
cd "$dir"
total=$(find . -type f -name "*.7z" | wc -l)
current=1
log_file="extract.log"  # 指定日志文件路径

# 创建日志文件
touch "$log_file"

echo "Extracting files in $dir" > "$log_file"
find . -type f -name "*.7z" | while read file
do
    echo -ne "Extracting file $current of $total: $file \r"
	echo -ne "Extracting file $current of $total: $file" >> "$log_file"
    # 使用-o选项指定解压后的目录
    7z x "$file" -pwww.52cos.top -y -o"${file%/*}" > /dev/null
    if [ $? -eq 0 ]; then  # 检查解压返回值
        rm -f "$file"  # 删除源文件
        current=$((current+1))
        echo "Extracted $file" >> "$log_file"  # 记录解压成功的文件名到日志文件
    else
        echo "Error extracting $file" >> "$log_file"  # 记录解压失败的文件名到日志文件
    fi
done
echo "Extraction complete." >> "$log_file"
echo "Extraction complete."

