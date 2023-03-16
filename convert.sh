#!/bin/bash

OIFS="$IFS"
IFS=$'\n'

files=$(find "${1}" -type f -name "*.mobi")

for file in $files
do
	echo "${file/mobi/epub}"
    ebook-convert "${file}" "${file/mobi/epub}"
	#mogrify -format jpg -resize 25% ${img}
done

IFS="$OIFS"
