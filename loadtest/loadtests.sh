#!/usr/bin/env bash

HOST=$1
Z=$2
X=$3
Y=$4
LAYER_NAME=$5

if [ -z $LAYER_NAME ]; then
  URL="https://$HOST/tiles/$Z/$X/$Y.pbf?cache=False"
else
  URL="https://$HOST/tiles/$LAYER_NAME/$Z/$X/$Y.pbf?cache=False"
fi;


CURL_RESULT=$(curl -w "@curl-format.txt" -o /dev/null -s $URL)
echo "$Z;$X;$Y;$CURL_RESULT;$LAYER_NAME;$URL"
