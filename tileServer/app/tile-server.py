#!/usr/bin/env python

import os
import shutil
import math
import psycopg2
import time
import yaml
import datetime
from flask import request

from flask import Flask, redirect, make_response
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR,'cache')

queryTemplate = """
    SELECT ST_AsMVT(tile, '{}', 4096, 'geom')
    FROM (
      SELECT import.osm_{}.*, ST_AsMVTGeom(
        geometry,
        ST_transform(ST_SetSRID(ST_Makebox2d(ST_Point({},{}),ST_Point({},{})), 4326),3857)
      ) AS geom
      FROM import.osm_{}
      WHERE geometry && ST_transform(ST_SetSRID(ST_Makebox2d(ST_Point({},{}),ST_Point({},{})), 4326),3857)
    )
    AS tile;
"""

defaultTablesByZoom = {}

def tile_ul(x, y, z):
    n = 2.0 ** z
    lon_deg = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat_deg = math.degrees(lat_rad)
    return  lon_deg,lat_deg

def getTablesForZoom(z):
    return defaultTablesByZoom.get(z, [])

def get_tile(z,x,y, tableName, useCache):

    xmin,ymin = tile_ul(x, y, z)
    xmax,ymax = tile_ul(x + 1, y + 1, z)

    tables = getTablesForZoom(z) if tableName is None else tableName

    tile = None

    tilefolder = "{}/{}/{}/{}".format(CACHE_DIR,tableName,z,x)
    tilepath = "{}/{}.pbf".format(tilefolder,y)

    cacheVersionAvailable = os.path.exists(tilepath)

    if cacheVersionAvailable and not useCache:
        os.remove(tilepath)
        cacheVersionAvailable = False


    if not cacheVersionAvailable :
        startGenerate = time.time()
        conn = psycopg2.connect('dbname=tiles user=tiles password=Uf8yQECNtJgPAicUwrZHsBoyB8SgDcEaiGfexsziUCsJzR3KyW73FpsAPQMYyfe host=tileserver-postgis')
        cur = conn.cursor()

        if not os.path.exists(tilefolder):
            os.makedirs(tilefolder)

        with open(tilepath, 'wb') as f:
            for table_name in tables:
                query = queryTemplate.format(table_name,table_name,xmin,ymin,xmax,ymax,table_name,xmin,ymin,xmax,ymax)
                cur.execute(query)
                result = cur.fetchone()
                if len(result) > 0:
                    f.write(result[0])
            f.close()

        cur.close()
        conn.close()
        endGenerate = time.time()

        duration = round(endGenerate - startGenerate, 2)
        fileSize = os.path.getsize(tilepath) / 1000
        print("Generated tile at z={} x={} y={} for table {} in {}s and produced {}KB".format(z,x,y,tableName,duration,fileSize))

    tile = open(tilepath, 'rb').read()
    return tile

@app.route('/')
def index():
    return redirect("/static/index.html", code=302)


@app.route('/tiles')
@app.route('/tiles/<int:z>/<int:x>/<int:y>.pbf', methods=['GET'])
@app.route('/tiles/<string:tableName>/<int:z>/<int:x>/<int:y>.pbf', methods=['GET'])
def tiles(tableName=None,z=0, x=0, y=0):
    useCache = request.args.get('cache', default = True, type = bool)
    tile = get_tile(z, x, y, tableName, useCache)
    if (len(tile) > 0):
        response = make_response(tile)
    else:
        response = make_response(b'\\x')
    response.headers['Content-Type'] = "application/vnd.mapbox-vector-tile"
    return response


def initZoomDic():
    with open('zoomTables.yml', 'r') as stream:
        data = yaml.load(stream)
        for zoom in range(0, 24):
            result = []
            for tableName in data:
                e = data[tableName]
                if e['enabled'] and zoom >= e['min'] and zoom <= e['max']:
                    result.append(tableName)
            defaultTablesByZoom[zoom] = result

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)

# def pregenerate(lat0, lon0, lat1, lon1):
#
#     startTime = datetime.datetime.now()
#     total = 0
#     for zoom in range (0, 15):
#         x0,y0 = deg2num(lat0, lon0, zoom)
#         x1,y1 = deg2num(lat1, lon1, zoom)
#         x1 += 1
#         y1 += 1
#         total += (x1 - x0) * (y1 - y0)
#         print("finsihed calcualtion tiles for zoom level {}".format(zoom))
#     count = 1
#     for zoom in range (0, 15):
#         x0,y0 = deg2num(lat0, lon0, zoom)
#         x1,y1 = deg2num(lat1, lon1, zoom)
#         for x in range(x0, x1):
#             for y in range(y0, y1):
#
#                 currentTime = datetime.datetime.now()
#                 diffSeconds = currentTime - startTime
#                 eta = (count / diffSeconds.total_seconds() ) * (total - count)
#                 etaNow = eta + (currentTime - datetime.datetime(1970,1,1)).total_seconds()
#                 etaString = str(datetime.timedelta(seconds=etaNow))
#
#                 percent = (count / total) * 100
#                 print("{} {} {} {}%: ".format(diffSeconds, eta, etaString, percent), end='')
#                 get_tile(zoom, x, y, None)
#                 count += 1

if __name__ == "__main__":
    initZoomDic()
    #pregenerate(49.617828, 8.209534, 48.212778, 8.580322)
    app.run(host="0.0.0.0", debug=True)
