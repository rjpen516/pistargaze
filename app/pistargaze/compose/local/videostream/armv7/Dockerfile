FROM ubuntu:18.04

RUN apt-get update
RUN apt-get -y install bash  gphoto2 inotify-tools

COPY ./compose/local/videostream/armv7/ffmpeg /opt/ffmpeg
COPY ./compose/local/videostream/armv7/ffmpeg_g /opt/ffmpeg_g
COPY ./compose/local/videostream/armv7/ffprobe /opt/ffprobe
COPY ./compose/local/videostream/armv7/ffprobe_g /opt/ffprobe_g
COPY ./compose/local/videostream/armv7/ffserver /opt/ffserver
COPY ./compose/local/videostream/armv7/ffserver_g /opt/ffserver_g

COPY ./compose/local/videostream/start /start

COPY ./compose/local/videostream/ffmpeg.conf /etc/

RUN chmod +x /start



COPY ./compose/local/videostream/state.sh /state.sh
RUN chmod +x /state.sh

ENTRYPOINT ["/start"]

