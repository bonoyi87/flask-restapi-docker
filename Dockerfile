FROM python:alpine

EXPOSE 5000
WORKDIR /app
ADD . /app


RUN python3 -m pip install pipenv

RUN apk add bash mariadb-dev mariadb-client build-base

COPY Pipfile /app


RUN pipenv install --ignore-pipfile
COPY autoapp.py /app

ADD run.sh /app
RUN chmod +x /app/*.sh
