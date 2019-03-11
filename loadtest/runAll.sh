#!/usr/bin/env bash

HOST=$1

echo "z;x;y;time_total;size_download;layer;url"

declare -a LAYERS=($(cat ../tileServer/app/zoomTables.yml | grep -e ":$" | cut -d ':' -f1))

function executeLoadtest() {
  ./loadtests.sh $HOST $1 $2 $3
  for LAYER in "${LAYERS[@]}"
  do
     ./loadtests.sh $HOST $1 $2 $3 $LAYER
  done
}

executeLoadtest 15 17150 11250
executeLoadtest 13 4288 2812
executeLoadtest 13 4289 2812
executeLoadtest 10 534 351
executeLoadtest 9 267 176
executeLoadtest 3 4 2
