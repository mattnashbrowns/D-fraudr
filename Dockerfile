# syntax=docker/dockerfile:1

FROM ubuntu

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get -y install python3 python-is-python3
RUN apt-get -y install python3-pip
RUN apt-get -y install sudo

RUN useradd -ms /bin/bash dfraudr

WORKDIR /D-Fraudr
COPY .  .
RUN chown -R dfraudr /D-Fraudr

USER dfraudr
WORKDIR /D-Fraudr
RUN mkdir -p instance/uploads
RUN /D-Fraudr/install/dfraudr-build.sh

CMD  "/D-Fraudr/startup.sh"
