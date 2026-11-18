#!/bin/sh
# usage: dl.sh <clip-name> <rawUrl>
cd "$(dirname "$0")/../../../../local/footage/clips" && curl -s -o "$1.mp4" "$2" && ffmpeg -v error -y -i "$1.mp4" -vf "fps=2,scale=300:-1,tile=5x2" -frames:v 1 "../clips-sheets/$1.jpg" && echo "$1 ok $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$1.mp4")"
