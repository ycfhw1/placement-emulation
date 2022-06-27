FROM ubuntu:xenial
MAINTAINER manuel.peuster@uni-paderborn.de
RUN sed -i s/archive.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list \
&& sed -i s/security.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list \
&& apt-get update && apt-get upgrade
# define interface names (should be the same as in VNFD)
ENV IFOUT output

RUN export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install -y -q \
	net-tools \
	iproute \
	traceroute \
	inetutils-ping \
	curl \
        wget \
        hping3 \
        httping

ADD start.sh start.sh
RUN chmod +x start.sh

WORKDIR /

# entry point
ENV SON_EMU_CMD ./start.sh
CMD /bin/bash

