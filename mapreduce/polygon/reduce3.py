#!/usr/bin/python

import sys
import traceback

#yellow = [[dict() for i in range(8)] for i in range(3)]
#green = [[dict() for i in range(8)] for i in range(3)]

trip_stats = dict()

for line in sys.stdin:
    try:
        #2015,1,15	2,1,58_90_125,33_58
        (key, value) = line.strip().split('\t', 1)
        if key in trip_stats:
            trip_stats[key] += int(value)
        else:
            trip_stats[key] = int(value)
    except:
        pass
        #traceback.print_exc()

for tkey in trip_stats.iterkeys():
    print "%s\t%d" % (tkey, trip_stats[tkey])

#output
#from_poly_id, to_poly_id , car_type, rate_type, count
