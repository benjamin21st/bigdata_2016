#!/usr/bin/env python
import shapefile

nycmap_path = '../data/ZillowNeighborhoods-NY'


def load_nyc_polygons(path):
    sf = shapefile.Reader(path)
    records = sf.records()
    shapes = sf.shapes()

    # Filter out only those of New York City
    idx = 0
    data_list = []
    for index, record in enumerate(records):
        boroughs = ['New York', 'Bronx', 'Queens', 'Kings', 'Richmond']
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


if __name__ == "__main__":
    lists = load_nyc_polygons(nycmap_path)
    print lists
