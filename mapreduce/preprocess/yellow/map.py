#!/usr/bin/python

import sys
	
#input comes from STDIN (stream data that goes to the program)
for line in sys.stdin:
    try:
        keys = []
        values = []
        rowtype = 1
        items = line.strip().split(',')
    
        if len(items) > 0:
            if items[0] == "medallion":
                continue
    
        if len(items) == 11: #fare
            keys.extend(items[0:4])
            values.extend(items[4:])
            rowtype = 1
        elif len(items) == 14: #trip
            keys.extend(items[0:3])
            keys.append(items[5])
            values.extend(items[3:5])
            values.extend(items[6:])
            rowtype = 2
        print "%s\t%d,%s" %(",".join(keys), rowtype, ",".join(values))  
    except:
        pass