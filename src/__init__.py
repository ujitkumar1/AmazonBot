from flask import Flask
from flask_restful import Api

from log import log

log.info("Initializing the Flask App")
app = Flask(__name__)

log.info("Initializing the Flask API App")
api = Api(app)
