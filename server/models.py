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


