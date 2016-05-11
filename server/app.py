import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS


app = Flask(__name__)
app.config.from_pyfile('config.py')
cors = CORS(app)  # https://flask-cors.readthedocs.org/en/latest/
db = SQLAlchemy(app)
logging.basicConfig(filename='app_log.txt', level=logging.DEBUG,
                    format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)
