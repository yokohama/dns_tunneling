#!/bin/bash

file_path=$1

IFS='/' read -r -a array <<< "$1"

length=${#array[@]}
base64_full_filename=${array[length-1]}

prefix=`echo $base64_full_filename | awk -F'_' '{print $1}'`
base64_filename=`echo $base64_full_filename | awk -F'_' '{print $2}'`
filename=`echo $base64_filename | base64 -d`

sanitize_filename=`echo $filename | sed 's|/|__|g'`

cat $file_path | base64 -d > outfile/${prefix}-${sanitize_filename}

exit
