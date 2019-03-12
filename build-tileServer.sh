#!/usr/bin/env bash

docker build -t greenhalos/tile-server ./tileServer
docker push greenhalos/tile-server
