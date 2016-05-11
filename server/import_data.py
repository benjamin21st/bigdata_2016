from models import *
from datetime import date
import sys
import glob
import errno


def insert_stats_row(line, id):
    (keys, values) = line.strip().split('\t', 1)
    (year, month, day, taxi_type, rate_type) = map(int, keys.split(','))
    value_list = map(float, values.split(','))
    dt = datetime.date(year, month, day)

    total_cnt_vendorID_1 = int(value_list[0])
    total_cnt_vendorID_2 = int(value_list[1])
    total_trip_time = value_list[2]
    total_pass_cnt = int(value_list[3])
    total_trip_dst = value_list[4]
    total_sfflag_Y = int(value_list[5])
    total_sfflag_N = int(value_list[6])
    total_fare_amount = value_list[7]
    total_extra = value_list[8]
    total_mta_tax = value_list[9]
    total_tip_amount = value_list[10]
    total_ehail_fee = value_list[11]
    total_imprv_srchg = value_list[12]
    total_total_amount = value_list[13]
    total_payment_1 = int(value_list[14])
    total_payment_2 = int(value_list[15])
    total_payment_3 = int(value_list[16])
    total_payment_4 = int(value_list[17])
    total_payment_5 = int(value_list[18])
    total_payment_6 = int(value_list[19])
    total_trip_type_0 = int(value_list[20])
    total_trip_type_1 = int(value_list[21])
    total_trip_type_2 = int(value_list[22])
    total_tolls_amount = int(value_list[23])
    total_record_cnt = int(value_list[24])

    ts = TripStats(id=id, datetime=dt, taxi_type=taxi_type,rate_type=rate_type,
                   total_cnt_vendorID_1 = total_cnt_vendorID_1,
                   total_cnt_vendorID_2 = total_cnt_vendorID_2,
                   total_trip_time = total_trip_time,
                   total_pass_cnt = total_pass_cnt,
                   total_trip_dst = total_trip_dst,
                   total_sfflag_Y = total_sfflag_Y,
                   total_sfflag_N = total_sfflag_N,
                   total_fare_amount = total_fare_amount,
                   total_extra = total_extra,
                   total_mta_tax = total_mta_tax,
                   total_tip_amount = total_tip_amount,
                   total_ehail_fee = total_ehail_fee,
                   total_imprv_srchg = total_imprv_srchg,
                   total_total_amount = total_total_amount,
                   total_payment_1 = total_payment_1,
                   total_payment_2 = total_payment_2,
                   total_payment_3 = total_payment_3,
                   total_payment_4 = total_payment_4,
                   total_payment_5 = total_payment_5,
                   total_payment_6 = total_payment_6,
                   total_trip_type_0 = total_trip_type_0,
                   total_trip_type_1 = total_trip_type_1,
                   total_trip_type_2 = total_trip_type_2,
                   total_tolls_amount = total_tolls_amount,
                   total_record_cnt = total_record_cnt)
    try:
        ts.save()
    except:
        # Roll back database transaction in case it blocks future operations
        session.rollback()
        print "Oops, something went terribly wrong"


def insert_spatial_row(line, id):
    (keys, values) = line.strip().split('\t', 1)
    (year, month, day, taxi_type, rate_type, action) = map(int, keys.split(','))
    dt = datetime.date(year, month, day)

    tss = TripSpatialStats(id=id, datetime=dt, taxi_type=taxi_type,
                           rate_type=rate_type, action = action,
                           total_record_cnt=values)

    try:
        tss.save()
    except:
        # Roll back database transaction in case it blocks future operations
        session.rollback()
        print "Oops, something went terribly wrong"


def load_data(paths, type):
    cnt = 0
    for path in paths:
        files = glob.glob(path)
        for name in files:
            print "read %s" % name
            try:
                with open(name, "r") as f: # No need to specify 'r': this is the default.
                    for line in f:
                    # lines = f.readline()
                    # for line in lines:
                        if type == 1:
                            try:
                                insert_stats_row(line, cnt)
                            except:
                                session.rollback()
                                logger.error("Unable to insert stats row")
                                pass
                            cnt += 1
                        elif type == 2:
                            try:
                                insert_spatial_row(line, cnt)
                                cnt += 1
                            except:
                                session.rollback()
                                logger.error("Unable to insert spatial row")
                                pass

            except IOError as exc:
                if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
                    raise # Propagate other kinds of IOError.
        print "%d rows" % cnt
    return


def test_row():
    insert_stats_row("2015,1,30,2,1	1,1,6685397.08333,785933.0,1155641.36,6411,467814,5389074.02,184854.0,236910.5,730305.14,0.0,142221.3,6752871.21997,305412,166972,1397,444,0,0,474225,0,0,69455.31,474225", 0)
    insert_spatial_row("2015,1,31,2,1,0	2,3,28439,26,0,3388,4,4784,0,0,0,3,4,3,42413,0,16,0,5,0,2,11162,427,0,221,0,66,79,35,1,0,726,0,14093,543,1323,5,0,18,3,10,14,0,5739,20,65,1916,11,514,51,5681,13,15,0,9,2,31611,751,67371,2443,0,3581,0,22,34,4081,0,1038,15,14,11,57,0,2,0,7920,18,8,0,851,2,6,5063,3024,66239,3,8847,33,6,2387,36469,17985,6,0,0,3,0,2213,34,160,544,32,317,0,4,44778,0,0,1882,16678,0,3415,0,44,2,2,1,5,14,0,30,10,0,0,57,24990,1796,0,1100",0)


def test_path():
    stat_path_list = ["../mapreduceresult/GreenResult/*", "../mapreduceresult/YellowResult/*"]
    poly_path_list = ["../mapreduceresult/YellowPolygonResult/*", "../mapreduceresult/GreenPolygonResult/*"]
    load_data(stat_path_list, 1)
    load_data(poly_path_list, 2)


if __name__ == "__main__":
    test_path()
