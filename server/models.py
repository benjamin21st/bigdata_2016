import datetime
import logging
from app import db

from sqlalchemy import desc
from sqlalchemy.dialects import mysql

session = db.session

# Override with the "db." prefix, minimum code change?
Base = db.Model
Column = db.Column
String = db.String
# Integer = db.Integer
Integer = mysql.INTEGER
DateTime = db.DateTime
Boolean = db.Boolean
Text = db.Text
ForeignKey = db.ForeignKey
Numeric = db.Numeric
BigInt = db.BigInteger
SmallInt = db.SmallInteger
Decimal = db.DECIMAL


logging.basicConfig(filename='db_log.txt', level=logging.DEBUG,
                    format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)


class BaseAttr(object):
    created_at = Column(DateTime(), default=datetime.datetime.now)
    updated_at = Column(DateTime(), default=datetime.datetime.now)

    def __repr__(self):
        return "<Obj {}>".format(self.id)

    def save(self):
        session.add(self)
        session.commit()
        self.updated_at = datetime.datetime.now()
        return self

    def delete(self):
        session.delete(self)
        session.commit()


class Trip(BaseAttr, Base):
    __tablename__ = 'trips'

    id = Column(Integer(), primary_key=True)
    medallion = Column(String(50))
    hack_license = Column(String(50))
    vendor_id = Column(String(3))
    rate_code = Column(Integer(6))
    store_and_fwd_flag = Column(String(3))
    pickup_datetime = Column(DateTime(), nullable=False, default=datetime.datetime.now)
    dropoff_datetime = Column(DateTime(), nullable=False, default=datetime.datetime.now)
    passenger_count = Column(Integer(6))
    trip_time_in_secs = Column(Integer(11))
    trip_distance = Column(Decimal(12, 5))
    pickup_longitude = Column(Decimal(15, 10))
    pickup_latitude = Column(Decimal(15, 10))
    dropoff_longitude = Column(Decimal(15, 10))
    dropoff_latitude =  Column(Decimal(15, 10))

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


class TripStats(BaseAttr, Base):
    __tablename__ = 'tripsStats'

    id = Column(Integer(), primary_key=True)
    datetime = Column(DateTime(), nullable=False, default=datetime.datetime.now)
    taxi_type = Column(Integer(6))
    rate_code = Column(Integer(6))

    total_cnt_vendorID_1 = Column(Integer(10))
    total_cnt_vendorID_2 = Column(Integer(10))
    total_trip_time = Column(Decimal(12,5))
    total_pass_cnt = Column(Integer(10))
    total_trip_dst = Column(Decimal(12,5))
    total_sfflag_Y = Column(Integer(10))
    total_sfflag_N = Column(Integer(10))
    total_fare_amount = Column(Decimal(12,5))
    total_extra = Column(Decimal(12,5))
    total_mta_tax = Column(Decimal(12,5))
    total_tip_amount = Column(Decimal(12,5))
    total_ehail_fee = Column(Decimal(12,5))
    total_imprv_srchg = Column(Decimal(12,5))
    total_total_amount = Column(Decimal(12,5))
    total_payment_1 = Column(Integer(10))
    total_payment_2 = Column(Integer(10))
    total_payment_3 = Column(Integer(10))
    total_payment_4 = Column(Integer(10))
    total_payment_5 = Column(Integer(10))
    total_payment_6 = Column(Integer(10))
    total_trip_type_0 = Column(Integer(10))
    total_trip_type_1 = Column(Integer(10))
    total_trip_type_2 = Column(Integer(10))
    total_tolls_amount = Column(Integer(10))
    total_record_cnt = Column(Integer(10))

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


# Example:
# for d in data:
#     trip_stat = TripStats(datetime=val1, taxi_type=val2, rate_code=val3)
#     try:
#         trip_stat.save()
#     except:
    #     session.rollback()
    #     print "There was an exception"

class TripSpatialStats(BaseAttr, Base):
    __tablename__ = 'tripsSpatialStats'

    id = Column(Integer(), primary_key=True)
    datetime = Column(DateTime(), nullable=False, default=datetime.datetime.now)
    taxi_type = Column(Integer(6))
    rate_code = Column(Integer(6))
    action = Column(Integer(6)) # 0 pickup, 1 drop off
    total_record_cnt = Column(String(2048))

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


#class Polygons(BaseAttr, Base):


class TripPolygonStats(BaseAttr, Base):
    __tablename__ = 'tripsPolygonStats'

    id = Column(Integer(), primary_key=True)
    datetime = Column(DateTime(), nullable=False, default=datetime.datetime.now)
    taxi_type = Column(Integer(6))
    rate_code = Column(Integer(6))
    action = Column(Integer(6)) # 0 pickup, 1 drop off
    PolygonId = Column(Integer(6))
    Count = Column(Integer(10))

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)