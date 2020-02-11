FROM ubuntu:18.04


RUN apt-get update && true
RUN apt-get -y install build-essential git-core checkinstall gcc-multilib 
RUN git clone https://github.com/raspberrypi/tools.git /opt/tools

RUN touch /tmp/test



RUN git clone git://source.ffmpeg.org/ffmpeg.git
WORKDIR /ffmpeg
RUN git checkout 2ca65fc7b74444edd51d5803a2c1e05a801a6023

RUN git clone https://code.videolan.org/videolan/x264.git


WORKDIR /ffmpeg/x264

RUN git checkout 7d0ff22e8c96de126be9d3de4952edd6d1b75a8c 
RUN ./configure --host=arm-linux --cross-prefix="/opt/tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian-x64/bin/arm-linux-gnueabihf-" --enable-static --enable-shared --disable-asm --disable-opencl --prefix=/ffmpeg
RUN make -j
RUN make install
RUN make distclean


WORKDIR /ffmpeg
RUN git clone https://chromium.googlesource.com/webm/libvpx
WORKDIR /ffmpeg/libvpx
#RUN git checkout v1.4.0
ENV CROSS=/opt/tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian-x64/bin/arm-linux-gnueabihf-
RUN ./configure  --target=armv7-linux-gcc --enable-static --disable-unit-tests 
RUN make -j
RUN make install
RUN checkinstall --pkgname=libvpx --pkgversion="$(date +%Y%m%d%H%M)-git" --backup=no --default --deldoc=yes


RUN rm /etc/ld.so.cache && ldconfig

WORKDIR /ffmpeg


RUN ./configure --enable-cross-compile --cross-prefix="/opt/tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian-x64/bin/arm-linux-gnueabihf-" --arch=armel --target-os=linux --enable-gpl  --enable-libvpx  --extra-cflags="-I/ffmpeg/libvpx/" --extra-ldflags="-ldl -L/ffmpeg/libvpx/"  --extra-cflags="-I/ffmpeg/libx264/" --extra-ldflags="-ldl -L/ffmpeg/libx264/"  
RUN make -j




#X86 version of the ffmpeg (useful for development and intel nuc versions of the stack)

RUN apt-get -y install yasm nasm

RUN cp -Rv /ffmpeg /ffmpeg_x86_linux
ENV CROSS=''
WORKDIR /ffmpeg_x86_linux
RUN make clean 
WORKDIR /ffmpeg_x86_linux/x264/
RUN make clean
RUN ./configure --enable-static --disable-asm 
RUN make -j

WORKDIR /ffmpeg_x86_linux/libvpx
RUN make clean
RUN ./configure --enable-static
RUN make -j


#
WORKDIR /ffmpeg_x86_linux
RUN ./configure --target-os=linux --enable-gpl    --extra-cflags="-I/ffmpeg_x86_linux/libvpx/" --extra-ldflags="-ldl -L/ffmpeg_x86_linux/libvpx/"  --extra-cflags="-I/ffmpeg_x86_linux/libx264/" --extra-ldflags="-ldl -L/ffmpeg_x86_linux/libx264/" --enable-libvpx

RUN make -j 
