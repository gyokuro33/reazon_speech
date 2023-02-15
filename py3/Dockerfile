FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu18.04
ARG DEBIAN_FRONTEND=noninteractive
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
# ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

# パッケージの追加とタイムゾーンの設定
# 必要に応じてインストールするパッケージを追加してください
RUN apt-get update && apt-get install -y \
    tzdata \
    &&  ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
    &&  apt-get clean \
    &&  rm -rf /var/lib/apt/lists/*

ENV TZ=Asia/Tokyo
RUN apt-get update && apt-get install -y cmake sox libsndfile1-dev ffmpeg flac nkf libfreetype6 libfreetype6-dev
RUN apt update && apt upgrade -y && apt install -y python3-pip curl git  python-pip wget
RUN pip3 install --no-cache-dir \
    torch==1.8.1 packaging
RUN git clone https://github.com/espnet/espnet
WORKDIR /espnet/tools
RUN ./setup_anaconda.sh anaconda espnet 3.8
RUN python3 -m  pip install -U pip && make TH_VERSION=1.8.1 CUDA_VERSION=11.1