#!/bin/bash
path=$1

if [ -a "$path" ]
then
    echo "$path exist"
    ls $path
else
    echo "$path is error"
    exit 0
fi

files=$(ls "$path")
echo $files

for file in $files
do 
	echo "**********"
	childpath="$path/$file"
	echo "childpath is $childpath"

	if [ -d "$childpath" ]	
	then
		imgfiles=$(find "$childpath" -type f -name "*.jpg")
		for file in $imgfiles
		do
			echo ${#file}
			imgfile="${childpath}/${file}"
			echo "file name is ${imgfile}"
			
			#mogrify -format jpg -resize 25% "$imgfile"
		done
	fi
	echo "##################"
done
