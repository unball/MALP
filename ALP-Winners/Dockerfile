FROM ubuntu:18.04

# Dependencias
RUN apt-get update
RUN apt-get install -y \
    git \
    sudo \
    nano \
    python3.8 \
    python3-pip \
    protobuf-compiler \
    libprotobuf-dev
RUN apt-get clean
RUN adduser --disabled-password --gecos '' unball

USER unball

WORKDIR /home/unball
RUN git clone https://OrdinaryUnballMember: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@github.com/unball/ALP-Winners

WORKDIR /home/unball/ALP-Winners
RUN git checkout dev_luiz

WORKDIR /home/unball/ALP-Winners/src/client/protobuf/
RUN sh protobuf.sh

WORKDIR /home/unball/ALP-Winners
RUN pip3 install -r requirements.txt



