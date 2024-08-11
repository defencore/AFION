FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    build-essential \
    libncurses5-dev \
    zlib1g-dev \
    gawk \
    git \
    ccache \
    gettext \
    libssl-dev \
    xsltproc \
    rsync \
    unzip \
    python3 \
    python3-distutils \
    file
 
CMD ["bash"]
