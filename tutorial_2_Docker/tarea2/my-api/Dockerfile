FROM python:3.8.10-alpine3.12

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirements.txt 

ENTRYPOINT python main.py