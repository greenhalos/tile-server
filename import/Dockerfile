FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y wget

RUN mkdir /code

RUN wget -nv -O /code/imposm.tar.gz https://github.com/omniscale/imposm3/releases/download/v0.6.0-alpha.4/imposm-0.6.0-alpha.4-linux-x86-64.tar.gz

WORKDIR /code

RUN tar -xzf imposm.tar.gz
RUN mv imposm-0.6.0-alpha.4-linux-x86-64 imposm

RUN wget -nv -O data.osm.pbf http://download.geofabrik.de/europe/germany/baden-wuerttemberg/karlsruhe-regbez-latest.osm.pbf

ADD mapping.yml /code
ADD config.json /code

CMD ["imposm/imposm", "import", "-config", "./config.json", "-read", "./data.osm.pbf", "-write", "-overwritecache"]
