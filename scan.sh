#!/bin/bash

# 接受要扫描的目录路径作为参数
dir="$1"

# 如果未提供目录参数，显示使用说明并退出
if [ -z "$dir" ]; then
    echo "使用方法： $0 /path/to/images"
    exit 1
fi

# 扫描目录中的所有图片
count=0
total=$(find "$dir" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | wc -l)

echo "处理进度：$total"

