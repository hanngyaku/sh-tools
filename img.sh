#!/bin/bash

OIFS="$IFS"
IFS=$'\n'

function resizeImg () {
    # echo "$1" # arguments are accessible through $1, $2,...
    imgs=$(find "$1" -type f -name "*.jpg")
    imgsCount=$(find "$1" -type f -name "*.jpg" | wc -l)

    echo $2
    echo $imgsCount

    for img in $imgs
    do
        echo $img
    done

    echo "***"
    find "$1" -type f -name "*.jpg" $2 
 }

function commandPar () {
    # echo "$1" # arguments are accessible through $1, $2,...
    com="find ${1} -type f -name "*.jpg" ${2}"
    echo $(eval ${com})
}

# resizeImg $1 "-size +1k -size -5M"
# commandPar $1 "-size +1k -size -5M"

# 支持参数 :size:resize
# 查找size的文件，设置为原来的resize%
while getopts ':s:r:s' OPT; do
    case $OPT in
        s) 
        S_DIR="$OPTARG"
        echo $S_DIR
        ;;
        r) 
        D_DIR="$OPTARG"
        echo $D_DIR
        ;;
    esac
done
#echo $S_DIR
#echo $D_DIR

IFS="$OIFS"