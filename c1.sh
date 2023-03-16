#!/bin/bash

OIFS="$IFS"
IFS=$'\n'

while getopts ":n:a:h" optname
do
    case "$optname" in
      "n")
        echo "get option -n,value is $OPTARG"
        ;;
      "a")
        echo "get option -a ,value is $OPTARG"
        ;;
      "h")
        echo "get option -h,eg:./test.sh -n 编程珠玑 -a 守望先生"
        ;;
      ":")
        echo "No argument value for option $OPTARG"
        ;;
      "?")
        echo "Unknown option $OPTARG"
        ;;
      *)
        echo "Unknown error while processing options"
        ;;
    esac
    # echo "option index is $OPTIND"
done

IFS="$OIFS"
