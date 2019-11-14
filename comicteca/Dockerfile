# pull official base image
# FROM python:3.8.0-alpine
FROM python:2.7.13-alpine
#FROM python:2.7.13-slim

# RUN mkdir -p /usr/src/app

# Static and Media directories
RUN mkdir -p /usr/src/app/staticfiles && mkdir -p /usr/src/app/media && ls -hal /usr/src/app

# set work directory
WORKDIR /usr/src/app

# Set environment variables
# PYTHONDONTWRITEBYTECODE: 
# If this is set, Python won’t try to write .pyc or .pyo files on the import of source modules. This is equivalent to specifying the -B option.
ENV PYTHONDONTWRITEBYTECODE 1
# PYTHONUNBUFFERED: 
# Force stdin, stdout and stderr to be totally unbuffered. On systems where it matters, also put stdin, stdout and stderr in binary mode.
ENV PYTHONUNBUFFERED 1

# Install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev python-dev jpeg-dev zlib-dev postgresql-client

# Install requirements
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
