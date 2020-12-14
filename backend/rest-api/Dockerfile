FROM python:3.9

# set work directory
WORKDIR /code/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#setup mysql driver
RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev  -y
RUN apt-get -y install sudo

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements/requirements.txt /code/app/requirements.txt
RUN pip install -r /code/app/requirements.txt

# copy project
COPY . /code/app/
COPY .env /code/app/.env