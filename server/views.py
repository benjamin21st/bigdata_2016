# TODO: fix this circular import
# import json
import simplejson as json
import sys
from app import app
from flask import request
from sqlalchemy import extract
from sqlalchemy.sql import func
from models import *

COLOR_CODE = {
    'green': 1,
    'yellow': 2
}

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
        offset = int(request.args['offset'])
    trip_stats = TripStats.query.limit(100).all()
    data = []
    for ts in trip_stats:
        data.append(jsonify_trip(ts))

    return return_json(data)


# example: http://localhost:5011/tripstats/green?count
@app.route('/tripstats/<path:color>')
def get_taxi_data_by_type(color):
    taxi_type = COLOR_CODE[color]

    base_query = TripStats.query
    if 'count' in request.args:
        return return_json({"count": base_query.filter(TripStats.taxi_type == taxi_type).count(), "type": color})
    if 'interval' in request.args:
        # TODO:
        # By default, we will just return a key-value pair of month and count
        if request.args['interval'] == 'monthly':
            out_data = {}
            for i in range(1, 13):
                out_data[i] = session.query(TripStats).filter(TripStats.taxi_type == taxi_type, extract('month', TripStats.datetime) == i).count()
            return return_json(out_data)

    trip_stats = base_query.filter(TripStats.taxi_type == taxi_type).all()
    data = []
    for ts in trip_stats:
        data.append(jsonify_trip(ts))
    return return_json(data)

# example: http://localhost:5011/tripstats/dist/yellow?range=year
@app.route('/tripstats/dist/<path:color>')
def get_taxi_travel_distance(color):
    taxi_type = COLOR_CODE[color]

    if 'range' in request.args:
        if request.args['range'] == 'year':
            outdata = session.query(func.sum(TripStats.total_trip_dst)).filter(TripStats.taxi_type == taxi_type).first()
            return return_json({"type": color, "distance": outdata[0]})

    return return_json({})

@app.route('/tripstats/passengers/<path:color>')
def get_taxi_passenger_count(color):
    taxi_type = COLOR_CODE[color]

    if 'range' in request.args:
        total_cnt = session.query(func.sum(TripStats.total_pass_cnt)).filter(TripStats.taxi_type == taxi_type).first()[0]
        if request.args['range'] == 'year':
            cnt = total_cnt
        elif request.args['range'] == 'month':
            cnt = int(total_cnt / 12)
        elif request.args['range'] == 'day':
            cnt = int(total_cnt / 365)
        else:
            cnt = total_cnt
        return return_json({"type": color, "passengers_count": cnt})
    else:
        return return_json({"error": "please specify a range, example: /tripstats/passengers/green?range=year "})

# example: A typical taxi travels 70,000 miles per year
# example: Trips: 485,000 per day | 175 MILLION per year
# example: Passengers: 600,000 per day | 236 MILLION per year

@app.route('/spatialstats')
def get_spatial_stats():
    offset = 0
    if 'offset' in request.args:
        offset = int(request.args['offset'])
    spatial_stats = TripSpatialStats.query.all()
    data = []
    for ss in spatial_stats:
        data.append({
            "datetime": ss.datetime.strftime('%s'),
            "taxi_type": ss.taxi_type,
            "rate_code": ss.rate_code,
            "action": ss.action,
            "total_record_cnt": ss.total_record_cnt
            })
    return return_json(data)


def jsonify_trip(trip):
    return {
            "datetime": trip.datetime.strftime('%s'),
            "taxi_type": trip.taxi_type,
            "rate_code": trip.rate_code,
            "total_cnt_vendorID_1": trip.total_cnt_vendorID_1,
            "total_cnt_vendorID_1": trip.total_cnt_vendorID_1,
            "total_trip_time": trip.total_trip_time,
            "total_pass_cnt": trip.total_pass_cnt,
            "total_trip_dst": trip.total_trip_dst,
            "total_sfflag_Y": trip.total_sfflag_Y,
            "total_sfflag_N": trip.total_sfflag_N,
            "total_fare_amount": trip.total_fare_amount,
            "total_extra": trip.total_extra,
            "total_mta_tax": trip.total_mta_tax,
            "total_tip_amount": trip.total_tip_amount,
            "total_ehail_fee": trip.total_ehail_fee,
            "total_imprv_srchg": trip.total_imprv_srchg,
            "total_total_amount": trip.total_total_amount,
            "total_payment_1": trip.total_payment_1,
            "total_payment_2": trip.total_payment_2,
            "total_payment_3": trip.total_payment_3,
            "total_payment_4": trip.total_payment_4,
            "total_payment_5": trip.total_payment_5,
            "total_payment_6": trip.total_payment_6,
            "total_trip_type_0": trip.total_trip_type_0,
            "total_trip_type_1": trip.total_trip_type_1,
            "total_trip_type_2": trip.total_trip_type_2,
            "total_tolls_amount": trip.total_tolls_amount,
            "total_record_cnt": trip.total_record_cnt
        }


def return_json(data, status=200):
    return json.dumps(data), status, {'contentType': 'Application/JSON'}


if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5000
    app.run(debug=True, port=port)
