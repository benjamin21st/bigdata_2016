#!/usr/bin/python

import sys
import traceback

#yellow = [[dict() for i in range(8)] for i in range(3)]
#green = [[dict() for i in range(8)] for i in range(3)]

trip_stats = dict()

rowcnt = 129


def myfloat(input):
    ret = 0.0
    try:
        ret = float(input)
    except:
        pass
    return ret


def findAllIdx(value_items):
    ret = []

    prod_items = [list()] * 2
    for idx, value in enumerate(value_items):
        if "_" in value:
            idxs = value.split('_')
            for i in idxs:
                pos = int(i)
                if pos > -1:
                    prod_items[idx].append(pos)
        else:
            if int(value) >= 0:
                prod_items[idx].append(int(value))

    for item in prod_items[0]:
        for item2 in prod_items[1]:
            ret.append(str(item)+","+str(item2))

    return ret


for line in sys.stdin:
    try:
        #2015,1,15	2,1,58_90_125,33_58
        (key, value_items) = line.strip().split('\t', 1)
        (rowtype, value_items2) = value_items.split(',', 1)
        (ratetype, values) = value_items2.split(',', 1)
        value_items = values.split(',')
        #print value
        # green[action][ratetype][time][poly_idx]

        reduce_keys = findAllIdx(value_items)
        for reduce_key in reduce_keys:
            rk = reduce_key+","+rowtype+","+ratetype
            if rk in trip_stats:
                trip_stats[rk] += 1
            else:
                trip_stats[rk] = 1
    except:
        #traceback.print_exc()

for tkey in trip_stats.iterkeys():
    print "%s\t%d" % (tkey, trip_stats[tkey])

#output
#from_poly_id, to_poly_id , car_type, rate_type, count
