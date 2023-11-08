FROM ubuntu

RUN apt update 
RUN apt install -y python2.7 python2.7-dev git python-pip
RUN apt install -y net-tools netcat iputils-ping

WORKDIR /HoneyPy
COPY ./HoneyPy/requirements.txt /HoneyPy

RUN python2.7 -m pip install -r requirements.txt

