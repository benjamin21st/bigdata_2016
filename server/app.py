import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
logging.basicConfig(filename='app_log.txt', level=logging.DEBUG,
                    format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    return 'OMG, it worked!'


if __name__ == '__main__':
    app.run(debug=True)
