# TODO: fix this circular import
# import json
import simplejson as json
import sys
import os
from app import app
from flask import request, send_from_directory
from sqlalchemy import extract
from sqlalchemy.sql import func
from models import *

COLOR_CODE = {
    'green': 1,
    'yellow': 2
}

@app.route('/')
def index():
    curdir = os.getcwd()

    return send_from_directory(curdir, 'index.html')

# Disable:
# There aren't really any data in Trip table
# @app.route('/trips/count')
# def count_trips():
#     return json.dumps({'count': Trip.query.count()})

@app.route('/tripstats')
def get_trip_stats():
    offset = 0
    base_query = TripStats.query
    if 'limit' in request.args:
        limit = int(request.args['limit'])
        trip_stats = base_query.limit(limit).all()
    else:
        trip_stats = base_query.all()
    data = []
    for ts in trip_stats:
        data.append(jsonify_trip(ts))

    return return_json(data)


# example: http://localhost:5011/tripstats/green?count
@app.route('/tripstats/<path:color>')
def get_taxi_data_by_type(color):
    taxi_type = COLOR_CODE[color]
    trip_stats = session.query(TripStats).filter(TripStats.taxi_type == taxi_type).all()
    data = []
    for ts in trip_stats:
        data.append(jsonify_trip(ts))
    return return_json(data)


@app.route('/tripstats/count/<path:color>')
def get_taxi_data_count(color):
    if color == 'all':
        base_query = session.query(func.sum(TripStats.total_record_cnt))
        yellow_count = base_query.filter(TripStats.taxi_type == 2).first()[0]
        green_count = base_query.filter(TripStats.taxi_type == 1).first()[0]

        return return_json({
            "yellow": {
                "day": int(yellow_count/365),
                "week": int(yellow_count/52),
                "month": int(yellow_count/12),
                "year": int(yellow_count)
            },
            "green": {
                "day": int(green_count/365),
                "week": int(green_count/52),
                "month": int(green_count/12),
                "year": int(green_count)
            }
        })
    taxi_type = COLOR_CODE[color]
    count = session.query(func.sum(TripStats.total_record_cnt)).filter(TripStats.taxi_type == taxi_type).first()[0]
    if 'average' in request.args:
        if request.args['average'] == 'day':
            return return_json({"count": int(count/365), "type": color})
        elif request.args['average'] == 'month':
            return return_json({"count": int(count/12), "type": color})
        elif request.args['average'] == 'week':
            return return_json({"count": int(count/52), "type": color})
    return return_json({"count": count, "type": color})


@app.route('/tripstats/distribution/<path:color>')
def get_taxi_data_distribution(color):
    if color != 'all':
        taxi_type = COLOR_CODE[color]

    # TODO:
    # By default, we will just return a key-value pair of month and count
    out_data = []
    if 'interval' in request.args:
        if request.args['interval'] == 'month':
            # distribution by month
            # NOTE: Using a different mechanism now!!!!!!
            for i in range(1, 13):
                # out_data.append({
                #     "date": i,
                #     "count": session.query(func.sum(TripStats.total_record_cnt)).filter(TripStats.taxi_type == taxi_type, extract('month', TripStats.datetime) == i).first()[0]
                # })
                out_data.append({
                    "date": i,
                    "type": 2,
                    "count": session.query(func.sum(TripStats.total_record_cnt)).filter(TripStats.taxi_type == 2, extract('month', TripStats.datetime) == i).first()[0]
                })
                out_data.append({
                    "date": i,
                    "type": 1,
                    "count": session.query(func.sum(TripStats.total_record_cnt)).filter(TripStats.taxi_type == 1, extract('month', TripStats.datetime) == i).first()[0]
                })
        elif request.args['interval'] == 'week':
            # distribution by weekday
            yellow_trips = TripStats.query.filter(TripStats.taxi_type == 2).all()
            green_trips = TripStats.query.filter(TripStats.taxi_type == 1).all()
            mid_data_yellow = {}
            mid_data_green = {}
            for i in range(0, 8):
                for trip in yellow_trips:
                    if i in mid_data_yellow and trip.datetime.weekday() == i:
                        mid_data_yellow[i] += trip.total_record_cnt
                    elif trip.datetime.weekday() == i:
                        mid_data_yellow[i] = trip.total_record_cnt
            for i in range(0, 8):
                for trip in green_trips:
                    if i in mid_data_green and trip.datetime.weekday() == i:
                        mid_data_green[i] += trip.total_record_cnt
                    elif trip.datetime.weekday() == i:
                        mid_data_green[i] = trip.total_record_cnt

            for key, val in mid_data_yellow.items():
                out_data.append({
                    "date": key,
                    "type": 2,
                    "count": val
                })
            for key, val in mid_data_green.items():
                out_data.append({
                    "date": key,
                    "type": 1,
                    "count": val
                })

    return return_json(out_data)


# example: http://localhost:5011/tripstats/dist/yellow?range=year
@app.route('/tripstats/dist/<path:color>')
def get_taxi_travel_distance(color):
    if color != 'all':
        taxi_type = COLOR_CODE[color]

    if 'range' in request.args:
        total_distance = session.query(func.sum(TripStats.total_trip_dst)).filter(TripStats.taxi_type == taxi_type).first()[0]
        if request.args['range'] == 'year':
            distance = total_distance
        elif request.args['range'] == 'month':
            distance = float("%.2f" % (total_distance/12))
        elif request.args['range'] == 'week':
            distance = float("%.2f" % (total_distance/52))
        elif request.args['range'] == 'day':
            distance = float("%.2f" % (total_distance/365))

        return return_json({"type": color, "distance": distance})
    else:
        total_yellow = session.query(func.sum(TripStats.total_trip_dst)).filter(TripStats.taxi_type == 2).first()[0]
        total_green = session.query(func.sum(TripStats.total_trip_dst)).filter(TripStats.taxi_type == 1).first()[0]
        return return_json({"yellow": total_yellow, "green": total_green})


@app.route('/tripstats/passengers/<path:color>')
def get_taxi_passenger_count(color):
    if color == 'all':
        base_query = session.query(func.sum(TripStats.total_pass_cnt))
        yellow_count = base_query.filter(TripStats.taxi_type == 2).first()[0]
        green_count = base_query.filter(TripStats.taxi_type == 1).first()[0]

        return return_json({
            "yellow": {
                "year": yellow_count,
                "month": int(yellow_count/12),
                "week": int(yellow_count/52),
                "day": int(yellow_count/365)
            },
            "green": {
                "year": green_count,
                "month": int(green_count/12),
                "week": int(green_count/52),
                "day": int(green_count/365)
            }
        })

    taxi_type = COLOR_CODE[color]

    if 'range' in request.args:
        total_cnt = session.query(func.sum(TripStats.total_pass_cnt)).filter(TripStats.taxi_type == taxi_type).first()[0]
        if request.args['range'] == 'year':
            cnt = total_cnt
        elif request.args['range'] == 'month':
            cnt = int(total_cnt / 12)
        elif request.args['range'] == 'week':
            cnt = int(total_cnt / 52)
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
