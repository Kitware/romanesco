FROM ubuntu:14.04
MAINTAINER Jeffrey Baumes <jeff.baumes@kitware.com>

RUN apt-get update && apt-get install -y software-properties-common python-software-properties
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libpython-dev \
    python-pip
RUN pip install -U girder
RUN girder-install -f web
RUN girder-install -f plugin

COPY . /romanesco
WORKDIR /romanesco
RUN girder-install -f plugin -s .

ENTRYPOINT ["python", "-m", "girder"]
