FROM python:3.8-alpine

RUN apk --no-cache add build-base libffi-dev

WORKDIR /build
ADD requirements.txt /build
RUN pip install -U pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt --upgrade

ENTRYPOINT /app/bot_main.py