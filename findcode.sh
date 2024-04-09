#!/bin/bash

# 记录脚本开始时间
start_time=$(date +%s)

# 指定要查找的文件夹路径
search_dir="/Volumes/cgg_NAS-01908-03406/里番/年度合集/2024年合集/test"

# 使用 find 命令查找指定文件夹下的所有 MKV 文件
find "$search_dir" -type f -name "*.mkv" | while read -r file; do
    # 使用 ffprobe 获取视频文件的编码器信息
    video_codec=$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "$file")

    # 判断视频编码器是 H.264 或者 HEVC 的文件
    if [ "$video_codec" == "h264" ] || [ "$video_codec" == "hevc" ]; then
        echo "Converting file: $file"
        output_file="${file%.mkv}.mp4"

        # 记录转换开始时间
        conversion_start_time=$(date +%s)
        
        ffmpeg -nostdin -i "$file" -c:v copy -c:a copy "$output_file"
        if [ $? -eq 0 ]; then
            echo "Conversion successful: $output_file"
            echo "Deleting original file: $file"
            rm "$file"
        else
            echo "Conversion failed for: $file"
        fi

        # 计算转换运行时间
        conversion_end_time=$(date +%s)
        conversion_duration=$((conversion_end_time - conversion_start_time))
        echo "Conversion time: $conversion_duration seconds"
    fi
done

# 计算脚本总运行时间
end_time=$(date +%s)
total_duration=$((end_time - start_time))
echo "Total script execution time: $total_duration seconds"
