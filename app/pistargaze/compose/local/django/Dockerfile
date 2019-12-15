FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  # Translations dependencies
  && apk add gettext \
  # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
  && apk add postgresql-client \
  && apk add gpsd gpsd-clients  \
  && apk add wget

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower


WORKDIR /tmp/gpsd-py3
COPY ./libs/gpsd-py3/ /tmp/gpsd-py3/
RUN python3 setup.py install 


RUN apk add git unzip  build-base gcc cmake


# We are going to install our astro python libs


WORKDIR /opt
RUN wget https://github.com/opencv/opencv/archive/2.4.13.6.zip
RUN unzip 2.4.13.6.zip && \
  cd /opt/opencv-2.4.13.6/ && \
  mkdir build

WORKDIR /opt/opencv-2.4.13.6/build

RUN cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_FFMPEG=NO \
  -D WITH_IPP=NO -D WITH_OPENEXR=NO ..

  RUN make VERBOSE=1
RUN make
RUN make install

WORKDIR /tmp/

RUN apk add gfortran perl

RUN wget https://github.com/xianyi/OpenBLAS/archive/v0.3.6.tar.gz \
  && tar -xf v0.3.6.tar.gz \
  && cd OpenBLAS-0.3.6/ \
  && make BINARY=64 FC=$(which gfortran) USE_THREAD=1 \
  && make PREFIX=/usr/lib/openblas install



RUN ATLAS=/usr/lib/openblas/lib/libopenblas.so LAPACK=/usr/lib/openblas/lib/libopenblas.so pip install scipy==1.3
RUN export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/lib/openblas/lib/

RUN  pip3 install --no-cache-dir numpy scipy 

WORKDIR /opt

RUN wget http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-3.47.tar.gz
RUN tar -xvf cfitsio-3.47.tar.gz

WORKDIR /opt/cfitsio-3.47

RUN ./configure && make && make install

RUN cp -R /opt/cfitsio-3.47/lib/* /usr/lib/
RUN cp /opt/cfitsio-3.47/include/* /usr/include/

WORKDIR /opt

RUN apk add libc-dev bsd-compat-headers swig cairo-dev bash

RUN git clone https://github.com/dstndstn/astrometry.net.git
WORKDIR /opt/astrometry.net
RUN git checkout -b 0.78
RUN make && make py && make extra && make install


WORKDIR /usr/share/astrometry

RUN wget http://data.astrometry.net/4100/index-4112.fits
RUN wget http://data.astrometry.net/4100/index-4113.fits
RUN wget http://data.astrometry.net/4100/index-4114.fits
RUN wget http://data.astrometry.net/4100/index-4115.fits
RUN wget http://data.astrometry.net/4100/index-4116.fits
RUN wget http://data.astrometry.net/4100/index-4117.fits
RUN wget http://data.astrometry.net/4100/index-4118.fits
RUN wget http://data.astrometry.net/4100/index-4119.fits

WORKDIR /opt/
RUN git clone https://github.com/UBNanosatLab/openstartracker.git




WORKDIR /tmp/
RUN git clone https://github.com/seeing-things/point.git
WORKDIR /tmp/point
RUN python3 setup.py install

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
