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
RUN python3 -m venv venv
RUN #!/bin/bash source venv/bin/activate
RUN pip install --upgrade pip
COPY ./requirements/requirements.txt /code/app/requirements.txt
RUN pip install -r /code/app/requirements.txt

# copy project
COPY . /code/app/

EXPOSE 5000

RUN #!/bin/bash echo "app starting"

CMD [ "sudo", "gunicorn", "-b 0.0.0.0:5000", "application.start:app"]