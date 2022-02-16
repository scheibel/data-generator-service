FROM alpine:3.11

# Basics
RUN apk update
RUN apk upgrade
RUN apk add g++ gcc libffi-dev make python3 python3-dev py3-pip
RUN pip3 install pipenv

# Python3
WORKDIR /opt/data-generator-service

ADD Pipfile Pipfile

RUN pipenv install

ADD service.py service.py
ADD v0 v0
ADD data data

CMD ["pipenv", "run", "uvicorn", "--host", "0.0.0.0", "--port", "9000", "service:app"]
