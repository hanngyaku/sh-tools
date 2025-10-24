#!/bin/bash

# 让脚本出错时退出
set -e

# 使用说明
if [ "$#" -ne 3 ]; then
  echo "用法: $0 [backup|restore] <源路径> <备份路径>"
  exit 1
fi

mode=$1
src_dir=$2
backup_dir=$3

# 检查路径是否存在
if [ ! -d "$src_dir" ]; then
  echo "错误: 源路径不存在: $src_dir"
  exit 1
fi
mkdir -p "$backup_dir"

# 备份模式
if [ "$mode" = "backup" ]; then
  echo "开始备份 .nfo 文件..."
  find "$src_dir" -type f -name "*.nfo" | while read -r file; do
    relative_path="${file#$src_dir/}"
    target="$backup_dir/$relative_path"
    mkdir -p "$(dirname "$target")"
    cp -p "$file" "$target"
    echo "备份: $relative_path"
  done
  echo "✅ 备份完成。"

# 还原模式
elif [ "$mode" = "restore" ]; then
  echo "开始还原 .nfo 文件..."
  find "$backup_dir" -type f -name "*.nfo" | while read -r file; do
    relative_path="${file#$backup_dir/}"
    target="$src_dir/$relative_path"
    mkdir -p "$(dirname "$target")"
    cp -p "$file" "$target"
    echo "还原: $relative_path"
  done
  echo "✅ 还原完成。"

else
  echo "错误: 模式必须是 backup 或 restore"
  exit 1
fi
