FROM ubuntu:16.04

MAINTAINER Remy Galan "remyalexander@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev python3-tk python3-rtree

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "geoapi.py" ]
