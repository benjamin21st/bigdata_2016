#!/usr/bin/python

import sys

yellow = [dict()] * 7
green = [dict()] * 7

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
        (ratetype, value) = value_items2.split(',', 1)
        if rowtype == '1': #green
            if key in green[ratetype]:
                green[ratetype][key][int(value[0])-1]  += 1
                green[ratetype][key][2]  += float(value[1]) #triptime
                green[ratetype][key][3]  += float(value[7]) #passenger count
                green[ratetype][key][4]  += float(value[8]) #trip distance
                if value[2] == 'Y':
                    green[ratetype][key][5]  += 1 #Store_and_fwd_Y
                else:
                    green[ratetype][key][6]  += 1 #Store_and_fwd_N
                green[ratetype][key][7]  += float(value[9]) #fare amount
                green[ratetype][key][8]  += float(value[10]) #extra
                green[ratetype][key][9]  += float(value[11]) #mta tax
                green[ratetype][key][10] += float(value[12]) #tip amount
                green[ratetype][key][11] += float(value[13]) #ehail fee
                green[ratetype][key][12] += float(value[14]) #improvement surcharge
                green[ratetype][key][13] += float(value[15]) #total amount
                payoffset = int(value[16])
                tripoffset = int(value[17])
                green[ratetype][key][13+payoffset] += 1
                '''
                green[ratetype][key][12] += float() #payment 1
                green[ratetype][key][13] += float() #payment 2
                green[ratetype][key][14] += float() #payment 3
                green[ratetype][key][15] += float() #payment 4
                green[ratetype][key][16] += float() #payment 5
                green[ratetype][key][17] += float() #payment 6
                '''
                green[ratetype][key][20+tripoffset] += 1
                '''
                green[ratetype][key][18] += float() #trip type 0
                green[ratetype][key][19] += float() #trip type 1
                green[ratetype][key][20] += float() #trip type 2
                '''
                green[ratetype][key][23] += float(0) #tollsAmount 
                green[ratetype][key][record_cnt-1] += 1
                               
            else:
                row = [] * record_cnt
                row[int(value[0]) - 1]  = 1
                row[2]  = float(value[1]) #triptime
                row[3]  = float(value[7]) #passenger count
                row[4]  = float(value[8]) #trip distance
                if value[2] == 'Y':
                    row[5] = 1
                else:
                    row[6] = 1
                '''
                row[5]  = float() #Store_and_fwd_Y
                row[6]  = float() #Store_and_fwd_N
                '''
                row[7]  = float(value[9]) #fare amount
                row[8]  = float(value[10]) #extra
                row[9]  = float(value[11]) #mta tax
                row[10] = float(value[12]) #tip amount
                row[11] = float(value[13]) #ehail fee
                row[12] = float(value[14]) #improvement surcharge
                row[13] = float(value[15]) #total amount
                payoffset = int(value[16])
                tripoffset = int(value[17])
                row[13+payoffset] += 1
                '''
                row[14] = float() #payment 1
                row[15] = float() #payment 2
                row[16] = float() #payment 3
                row[17] = float() #payment 4
                row[18] = float() #payment 5
                row[19] = float() #payment 6
                '''
                row[20+tripoffset] += 1
                '''
                row[20] = float() #trip type 0
                row[21] = float() #trip type 1
                row[22] = float() #trip type 2
                '''
                row[23] = 0.0 #tollsAmount  
                row[record_cnt-1] = 1 #cnt  
                green[ratetype][key] = row
                
        elif rowtype == '2': #yellow
            if key in yellow[ratetype]:

                yellow[ratetype][key][0]  = float() #vendorID
                yellow[ratetype][key][1]  = float() #triptime
                yellow[ratetype][key][2]  = float() #passenger count
                yellow[ratetype][key][3]  = float() #trip distance
                yellow[ratetype][key][4]  = float() #Store_and_fwd_Y
                yellow[ratetype][key][5]  = float() #Store_and_fwd_N
                yellow[ratetype][key][6]  = float() #fare amount
                yellow[ratetype][key][7]  = float() #extra
                yellow[ratetype][key][8]  = float() #mta tax
                yellow[ratetype][key][9]  = float() #tip amount
                yellow[ratetype][key][10] = float() #ehail fee
                yellow[ratetype][key][11] = float() #improvement surcharge
                yellow[ratetype][key][12] = float() #total amount
                yellow[ratetype][key][13] = float() #payment 1
                yellow[ratetype][key][14] = float() #payment 2
                yellow[ratetype][key][15] = float() #payment 3
                yellow[ratetype][key][16] = float() #payment 4
                yellow[ratetype][key][17] = float() #payment 5
                yellow[ratetype][key][18] = float() #payment 6
                yellow[ratetype][key][19] = float() #trip type 0
                yellow[ratetype][key][20] = float() #trip type 1
                yellow[ratetype][key][21] = float() #trip type 2
                yellow[ratetype][key][22] = float() #tollsAmount    
                yellow[ratetype][key][record_cnt-1] += 1
                 
            else:
                row = [] * record_cnt
                row[0]  = float() #vendorID
                row[1]  = float() #triptime
                row[2]  = float() #passenger count
                row[3]  = float() #trip distance
                row[4]  = float() #Store_and_fwd_Y
                row[5]  = float() #Store_and_fwd_N
                row[6]  = float() #fare amount
                row[7]  = float() #extra
                row[8]  = float() #mta tax
                row[9]  = float() #tip amount
                row[10] = float() #ehail fee
                row[11] = float() #improvement surcharge
                row[12] = float() #total amount
                row[13] = float() #payment 1
                row[14] = float() #payment 2
                row[15] = float() #payment 3
                row[16] = float() #payment 4
                row[17] = float() #payment 5
                row[18] = float() #payment 6
                row[19] = float() #trip type 0
                row[20] = float() #trip type 1
                row[21] = float() #trip type 2
                row[22] = float() #tollsAmount        
                row[record_cnt-1] = 1 #cnt
                yellow[ratetype][key] = row
            
    except:
        pass

for (tkey, tvalue) in trips:
    flist = []
    if tkey in fares:
        flist = fares[tkey]
    for fare in flist:
        print "%s\t%s,%s" %(tkey, tvalue, fare)
