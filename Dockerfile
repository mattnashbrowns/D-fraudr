# syntax=docker/dockerfile:1

FROM ubuntu/postgres

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get -y install python3 python-is-python3
RUN apt-get -y install libpq-dev
RUN apt-get -y install python3-pip
RUN apt-get -y install sudo

RUN useradd -ms /bin/bash dfraudr

USER dfraudr
WORKDIR /D-Fraudr
COPY . .

USER root
WORKDIR /D-Fraudr
RUN build/root-build.sh
RUN chown -R postgres:postgres /var/run/postgresql

CMD  "/D-Fraudr/startup.sh"