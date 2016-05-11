# TODO: fix this circular import
# import json
import simplejson as json
import sys
from app import app
from flask import request
from models import *

@app.route('/')
def index():
    return 'OMG, it worked!'

@app.route('/trips/count')
def count_trips():
    return json.dumps({'count': Trip.query.count()})

@app.route('/tripstats')
def get_trip_stats():
    offset = 0
    if 'offset' in request.args:
        offset = request.args['offset']
    trip_stats = TripStats.query.limit(100).all()
    data = []
    for ts in trip_stats:
        data.append({
            "datetime": ts.datetime.strftime('%s'),
            "taxi_type": ts.taxi_type,
            "rate_code": ts.rate_code,
            "total_cnt_vendorID_1": ts.total_cnt_vendorID_1,
            "total_cnt_vendorID_1": ts.total_cnt_vendorID_1,
            "total_trip_time": ts.total_trip_time,
            "total_pass_cnt": ts.total_pass_cnt,
            "total_trip_dst": ts.total_trip_dst,
            "total_sfflag_Y": ts.total_sfflag_Y,
            "total_sfflag_N": ts.total_sfflag_N,
            "total_fare_amount": ts.total_fare_amount,
            "total_extra": ts.total_extra,
            "total_mta_tax": ts.total_mta_tax,
            "total_tip_amount": ts.total_tip_amount,
            "total_ehail_fee": ts.total_ehail_fee,
            "total_imprv_srchg": ts.total_imprv_srchg,
            "total_total_amount": ts.total_total_amount,
            "total_payment_1": ts.total_payment_1,
            "total_payment_2": ts.total_payment_2,
            "total_payment_3": ts.total_payment_3,
            "total_payment_4": ts.total_payment_4,
            "total_payment_5": ts.total_payment_5,
            "total_payment_6": ts.total_payment_6,
            "total_trip_type_0": ts.total_trip_type_0,
            "total_trip_type_1": ts.total_trip_type_1,
            "total_trip_type_2": ts.total_trip_type_2,
            "total_tolls_amount": ts.total_tolls_amount,
            "total_record_cnt": ts.total_record_cnt
        })

    return return_json(data, 200)


def return_json(data, status):
    return json.dumps(data), status, {'contentType': 'Application/JSON'}


if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5000
    app.run(debug=True, port=port)
