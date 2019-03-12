#!/usr/bin/env python3

import urllib.request
import sys
import yaml
import math
import _thread

allLayers = yaml.load(open("../tileServer/app/zoomTables.yml")).keys()

def executeSingleRequest(host, z, x, y, layerName):
    if layerName is None:
        url = "https://{}/tiles/{}/{}/{}.pbf?cache=False".format(host, z, x, y)
    else:
        url = "https://{}/tiles/{}/{}/{}/{}.pbf?cache=False".format(host, layerName, z, x, y)
    r = urllib.request.urlopen(url)
    print("{};{};{};{};{};{}".format(z, x, y, r.info()['Content-Length'], layerName, url))

def executeRequest(host, z, x, y):
    executeSingleRequest(host, z, x, y, None)
    for layer in allLayers:
        executeSingleRequest(host, z, x, y, layer)

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)

print("z;x;y;size_download;layer;url")
host = sys.argv[1]

for zoom in range (0, 24):
    x,y = deg2num(49.006870, 8.403420, zoom)
    executeRequest(host, zoom, x ,y)
