# TODO: fix this circular import
import json
from app import app
from models import *

@app.route('/')
def index():
    return 'OMG, it worked!'

@app.route('/trips/count')
def count_trips():
    return json.dumps({'count': Trip.query.count()})


if __name__ == '__main__':
    app.run(debug=True)
