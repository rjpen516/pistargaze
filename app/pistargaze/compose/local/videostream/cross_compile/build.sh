#!/bin/bash 


docker build ./ -t ffmpeg_build


docker create -ti --name copy_file ffmpeg_build bash

docker cp copy_file:/ffmpeg_x86_linux/ffmpeg ../x86_64_linux/ffmpeg
docker cp copy_file:/ffmpeg_x86_linux/ffmpeg_g ../x86_64_linux/ffmpeg_g
docker cp copy_file:/ffmpeg_x86_linux/ffprobe ../x86_64_linux/ffprobe
docker cp copy_file:/ffmpeg_x86_linux/ffprobe_g ../x86_64_linux/ffprobe_g
docker cp copy_file:/ffmpeg_x86_linux/ffserver ../x86_64_linux/ffserver
docker cp copy_file:/ffmpeg_x86_linux/ffserver_g ../x86_64_linux/ffserver_g


docker cp copy_file:/ffmpeg/ffmpeg ../armv7/ffmpeg
docker cp copy_file:/ffmpeg/ffmpeg_g ../armv7/ffmpeg_g
docker cp copy_file:/ffmpeg/ffprobe ../armv7/ffprobe
docker cp copy_file:/ffmpeg/ffprobe_g ../armv7/ffprobe_g
docker cp copy_file:/ffmpeg/ffserver ../armv7/ffserver
docker cp copy_file:/ffmpeg/ffserver_g ../armv7/ffserver_g


docker rm -f copy_file