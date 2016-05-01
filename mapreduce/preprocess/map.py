#!/usr/bin/python

import sys
import traceback
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

        date_obj = datetime.strptime(items[1], '%Y-%m-%d %H:%M:%S')
        keys.append(str(date_obj.year))
        keys.append(str(date_obj.month))
        keys.append(str(date_obj.day))
        date_end = datetime.strptime(items[2], '%Y-%m-%d %H:%M:%S')
        rate_ID = 0
        
        values.append(items[0])
        td = date_end - date_obj
        total_second = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
        values.append(str(total_second/60.0))
        if len(items) == 23: #green
            rate_ID = int(items[4])
            rowtype = 1
            values.append(items[3])
            values.extend(items[5:])
        elif len(items) == 19: #yellow
            rate_ID = int(items[7])
            rowtype = 2
            values.extend(items[3:7])
            values.extend(items[8:])
        print "%s\t%d,%d,%s" % (",".join(keys), rowtype, rate_ID, ",".join(values))
    except:
        traceback.print_exc()
# output
# green
# year,month,day    1,rateID, vendorID, triptime, sfflag, plon, plat, dlon, dlat, passcnt, tripdistance, fareAmount, extra, mtaTax, tipAmount, tollAmount, EhailFee, ImproveSurcharge, totalAmount, PaymentType, TripType
# yellow
# year,month,day    2,rateID, vendorID, triptime, passcnt, tripdistance, plon, plat, sfflag, dlon, dlat, PaymentType, fareAmount, extra, mtaTax, tipAmount, tollsAmount, ImproveSurcharge, totalAmount