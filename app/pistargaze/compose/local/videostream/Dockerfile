FROM ubuntu:18.04

RUN apt-get update
RUN apt-get -y install bash  gphoto2

COPY ./compose/local/videostream/ffmpeg /opt/ffmpeg
COPY ./compose/local/videostream/ffmpeg_g /opt/ffmpeg_g
COPY ./compose/local/videostream/ffprobe /opt/ffprobe
COPY ./compose/local/videostream/ffprobe_g /opt/ffprobe_g
COPY ./compose/local/videostream/ffserver /opt/ffserver
COPY ./compose/local/videostream/ffserver_g /opt/ffserver_g

COPY ./compose/local/videostream/start /start

COPY ./compose/local/videostream/ffmpeg.conf /etc/

RUN chmod +x /start



COPY state.sh /state.sh
RUN chmod +x /start.sh

ENTRYPOINT ["/start"]

