#!/bin/bash

# 接受要扫描的目录路径作为参数
dir="$1"

# 如果未提供目录参数，显示使用说明并退出
if [ -z "$dir" ]; then
    echo "使用方法： $0 /path/to/images"
    exit 1
fi

# 创建一个进度文件
progress_file="/tmp/scan_images_progress.txt"
echo "0" > "$progress_file"

# 扫描目录中的所有图片
count=0
total=$(find "$dir" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | wc -l)
while read img; do
    # 如果图片大于4M，调整大小
    if [ $(stat -c '%s' "$img") -gt 4000000 ]; then
        convert "$img" -define jpeg:extent=4MB "$img"
    fi

    # 更新进度文件
    count=$((count+1))
    percent=$((count*100/total))
    echo "处理进度：$percent% ($count/$total)" > "$progress_file"
done < <(find "$dir" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \))

# 删除进度文件
rm "$progress_file"

echo "扫描完成！"

