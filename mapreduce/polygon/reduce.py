#!/usr/bin/python

import sys
import traceback

yellow = [[dict() for i in range(7)] for i in range(3)]
green = [[dict() for i in range(7)] for i in range(3)]

rowcnt = 129

def myfloat(input):
    ret = 0.0
    try:
        ret = float(input)
    except:
        pass
    return ret


def findIdx(value):
    ret = []
    if "_" in value:
        idxs = value.split('_')
        for i in idxs:
            pos = int(i)
            if pos > -1:
                ret.append(pos)
    else:
        if int(value) > 0:
            ret.append(int(value))
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
                print ratetype
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
