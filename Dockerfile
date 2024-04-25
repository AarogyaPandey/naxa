FROM naxa/python:3.9-slim
# Uses naxa/python:3.9-slim instead of python:3.9-slim so that
# apt/requirement doesn't have to reinstall everytime

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code
RUN mkdir -p /sock
RUN mkdir -p /logs
WORKDIR /code

# COPY apt_requirements.txt /code/
RUN apt-get -y update
# RUN cat apt_requirements.txt | xargs apt -y --no-install-recommends install && \
# 	rm -rf /var/lib/apt/lists/* && \
# 	apt autoremove && \
# 	apt autoclean
RUN apt-get -y --no-install-recommends install \
curl \
libpangocairo-1.0-0 \
libpq-dev \
python-dev \
libproj-dev \
libc-dev \
binutils \
gettext \
make \
cmake \
gcc \
gdal-bin \
libgdal-dev \
g++

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

COPY requirements.txt /code/

#required for gdal installation
RUN pip install --no-cache-dir setuptools==57.5.0
RUN pip install --no-cache-dir -r requirements.txt
RUN rm /code/requirements.txt

COPY . /code