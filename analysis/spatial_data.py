from datetime import date
import sys
import glob
import errno
import datetime


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


class AllTrip:
    def __init__(self):
        self.polylist = []

    def insert_data(self, poly):
        self.polylist.append(poly)

    def assign(self, poly_list):
        self.polylist = poly_list

    def get_data(self, date_begin, date_end, rate_code=-1, taxi_type=-1, action=-1):
        result = [0 for x in range(129)]
        for poly in self.polylist:
            score = 0
            if date_begin <= poly.datetime <= date_end:
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


def insert_spatial_row(line):
    (keys, values) = line.strip().split('\t', 1)
    (year, month, day, taxi_type, rate_type, action) = map(int, keys.split(','))
    dt = datetime.date(year, month, day)

    tss = TripSpatialStats(datetime=dt, taxi_type=taxi_type,
                           rate_type=rate_type, action = action,
                           total_record_cnt=values)

    return tss


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


def load_data(paths, type=1):
    cnt = 1
    ret = []
    for path in paths:
        files = glob.glob(path)
        for name in files:
            print "read %s" % name
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
        print "%d rows" % cnt
    return ret


def test_row():
    ret = insert_spatial_row("2015,1,31,2,1,0	2,3,28439,26,0,3388,4,4784,0,0,0,3,4,3,42413,0,16,0,5,0,2,11162,427,0,221,0,66,79,35,1,0,726,0,14093,543,1323,5,0,18,3,10,14,0,5739,20,65,1916,11,514,51,5681,13,15,0,9,2,31611,751,67371,2443,0,3581,0,22,34,4081,0,1038,15,14,11,57,0,2,0,7920,18,8,0,851,2,6,5063,3024,66239,3,8847,33,6,2387,36469,17985,6,0,0,3,0,2213,34,160,544,32,317,0,4,44778,0,0,1882,16678,0,3415,0,44,2,2,1,5,14,0,30,10,0,0,57,24990,1796,0,1100")
    return ret


def test_path():
    at = AllTrip()
    poly_path_list = ["../mapreduceresult/YellowPolygonResult/*", "../mapreduceresult/GreenPolygonResult/*"]
    list = load_data(poly_path_list, 1)
    at.assign(list)
    data_201511 = at.get_data(datetime.date(2015,1,1), datetime.date(2015,1,1))
    #load_data(poly_path_list, 3)

    result = [0 for x in range(129)]
    for poly in at.polylist:
        if poly.datetime==datetime.date(2015,1,1):
            result = [x+y for x, y in zip(result, poly.records)]
    print result==data_201511

if __name__ == "__main__":
    #print test_row()
    test_path()
