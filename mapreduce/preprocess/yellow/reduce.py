#!/usr/bin/python

import sys

trips = []
fares = dict()
#input comes from STDIN (stream data that goes to the program)
for line in sys.stdin:
    try:
        (key, value_items) = line.strip().split('\t', 1)
        (rowtype, value) = value_items.split(',', 1)
        if rowtype == '1':
            if key in fares:
                fares[key].append(value)
            else:
                fares[key] = [value]
        elif rowtype == '2':
            trips.append((key, value))
    except:
        pass

for (tkey, tvalue) in trips:
    flist = []
    if tkey in fares:
        flist = fares[tkey]
    for fare in flist:
        print "%s\t%s,%s" %(tkey, tvalue, fare)
