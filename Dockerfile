FROM python:3.10.16-alpine3.21
LABEL maintainer="gnonasis@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN adduser -D my-user

USER my-user
