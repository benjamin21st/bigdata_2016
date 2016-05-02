#!/usr/bin/python

import sys
import traceback

yellow = [dict() for i in range(7)]
green = [dict() for i in range(7)]

def myfloat(input):
    ret = 0.0
    try:
        ret = float(input)
    except:
        pass
    return ret

'''
input:
# green
# year,month,day    1,rateID, sfflag, plon, plat, dlon, dlat, passcnt, tripdistance, fareAmount, extra, mtaTax, tipAmount, EhailFee, ImproveSurcharge, totalAmount, PaymentType, TripType
# yellow
# year,month,day    2,rateID, passcnt, tripdistance, plon, plat, sfflag, dlon, dlat, PaymentType, fareAmount, extra, mtaTax, tipAmount, tollsAmount, ImproveSurcharge, totalAmount
'''
'''
reduce:
key
year,
month,
day
0   0 or 1: green or yellow
1   ratetype
value
0   vendorIDis1
1   vendorIDis2
2   triptime
3   passenger count
4   trip distance
5   Store_and_fwd_Y
6   Store_and_fwd_N
7   fare amount
8   extra
9   mta tax
10  tip amount
11  ehail fee
12  improvement surcharge
13  total amount
14  payment 1
15  payment 2
16  payment 3
17  payment 4
18  payment 5
19  payment 6
20  trip type 0
21  trip type 1
22  trip type 2
23  tollsAmount
24  record count

'''
record_cnt = 25
#input comes from STDIN (stream data that goes to the program)
for line in sys.stdin:
    try:
        (key, value_items) = line.strip().split('\t', 1)
        (rowtype, value_items2) = value_items.split(',', 1)
        (ratetype, values) = value_items2.split(',', 1)
        value = values.split(',')
        ratetype = int(ratetype)
        #print value
        if rowtype == '1': #green
        #vendorID, triptime, sfflag, plon, plat, dlon, dlat, passcnt, tripdistance, fareAmount, 
        #          extra, mtaTax, tipAmount, tollAmount, EhailFee, ImproveSurcharge, totalAmount, PaymentType, TripType
            if key in green[ratetype]:
                green[ratetype][key][int(value[0])-1]  += 1
                green[ratetype][key][2]  += myfloat(value[1]) #triptime
                green[ratetype][key][3]  += myfloat(value[7]) #passenger count
                green[ratetype][key][4]  += myfloat(value[8]) #trip distance
                if value[2] == 'Y':
                    green[ratetype][key][5]  += 1 #Store_and_fwd_Y
                else:
                    green[ratetype][key][6]  += 1 #Store_and_fwd_N
                green[ratetype][key][7]  += myfloat(value[9]) #fare amount
                green[ratetype][key][8]  += myfloat(value[10]) #extra
                green[ratetype][key][9]  += myfloat(value[11]) #mta tax
                green[ratetype][key][10] += myfloat(value[12]) #tip amount
                green[ratetype][key][11] += myfloat(value[14]) #ehail fee
                green[ratetype][key][12] += myfloat(value[15]) #improvement surcharge
                green[ratetype][key][13] += myfloat(value[16]) #total amount
                payoffset = int(value[17])
                tripoffset = int(value[18 ])
                green[ratetype][key][13+payoffset] += 1
                '''
                green[ratetype][key][12] += myfloat() #payment 1
                green[ratetype][key][13] += myfloat() #payment 2
                green[ratetype][key][14] += myfloat() #payment 3
                green[ratetype][key][15] += myfloat() #payment 4
                green[ratetype][key][16] += myfloat() #payment 5
                green[ratetype][key][17] += myfloat() #payment 6
                '''
                green[ratetype][key][20+tripoffset] += 1
                '''
                green[ratetype][key][18] += myfloat() #trip type 0
                green[ratetype][key][19] += myfloat() #trip type 1
                green[ratetype][key][20] += myfloat() #trip type 2
                '''
                green[ratetype][key][23] += myfloat(value[13]) #tollsAmount 
                green[ratetype][key][record_cnt-1] += 1
                               
            else:
                green[ratetype][key] = [0] * record_cnt
                green[ratetype][key][int(value[0])-1]  += 1
                green[ratetype][key][2]  = myfloat(value[1]) #triptime
                green[ratetype][key][3]  = myfloat(value[7]) #passenger count
                green[ratetype][key][4]  = myfloat(value[8]) #trip distance
                if value[2] == 'Y':
                    green[ratetype][key][5]  = 1 #Store_and_fwd_Y
                else:
                    green[ratetype][key][6]  = 1 #Store_and_fwd_N
                green[ratetype][key][7]  = myfloat(value[9]) #fare amount
                green[ratetype][key][8]  = myfloat(value[10]) #extra
                green[ratetype][key][9]  = myfloat(value[11]) #mta tax
                green[ratetype][key][10] = myfloat(value[12]) #tip amount
                green[ratetype][key][11] = myfloat(value[14]) #ehail fee
                green[ratetype][key][12] = myfloat(value[15]) #improvement surcharge
                green[ratetype][key][13] = myfloat(value[16]) #total amount
                payoffset = int(value[17])
                tripoffset = int(value[18 ])
                green[ratetype][key][13+payoffset] = 1
                '''
                green[ratetype][key][12] = myfloat() #payment 1
                green[ratetype][key][13] = myfloat() #payment 2
                green[ratetype][key][14] = myfloat() #payment 3
                green[ratetype][key][15] = myfloat() #payment 4
                green[ratetype][key][16] = myfloat() #payment 5
                green[ratetype][key][17] = myfloat() #payment 6
                '''
                green[ratetype][key][20+tripoffset] = 1
                '''
                green[ratetype][key][18] = myfloat() #trip type 0
                green[ratetype][key][19] = myfloat() #trip type 1
                green[ratetype][key][20] = myfloat() #trip type 2
                '''
                green[ratetype][key][23] = myfloat(value[13]) #tollsAmount 
                green[ratetype][key][record_cnt-1] = 1
                
        elif rowtype == '2': #yellow
            # VendorID, tiptime ,passenger_count,trip_distance,pickup_longitude,pickup_latitude,RateCodeID,store_and_fwd_flag,dropoff_longitude,dropoff_latitude,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount
            #
            if key in yellow[ratetype]:
                yellow[ratetype][key][int(value[0]) - 1]  = 1 #vendorID

                yellow[ratetype][key][2]  += myfloat(value[1]) #triptime
                yellow[ratetype][key][3]  += myfloat(value[2]) #passenger count
                yellow[ratetype][key][4]  += myfloat(value[3]) #trip distance
                if value[6] == 'Y':
                    yellow[ratetype][key][5] += 1
                else:
                    yellow[ratetype][key][6] += 1
                '''
                yellow[ratetype][key][5]  += myfloat() #Store_and_fwd_Y
                yellow[ratetype][key][6]  += myfloat() #Store_and_fwd_N
                '''
                yellow[ratetype][key][7]  += myfloat(value[10]) #fare amount
                yellow[ratetype][key][8]  += myfloat(value[11]) #extra
                yellow[ratetype][key][9]  += myfloat(value[12]) #mta tax
                yellow[ratetype][key][10] += myfloat(value[13]) #tip amount
                yellow[ratetype][key][11] += myfloat(0) #ehail fee
                yellow[ratetype][key][12] += myfloat(value[15]) #improvement surcharge
                yellow[ratetype][key][13] += myfloat(value[16]) #total amount
                
                payoffset = int(value[9])
                tripoffset = int(0)
                yellow[ratetype][key][13+payoffset] += 1
                '''
                yellow[ratetype][key][14] += myfloat() #payment 1
                yellow[ratetype][key][15] += myfloat() #payment 2
                yellow[ratetype][key][16] += myfloat() #payment 3
                yellow[ratetype][key][17] += myfloat() #payment 4
                yellow[ratetype][key][18] += myfloat() #payment 5
                yellow[ratetype][key][19] += myfloat() #payment 6
                '''
                yellow[ratetype][key][20+tripoffset] += 1
                '''
                yellow[ratetype][key][20] += myfloat() #trip type 0
                yellow[ratetype][key][21] += myfloat() #trip type 1
                yellow[ratetype][key][22] += myfloat() #trip type 2
                '''
                yellow[ratetype][key][23] += myfloat(value[14]) #tollsAmount    
                yellow[ratetype][key][record_cnt-1] += 1
            else:
                row = [0] * record_cnt
                row[int(value[0]) - 1]  = 1 #vendorID

                row[2]  = myfloat(value[1]) #triptime
                row[3]  = myfloat(value[2]) #passenger count
                row[4]  = myfloat(value[3]) #trip distance
                if value[6] == 'Y':
                    row[5] += 1
                else:
                    row[6] += 1
                '''
                row[5]  = myfloat() #Store_and_fwd_Y
                row[6]  = myfloat() #Store_and_fwd_N
                '''
                row[7]  = myfloat(value[10]) #fare amount
                row[8]  = myfloat(value[11]) #extra
                row[9]  = myfloat(value[12]) #mta tax
                row[10] = myfloat(value[13]) #tip amount
                row[11] = myfloat(0) #ehail fee
                row[12] = myfloat(value[15]) #improvement surcharge
                row[13] = myfloat(value[16]) #total amount

                payoffset = int(value[9])
                tripoffset = int(0)
                row[13+payoffset] += 1
                '''
                row[14] = myfloat() #payment 1
                row[15] = myfloat() #payment 2
                row[16] = myfloat() #payment 3
                row[17] = myfloat() #payment 4
                row[18] = myfloat() #payment 5
                row[19] = myfloat() #payment 6
                '''
                row[20+tripoffset] += 1
                '''
                row[20] = myfloat() #trip type 0
                row[21] = myfloat() #trip type 1
                row[22] = myfloat() #trip type 2
                '''
                row[23] = myfloat(value[14]) 
                row[record_cnt-1] = 1 #cnt
                yellow[ratetype][key] = row
    except:
        traceback.print_exc()
        
        
for i in range(1, 7):
    #print green[i]
    for tkey in green[i].iterkeys():
        #print green[i][tkey]
        print "%s,1,%d \t%s" %(tkey, i, " ".join(map(str, green[i][tkey])))
        
for i in range(1, 7):
    for tkey in yellow[i].iterkeys():
        print "%s,2,%d \t%s" %(tkey, i, " ".join(map(str, yellow[i][tkey])))