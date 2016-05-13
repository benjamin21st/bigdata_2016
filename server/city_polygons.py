#!/usr/bin/env python
import shapefile
import json
import pprint

nycmap_path = '../data/ZillowNeighborhoods-NY'
boroughs = ['New York', 'Bronx', 'Queens', 'Kings', 'Richmond']


def load_nyc_polygons(path):
    sf = shapefile.Reader(path)
    records = sf.records()
    shapes = sf.shapes()

    # Filter out only those of New York City
    idx = 0
    data_list = []
    for index, record in enumerate(records):
        if record[1] in boroughs:
            join_data = {
                '_id_': idx,
                'name': record,
                'polygon': shapes[index].points,
                'bbox': shapes[index].bbox
            }
            data_list.append(join_data)
            idx += 1
    return data_list


def dump_polygon_js(path):
    sf = shapefile.Reader(path)
    records = sf.records()
    shapes = sf.shapes()

    idx = 0
    data_list = []
    for index, record in enumerate(records):
        if record[1] in boroughs:
            tmp = shapes[index].points
            tmp.append(shapes[index].points[0])

            join_data ={
                "type": "Feature",
                "properties": {
                "SP_ID": str(idx),
                "name": record[3],
                "borough": record[2],
                "state": record[0],
                "latitude": shapes[index].points[0][1],
                "longitude": shapes[index].points[0][0]
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        #shapes[index].points
                        tmp
                    ]
                    },
                "id": str(idx)
            }
            data_list.append(join_data)
            idx += 1

    retdata = {
            "type": "FeatureCollection",
            "features": data_list
            }
    return retdata


def loadjson():
# Load existing data
    with open('nyc.geojson') as f:
        data = json.load(f)

    for id, d in enumerate(data['features']):
        d['id'] = str(id)
        print id, d['properties']['NAME']
    '''
    # Add data
    feature = {}
    feature['type'] = 'Feature'
    feature['geometry'] = {'type': 'Point',
                       'coordinates': [10, 10],
                       }
    feature['properties'] =  {'prop0': 'value1'}
    data['features'].append(feature)
    '''
    # Write JSON file with new data
    with open('nyc.geojson2', 'w') as f:
        f.write(json.dumps(data))

def print_js():
    with open('nyc.geojson') as f:
        data = json.load(f)

    print "{"

    for id, d in enumerate(data['features']):
        d['id'] = str(id)
        print '%d:\"%s (%s)\",' % (id,d['properties']['NAME'], d['properties']['CITY'])

    print "}"
    '''
    # Add data
    feature = {}
    feature['type'] = 'Feature'
    feature['geometry'] = {'type': 'Point',
                       'coordinates': [10, 10],
                       }
    feature['properties'] =  {'prop0': 'value1'}
    data['features'].append(feature)
    '''


if __name__ == "__main__":
    print_js()
    #lists = load_nyc_polygons(nycmap_path)
    #lists = dump_polygon_js(nycmap_path)
    #pprint.pprint(lists)
    #json.dumps(lists, indent=4, sort_keys=True)
    #loadjson()
