#!/bin/bash

OIFS="$IFS"
IFS=$'\n'

files=$(find "${1}" -type f -name "*.z1p")

for file in $files
do
	echo "${file/z1p/zip}"
    mv "${file}" "${file/z1p/zip}"
	#mogrify -format jpg -resize 25% ${img}
done

IFS="$OIFS"
