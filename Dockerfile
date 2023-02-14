FROM python:3.8-alpine



ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY . /app
WORKDIR /app

RUN apk add --update --no-cahce --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev && \
    pip3 install -r requirements.txt
