FROM python/3.10-alpine3.16
MAINTAINER Thomas Lazarus (Github: lazarust)

ENV PYTHONUNUNBUFFERED 1

RUN mkdir /bot
WORKDIR /pot
# TODO: Some of these probably aren't necessary. Remove them.
RUN apt-get update && \
    apt-get install -y curl \
    git \
    python3-dev \
    python3-pip \
    wget

COPY requirements.txt ./
RUN pip install -r /requirements.txt

COPY . .