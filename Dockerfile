FROM python:3.7
MAINTAINER kimjun136@naver.com
RUN apt-get -y update \
    && apt-get install -y rabbitmq-server \
    && service rabbitmq-server start

RUN pip install --upgrade pip

WORKDIR /var/app/current
COPY . .

RUN ["chmod", "+x", "/var/app/current/run.sh"]
RUN ["pip", "install", "pipenv"]

EXPOSE 8000
ENTRYPOINT ["/var/app/current/run.sh"]
