FROM python:3.9.6-alpine
MAINTAINER Jacob Leiner

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECIDE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
COPY requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev python3-dev musl-dev

# install dependencies
RUN pip install pip --upgrade
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
