# syntax=docker/dockerfile:1

FROM ubuntu

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get -y install python3 python-is-python3
RUN apt-get -y install python3-pip
RUN apt-get -y install sudo

RUN useradd -ms /bin/bash dfraudr

USER dfraudr
WORKDIR /D-Fraudr
COPY . .

USER root
WORKDIR /D-Fraudr
RUN rm *sqlite

USER dfraudr
WORKDIR /D-Fraudr
RUN /D-Fraudr/build/dfraudr-build.sh

CMD  "/D-Fraudr/startup.sh"