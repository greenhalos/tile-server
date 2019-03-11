#!/usr/bin/env bash

docker build -t greenhalos/tile-server-import .
docker push greenhalos/tile-server-import
