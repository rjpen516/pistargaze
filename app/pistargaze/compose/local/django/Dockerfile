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
  && apk add wget cython \
  && pip install cython

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

RUN     buildDeps="autoconf \
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
                   expat-dev" && \

        apk  add --no-cache --update ${buildDeps}




RUN git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg && cd ffmpeg/ && git checkout 2ca65fc7b74444edd51d5803a2c1e05a801a6023 && ./configure --prefix=/opt/ --enable-libvpx && make -j && make install




WORKDIR /tmp/
RUN git clone https://github.com/seeing-things/point.git
WORKDIR /tmp/point
RUN python3 setup.py install

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
