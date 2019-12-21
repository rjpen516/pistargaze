#!/bin/bash 


docker build ./ -t ffmpeg_build


docker create -ti --name copy_file ffmpeg_build bash

docker cp copy_file:/ffmpeg/ffmpeg ../ffmpeg
docker cp copy_file:/ffmpeg/ffmpeg_g ../ffmpeg_g
docker cp copy_file:/ffmpeg/ffprobe ../ffprobe
docker cp copy_file:/ffmpeg/ffprobe_g ../ffprobe_g
docker cp copy_file:/ffmpeg/ffserver ../ffserver
docker cp copy_file:/ffmpeg/ffserver_g ../ffserver_g


docker rm -f copy_file