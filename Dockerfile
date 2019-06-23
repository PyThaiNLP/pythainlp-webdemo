FROM python:3.6.8-alpine3.9

WORKDIR /usr/src/app

# Install build dependencies such as gcc
RUN apk update && apk add build-base

COPY requirements.txt .
RUN pip install --upgrade pip && pip install  -r requirements.txt

COPY . .

CMD python main.py
EXPOSE 80