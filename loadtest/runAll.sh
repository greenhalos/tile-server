#!/usr/bin/env bash

HOST=$1

echo "z;x;y;time_total;size_download;url"

./loadtests.sh $HOST 15 17150 11250
./loadtests.sh $HOST 13 4288 2812
./loadtests.sh $HOST 13 4289 2812
./loadtests.sh $HOST 10 534 351
./loadtests.sh $HOST 9 267 176
./loadtests.sh $HOST 3 4 2
