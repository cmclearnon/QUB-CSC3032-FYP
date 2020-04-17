from flask import render_template, Blueprint, request, Response, jsonify, Flask
import logging
log = logging.getLogger()

from flask_cors import CORS
from flask_restful import Api
import os

from setup import setup_db
from db import db
from endpointresources.DatasetResource import DatasetResource
from endpointresources.ModelAccuracyResource import ModelAccuracyResource
from endpointresources.SinglePredictionResource import SinglePredictionResource

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db/datasets.db')
app.config.from_pyfile('config.cfg')

db.init_app(app)
db.app = app
setup_db()

api = Api(app)
api.add_resource(DatasetResource, '/datasets')
api.add_resource(ModelAccuracyResource, '/model_accuracy')
api.add_resource(SinglePredictionResource, '/single_prediction')

