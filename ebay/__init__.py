import socket

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
hostname = socket.gethostname()
with open("ebay/config.txt") as f1:
    configuser = f1.readline().rstrip()
    configpass = f1.readline().rstrip()
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://%s:%s@localhost/ebay" % (configuser, configpass)

db = SQLAlchemy(app)

__all__ = ['views', 'models']

# Logging to external file
app.debug = True
import logging
from logging import Formatter
from logging import FileHandler
from logging.handlers import RotatingFileHandler
log = "/var/log/lighttpd/restapi.log"
file_handler_1 = RotatingFileHandler(log, maxBytes=2*1024*1024, backupCount=5)
file_handler = FileHandler(log)
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)


# Import all views from here
from ebay.views import items

# Load all blueprints
app.register_blueprint(items.mod)

