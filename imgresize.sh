#!/bin/bash

OIFS="$IFS"
IFS=$'\n'

#size in [16,+] file resize 25%
imgs=$(find "$1" -type f -size +16M -name "*.jpg")
imgtask=$(find "$1" -type f -size +16M -name "*.jpg" | wc -l)
index=0
for img in $imgs
do
	printf "%d/%d\r" "${index}" "${imgtask}"
	index=$(($index+1))
	#echo "${img}"
	mogrify -format jpg -resize 25% ${img}
done
echo

#size in [5, 16] file resize 50%
imgs=$(find "$1" -type f -size +5M -size -16M -name "*.jpg")
index=0
imgtask=$(find "$1" -type f -size +5M -size -16M -name "*.jpg" | wc -l)
for img in $imgs
do
	printf "%d/%d\r" "${index}" "${imgtask}"
	index=$(($index+1))
	#echo "${img}"
	mogrify -format jpg -resize 50% ${img}
done
echo

IFS="$OIFS"
