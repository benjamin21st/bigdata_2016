#!/usr/bin/env python
import shapefile

sf = shapefile.Reader('../data/ZillowNeighborhoods-NY')


records = sf.records()
shapes = sf.shapes()

# Filter out only those of New York City
for index, record in enumerate(records):
    boroughs = ['New York', 'Bronx', 'Queens', 'Brooklyn', 'Staten Island']
    if record[1] in boroughs:
        join_data = {
            'name': record,
            'gps': shapes[index].bbox
        }
        print join_data
