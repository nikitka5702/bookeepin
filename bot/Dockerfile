FROM python:3.7-alpine
ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apk add --no-cache gcc linx-headers postgresql-dev python3-dev musl-dev
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
