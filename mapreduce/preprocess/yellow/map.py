#!/usr/bin/python

import sys
from datetime import datetime
	
#input comes from STDIN (stream data that goes to the program)
for line in sys.stdin:
    try:
        keys = []
        values = []
        rowtype = 1
        items = line.strip().split(',')
    
        if len(items) > 0:
            if items[0] == "VendorID":
                continue

        date_obj = datetime.strptime(item[1], '%Y-%m-%d %H:%M:%s')
        keys.append(date_obj.year)
        keys.append(date_obj.month)
        keys.append(date_obj.day)
        date_end = datetime.strptime(item[2], '%Y-%m-%d %H:%M:%s')
        rate_ID = 0
        
        values.append(items[0])
        values.append(date_end - date_obj)

        if len(items) == 21: #green
            rate_ID = int(item[4])
            rowtype = 1
            values.append(items[3])
            values.extend(items[5:])
        elif len(items) == 19: #yellow
            rate_ID = int(item[7])
            rowtype = 2
            values.extend(items[3:7])
            values.extend(items[3:8])
        print "%s\t%d,%d,%s" %(",".join(keys), rowtype, rate_ID, ",".join(values))  
    except:
        pass

# output        
# green
# year,month,day    1,rateID, triptime, sfflag, plon, plat, dlon, dlat, passcnt, tripdistance, fareAmount, extra, mtaTax, tipAmount, EhailFee, ImproveSurcharge, totalAmount, PaymentType, TripType
# yellow
# year,month,day    2,rateID, triptime, passcnt, tripdistance, plon, plat, sfflag, dlon, dlat, PaymentType, fareAmount, extra, mtaTax, tipAmount, tollsAmount, ImproveSurcharge, totalAmount