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

#USER postgres
#WORKDIR /D-Fraudr
#RUN  /D-Fraudr/build/postgres-build.sh

#USER dfraudr
#WORKDIR /D-Fraudr
#RUN build/dfraudr-build.sh


USER root
CMD "/D-Fraudr/startup.sh"
#CMD [ "python3", "-m" , "flask", “--app”, “dfraudr”, "run", "--host=0.0.0.0"]