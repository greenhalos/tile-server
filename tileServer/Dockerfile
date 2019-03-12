FROM python:3.7-alpine

RUN adduser -D tiles

WORKDIR /home/tiles

RUN apk add postgresql-dev gcc musl-dev

COPY ./tileServer/requirements.txt /tmp/

RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

COPY ./tileServer/app /home/tiles

USER tiles

EXPOSE 5000
ENTRYPOINT ["python", "./tile-server.py"]
