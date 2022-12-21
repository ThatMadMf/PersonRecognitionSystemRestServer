FROM python:3.7.0

RUN mkdir /django-server
WORKDIR /django-server

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD requirements.txt /django-server
RUN pip install -r requirements.txt
ADD ./server /django-server/server
ADD PersonRecognitionSystemRestServer /django-server/PersonRecognitionSystemRestServer
ADD manage.py /django-server
