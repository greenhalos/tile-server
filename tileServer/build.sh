#!/usr/bin/env bash

docker build -t greenhalos/tile-server .
docker push greenhalos/tile-server
