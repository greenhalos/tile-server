#!/usr/bin/env bash

HOST=$1
Z=$2
X=$3
Y=$4

URL="https://$HOST/tiles/$Z/$X/$Y.pbf?cache=False"

CURL_RESULT=$(curl -w "@curl-format.txt" -o /dev/null -s $URL)
echo "$Z;$X;$Y;$CURL_RESULT;$URL"
