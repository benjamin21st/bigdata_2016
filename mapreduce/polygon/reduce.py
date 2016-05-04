#!/usr/bin/python

import sys
import traceback

yellow = [dict() for i in range(7)]
green = [dict() for i in range(7)]

rowcnt = 128

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
        for idx in idxs:
            pos = (int) idx
            if pos > -1:
                ret.append(pos)
    else:
        ret.append(int(value))
    return ret
    

for line in sys.stdin:
    try:
        #2015,1,15	2,1,58_90_125,33_58
        
        (key, value_items) = line.strip().split('\t', 1)
        (rowtype, value_items2) = value_items.split(',', 1)
        (ratetype, values) = value_items2.split(',', 1)
        value = values.split(',')
        ratetype = int(ratetype)
        #print value
        if rowtype == '1': #green
            if key in green[ratetype]:
                idxs = findIdx(value)
                for idx in idxs:
                    green[ratetype][idx] += 1
            else:
                row = [0 for i in range(rowcnt)]
                green[ratetype] = row
                idxs = findIdx(value)
                for idx in idxs:
                    green[ratetype][idx] += 1
        elif rowtype == '2': #yellow
            if key in yellow[ratetype]:
                idxs = findIdx(value)
                for idx in idxs:
                    yellow[ratetype][idx] += 1
            else:
                row = [0 for i in range(rowcnt)]
                yellow[ratetype] = row
                idxs = findIdx(value)
                for idx in idxs:
                    yellow[ratetype][idx] += 1
                    
for i in range(1, 7):
    #print green[i]
    for tkey in green[i].iterkeys():
        #print green[i][tkey]
        print "%s,1,%d\t%s" %(tkey, i, ",".join(map(str, green[i][tkey])))
        
for i in range(1, 7):
    for tkey in yellow[i].iterkeys():
        print "%s,2,%d\t%s" %(tkey, i, ",".join(map(str, yellow[i][tkey])))
        
#output
#district, pick_up/dropoff, cartype, ratetype, times, date