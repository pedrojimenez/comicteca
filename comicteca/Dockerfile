# pull official base image
# FROM python:3.8.0-alpine
FROM python:2.7.13-alpine
#FROM python:2.7.13-slim

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/comicteca
RUN mkdir -p $APP_HOME/staticfiles && mkdir -p $APP_HOME/media
WORKDIR $APP_HOME




# Static and Media directories
###RUN mkdir -p /usr/src/app/staticfiles && mkdir -p /usr/src/app/media && ls -hal /usr/src/app

# set work directory
### WORKDIR /usr/src/app

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
#COPY ./requirements.txt /usr/src/app/requirements.txt
COPY ./requirements.txt $APP_HOME
RUN pip install -r requirements.txt

# copy entrypoint.sh
#COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
#COPY . /usr/src/app/
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.sh
###ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
ENTRYPOINT ["/home/app/comicteca/entrypoint.sh"]
