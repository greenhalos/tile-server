#!/usr/bin/env python3

import json
import yaml

result = {}

with open('app/static/greenhalos-style.json') as json_file:
    data = json.load(json_file)
    for layer in data['layers']:
        if 'source-layer' in layer:
            minzoom = layer.get('minzoom', 0)
            maxzoom = layer.get('maxzoom', 24)
            sourceLayer = layer['source-layer']
            if not sourceLayer in result:
                result[sourceLayer] = {
                    'min': minzoom,
                    'max': maxzoom,
                    'enabled': True,
                }
            if minzoom < result[sourceLayer]['min']:
                result[sourceLayer]['min'] = minzoom
            if maxzoom > result[sourceLayer]['max']:
                result[sourceLayer]['max'] = maxzoom

print(yaml.dump(result, default_flow_style=False))
