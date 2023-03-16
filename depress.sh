#!/bin/bash
#解压文件并且删除原文件，缩小尺寸

OIFS="$IFS"
IFS=$'\n'

files=$(find "${1}" -type f -name "*.7z")

for file in $files
do
	echo "${file/z1p/zip}"
    mv "${file}" "${file/z1p/zip}"
	#mogrify -format jpg -resize 25% ${img}
done

IFS="$OIFS"