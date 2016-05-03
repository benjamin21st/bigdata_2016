#!/usr/bin/env python
import shapefile

sf = shapefile.Reader('../data/ZillowNeighborhoods-NY')


records = sf.records()
shapes = sf.shapes()

# Filter out only those of New York City
idx = 0
boxes = []
for index, record in enumerate(records):
    boroughs = ['New York', 'Bronx', 'Queens', 'Kings', 'Richmond']
    if record[1] in boroughs:
        join_data = {
            '_id_': idx,
            'name': record,
            'gps': shapes[index].points #shapes[index].points
        }
        boxes.append(shapes[index].bbox)
        print join_data
        idx += 1

#print boxes