FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends gcc postgresql postgresql-contrib python3-dev
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . .
