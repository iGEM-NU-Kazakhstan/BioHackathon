#Grab the latest alpine image
FROM alpine:latest

# Install python and pip
RUN apk add --no-cache --update python3 py3-pip bash g++

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


ADD . /opt/webapp/
WORKDIR /opt/webapp

ARG ARGPORT=$PORT
RUN g++ main.cpp
CMD ["python3", "app.py"]