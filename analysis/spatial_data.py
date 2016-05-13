from datetime import date
import sys
import glob
import errno
import operator
import datetime
sys.path.append('../server/')
from city_polygons import *


class TripSpatialStats():
    datetime = datetime.datetime.now
    taxi_type = 0
    rate_code = 0
    action = 0
    total_record_cnt = ""

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.records = map(int, self.total_record_cnt.split(','))


class TripPolygonStats:
    datetime = datetime.datetime.now
    taxi_type = 0
    rate_code = 0
    action = 0
    PolygonId = 0
    Count = 0

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


class NghTripStats:
    from_id = 0
    to_id = 0
    taxi_type = 0
    rate_code = 0
    Count = 0

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


class AllTrip:
    def __init__(self):
        self.polylist = []

    def insert_data(self, poly):
        self.polylist.append(poly)

    def assign(self, poly_list):
        self.polylist = poly_list

    def get_sum_data(self, date_list, rate_code=-1, taxi_type=-1, action=-1):
        result = [0 for x in range(129)]
        for poly in self.polylist:
            score = 0
            if poly.datetime in date_list:
                score += 1
            if rate_code == -1 or rate_code == poly.rate_code:
                score += 1
            if taxi_type == -1 or taxi_type == poly.taxi_type:
                score += 1
            if action == -1 or action == poly.action:
                score += 1

            if score == 4:
                result = [x+y for x, y in zip(result, poly.records)]

        return result

    def get_max_in_polygons(self, poly_id_list, date_list, rate_code=-1, taxi_type=-1, action=-1):
        result = 0
        max_poly = TripSpatialStats()
        for idx, poly in enumerate(self.polylist):
            score = 0
            if poly.datetime in date_list:
                score += 1
            if rate_code == -1 or rate_code == poly.rate_code:
                score += 1
            if taxi_type == -1 or taxi_type == poly.taxi_type:
                score += 1
            if action == -1 or action == poly.action:
                score += 1

            if score == 4:
                for poly_id in poly_id_list:
                    result = max(poly.records[poly_id], result)
                    max_poly = poly
                    max_poly_id = poly_id

        return result, max_poly.datetime, max_poly.action, max_poly.taxi_type, max_poly.rate_code, max_poly_id

    def load_data(self, paths, type=1):
        cnt = 1
        ret = []
        for path in paths:
            files = glob.glob(path)
            for name in files:
                #print "read %s" % name
                try:
                    with open(name, "r") as f: # No need to specify 'r': this is the default.
                        for line in f:
                            if type == 1:
                                tss = insert_spatial_row(line)
                                ret.append(tss)
                                cnt += 1
                            elif type == 2:
                                tss_list = insert_spatial_row(line)
                                ret.extend(tss_list)
                                cnt += len(tss_list)
                except IOError as exc:
                    if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
                        raise # Propagate other kinds of IOError.
            #print "%d rows" % cnt
        self.polylist = ret
        return ret

    def add_polygon_name(self, data_all, polygons):
        tripdict = {}
        for id, trip_num in enumerate(data_all):
            tripdict[polygons[id]['name'][3]+", "+polygons[id]['name'][2]] = trip_num

        return tripdict

    def print_jsonfy(self, list):
        print "{"
        for idx, value in enumerate(list):
            print '\"%d\":%d,' % (idx, value)
        print "}"

class TripFromTo:
    def __init__(self):
        # [f_id][to_id][rate_type][car_type] = count
        self.tripMatrix = [[[[0,0] for i in range(8)] for j in range(129)] for k in range(129)]
        self.tripList = []

    def load_data(self, paths):
        cnt = 1
        ret = []
        for path in paths:
            files = glob.glob(path)
            for name in files:
                #print "read %s" % name
                try:
                    with open(name, "r") as f: # No need to specify 'r': this is the default.
                        for line in f:
                            ngbItem = parse_trip_data(line)
                            self.tripList.append(ngbItem)
                            cnt += 1
                except IOError as exc:
                    if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
                        raise # Propagate other kinds of IOError.
            #print "%d rows" % cnt

    def get_sum_data(self, rate_code=-1, taxi_type=-1, only_different=False):
        result = [[0 for j in range(129)] for k in range(129)]
        for idx, items in enumerate(self.tripList):
            score = 0
            if rate_code == -1 or items.rate_code == rate_code:
                score += 1
            if taxi_type == -1 or items.taxi_type == taxi_type:
                score += 1

            if score == 2:
                result[items.from_id][items.to_id] += items.Count

        rank_dict = dict()
        for idr,row in enumerate(result):
            for idc, col in enumerate(row):
                if only_different and idr == idc:
                    continue
                rank_dict[str(idr)+","+str(idc)] = col

        return result, rank_dict

    def add_polygon_name(self, rank_dict, polygons):
        tripdict = {}
        for k,v in rank_dict.iteritems():
            fid, tid = map(int, k.split(','))
            tripdict[polygons[fid]['name'][3]+", "+polygons[fid]['name'][2]
                 + " => "+polygons[tid]['name'][3]+", "+polygons[tid]['name'][2]] = v

        sorted_list = sorted(tripdict.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_list

def insert_spatial_row(line):
    (keys, values) = line.strip().split('\t', 1)
    (year, month, day, taxi_type, rate_type, action) = map(int, keys.split(','))
    dt = datetime.date(year, month, day)

    tss = TripSpatialStats(datetime=dt, taxi_type=taxi_type,
                           rate_type=rate_type, action = action,
                           total_record_cnt=values)

    return tss


def parse_trip_data(line):
    (keys, cnt) = line.split('\t')
    key_items = map(int, keys.strip().split(','))
    return NghTripStats(from_id=key_items[0], to_id=key_items[1], taxi_type=key_items[2], rate_type=key_items[3], Count=int(cnt))



def insert_polyon_row(line):
    polygon_list = []
    (keys, values) = line.strip().split('\t', 1)
    (year, month, day, taxi_type, rate_type, action) = map(int, keys.split(','))
    dt = datetime.date(year, month, day)
    value_items = values.split(',')
    #print len(value_items)

    for i in range(0, len(value_items)):
        tss = TripPolygonStats(datetime=dt, taxi_type=taxi_type,
                               rate_type=rate_type, action=action,
                               PolygonId=i, Count=int(value_items[i]))

        polygon_list.append(tss)

    return polygon_list


def test_row():
    ret = insert_spatial_row("2015,1,31,2,1,0	2,3,28439,26,0,3388,4,4784,0,0,0,3,4,3,42413,0,16,0,5,0,2,11162,427,0,221,0,66,79,35,1,0,726,0,14093,543,1323,5,0,18,3,10,14,0,5739,20,65,1916,11,514,51,5681,13,15,0,9,2,31611,751,67371,2443,0,3581,0,22,34,4081,0,1038,15,14,11,57,0,2,0,7920,18,8,0,851,2,6,5063,3024,66239,3,8847,33,6,2387,36469,17985,6,0,0,3,0,2213,34,160,544,32,317,0,4,44778,0,0,1882,16678,0,3415,0,44,2,2,1,5,14,0,30,10,0,0,57,24990,1796,0,1100")
    return ret


def build_spatial_data():
    polygons = load_nyc_polygons(nycmap_path)
    at = AllTrip()
    poly_path_list = ["../mapreduceresult/YellowPolygonResult/*", "../mapreduceresult/GreenPolygonResult/*"]

    at.load_data(poly_path_list, 1)

    base = datetime.date(2015,1,1)
    date_list = [base + datetime.timedelta(days=x) for x in range(0, 366)]
    data_all = at.get_sum_data(date_list, action=1)
    #load_data(poly_path_list, 3)

    at.print_jsonfy(data_all)

    #tripdict = at.add_polygon_name(data_all, polygons)
    #sorted_list = sorted(tripdict.items(), key=operator.itemgetter(1), reverse=True)

    #for record in sorted_list:
    #    print record


def build_cm_data(filterlist=['New York City-Manhattan',
                              'New York City-Queens',
                              'New York City-Bronx',
                              'New York City-Brooklyn',
                              'New York City-Staten Island']):
    polygons = load_nyc_polygons(nycmap_path)
    tft = TripFromTo()
    poly_path_list = ["../mapreduceresult/YellowNghTripStatsMerge/*", "../mapreduceresult/GreenNghTripStatsMerge/*"]

    tft.load_data(poly_path_list)

    rank, rank_dict = tft.get_sum_data()

    labels, cities = get_polygons_header()

    headers = []
    for idx, label in enumerate(labels):
        if cities[idx] in filterlist:
            headers.append(label)

    print(",".join(map(str, headers)))
    for idx, row in enumerate(rank):
        show = []
        if cities[idx] in filterlist:
            show.append(labels[idx])
            for ridx, val in enumerate(row):
                if cities[ridx] in filterlist:
                    show.append(val)
        if len(show) > 0:
            print(",".join(map(str, show)))

    '''
    sorted_list = tft.add_polygon_name(rank_dict, polygons)

    for record in sorted_list:
        print record
    '''

    '''
    rank, rank_dict = tft.get_sum_data(only_different=True)
    sorted_list = tft.add_polygon_name(rank_dict, polygons)

    for record in sorted_list:
        print record
    '''


if __name__ == "__main__":
    #print test_row()

    #build_spatial_data()

    #build_cm_data()
    build_cm_data(['New York City-Manhattan'])
