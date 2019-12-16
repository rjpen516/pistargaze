FROM dm90/astrometry@sha256:9623aa52a531a36cd35b84f767506d920b7e01bb4bab19125f4aac89d4fff903


#RUN yum update
RUN yum --assumeyes install patch
#COPY ./compose/local/nova/api.py.patch /tmp/

WORKDIR /astrometry.net/net

#RUN patch -R api.py < /tmp/api.py.patch

RUN rm /astrometry.net/net/api.py*
COPY ./compose/local/nova/api.py /astrometry.net/net/api.py


RUN rm /astrometry.net/net/models.py*
COPY ./compose/local/nova/models.py /astrometry.net/net/models.py

RUN rm /astrometry.net/net/process_submissions.py*
COPY ./compose/local/nova/process_submissions.py /astrometry.net/net/process_submissions.py

WORKDIR /
ENTRYPOINT ["./docker-entrypoint.sh"]
# start nova by default
CMD ["nova"]
