FROM python:3.7.3-slim-stretch

ENV HOME=/opt/repo

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y wget gnupg2

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get update
RUN apt-get install -y python3 python3-pip postgresql-server-dev-10 gcc musl-dev

COPY ./docker-entrypoint.sh ${HOME}/docker-entrypoint.sh

COPY ./requirements.txt /tmp/
RUN pip3 install -U pip
RUN pip3 install -r /tmp/requirements.txt

COPY ./app ${HOME}/app

WORKDIR ${HOME}
ENTRYPOINT ["./docker-entrypoint.sh"]
