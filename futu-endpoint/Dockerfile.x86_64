FROM --platform=linux/x86_64 ubuntu:16.04

WORKDIR /FutuOpenD

ADD ./src/* /FutuOpenD/

COPY docker-entrypoint.sh /

RUN apt-get update
RUN apt-get install -y telnet curl

EXPOSE 11111 22222 33333
ENTRYPOINT ["sh", "/docker-entrypoint.sh"]