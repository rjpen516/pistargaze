FROM python:3.7-alpine

COPY ./compose/local/videostream/ffmpeg.conf /etc/ffmpeg.conf



RUN     buildDeps="autoconf \
                   git \
                   automake \
                   bash \
                   binutils \
                   bzip2 \
                   cmake \
                   curl \
                   coreutils \
                   diffutils \
                   file \
                   g++ \
                   gcc \
                   gperf \
                   libtool \
                   make \
                   python \
                   openssl-dev \
                   tar \
                   yasm \
                   nasm \
                   zlib-dev \
                   libvpx-dev \
                   libc-dev \
                   expat-dev" && \
    apk  add --no-cache --update ${buildDeps}




RUN git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg && cd ffmpeg/ && git checkout 2ca65fc7b74444edd51d5803a2c1e05a801a6023 && ./configure --prefix=/opt/ --enable-libvpx && make -j && make install

COPY ./compose/local/videostream/start /start
RUN chmod a+x /start


ENTRYPOINT ["/start"]