FROM python:3.10
MAINTAINER Thomas Lazarus (Github: lazarust)

ENV PYTHONUNUNBUFFERED 1

RUN mkdir /bot
WORKDIR /bot
# TODO: Some of these probably aren't necessary. Remove them.
RUN apt-get update && \
    apt-get install -y curl \
    git \
    python3-dev \
    python3-pip \
    wget

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .