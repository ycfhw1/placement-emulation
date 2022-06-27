FROM ubuntu:xenial
MAINTAINER manuel.peuster@uni-paderborn.de
RUN sed -i s/archive.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list \
&& sed -i s/security.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list \
&& apt-get update && apt-get upgrade
RUN export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install -y -q \
	net-tools \
	iproute \
	inetutils-ping \
	iptables \
	squid3 \
	curl

ADD squid.conf /etc/squid/squid.conf

ADD start.sh start.sh
RUN chmod +x start.sh
ADD ipconfig.sh ipconfig.sh
RUN chmod +x ipconfig.sh

WORKDIR /

EXPOSE 3128

# entry point
ENV SON_EMU_CMD ./start.sh
CMD /bin/bash
