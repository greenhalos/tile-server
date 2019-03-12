#!/usr/bin/env bash

docker build -t greenhalos/tile-server-import ./import/
docker push greenhalos/tile-server-import
