FROM python:3.10.4-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt .
#if -r flag not included, pip will fail to install the "package", -r installs contents
RUN pip install -r requirements.txt

COPY . .