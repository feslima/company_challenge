FROM python:3.9.6-alpine

ARG DIR_NAME=/usr/src/backend

WORKDIR $DIR_NAME

RUN apk update && apk add postgresql-dev python3-dev gcc libc-dev

# These dependencies required by Pillow so that the tests can run
RUN apk add --update --no-cache --virtual .tmp linux-headers
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk del .tmp

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY ./requirements-dev.txt $DIR_NAME
RUN pip install -r requirements-dev.txt

# Copy source files
COPY . $DIR_NAME
