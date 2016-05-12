#!/usr/bin/python

import sys
import traceback

#yellow = [[dict() for i in range(8)] for i in range(3)]
#green = [[dict() for i in range(8)] for i in range(3)]

yellow = dict()

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
                prod_items[idx].append(pos)
    return ret


for line in sys.stdin:
    try:
        #2015,1,15	2,1,58_90_125,33_58

        (key, value_items) = line.strip().split('\t', 1)
        (rowtype, value_items2) = value_items.split(',', 1)
        (ratetype, values) = value_items2.split(',', 1)
        value_items = values.split(',')
        ratetype = int(ratetype)
        #print value
        # green[action][ratetype][time][poly_idx]
        for j, value in enumerate(value_items):
            if rowtype == '1': #green
                if key in green[j][ratetype]:
                    idxs = findIdx(value)
                    for idx in idxs:
                        green[j][ratetype][key][idx] += 1
                else:
                    row = [0 for i in range(rowcnt)]
                    green[j][ratetype][key] = row
                    idxs = findIdx(value)
                    for idx in idxs:
                        green[j][ratetype][key][idx] += 1
            elif rowtype == '2': #yellow
                if ratetype == 99:
                    ratetype = 7
                if key in yellow[j][ratetype]:
                    idxs = findIdx(value)
                    for idx in idxs:
                        yellow[j][ratetype][key][idx] += 1
                else:
                    row = [0 for i in range(rowcnt)]
                    yellow[j][ratetype][key] = row
                    idxs = findIdx(value)
                    for idx in idxs:
                        yellow[j][ratetype][key][idx] += 1
    except:
        print line
        traceback.print_exc()

for j,t in enumerate(green):
    for i in range(1, 7):
        for tkey in green[j][i].iterkeys():
            print "%s,1,%d,%d\t%s" %(tkey, i, j, ",".join(map(str, green[j][i][tkey])))

for j,t in enumerate(yellow):
    for i in range(1, 7):
        for tkey in yellow[j][i].iterkeys():
            print "%s,2,%d,%d\t%s" %(tkey, i, j, ",".join(map(str, yellow[j][i][tkey])))

#output
#year,month,day,cartype,ratetype,pickup(0)/dropoff(1), sum value vectors
