# base image
FROM public.ecr.aws/docker/library/python:3.10
# setup environment variable
ENV DockerHOME=/home/app

# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update && apt-get -y install redis-server
RUN pip install --upgrade pip
RUN pip install redis

# copy whole project to your docker home directory.
COPY . $DockerHOME

RUN chmod 755 entryPoint.sh
RUN chmod 755 .

# run this command to install all dependencies
RUN pip install -r requirements.txt

## port where the Django app runs
EXPOSE 8000

CMD ["/bin/bash", "-c", "./entryPoint.sh"]