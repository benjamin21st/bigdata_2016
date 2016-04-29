import local_config

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@localhost:3306/trip_fare' % (local_config.MYSQL_USERNAME, local_config.MYSQL_PASSWORD)
SQLALCHEMY_TRACK_MODIFICATIONS = False
