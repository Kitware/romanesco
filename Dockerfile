FROM ubuntu:14.04
MAINTAINER Jeffrey Baumes <jeff.baumes@kitware.com>

RUN apt-get update && apt-get install -y software-properties-common python-software-properties
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libpython-dev \
    python-pip

RUN echo 'deb http://cran.rstudio.com/bin/linux/ubuntu trusty/' | tee /etc/apt/sources.list.d/cran.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9
RUN apt-get update && apt-get install -y \
    r-base-dev

COPY . /romanesco
WORKDIR /romanesco
RUN pip install -r /romanesco/requirements.txt

ENV C_FORCE_ROOT=1

ENTRYPOINT ["python", "-m", "romanesco"]
