#!/bin/bash

OIFS="$IFS"
IFS=$'\n'

imgs=$(find "." -type f -name "*.JPG")

for img in $imgs
do
	echo "${img}"
	mogrify -format jpg -resize 25% ${img}
done

IFS="$OIFS"
