from flask import render_template, Blueprint, request, Response, jsonify, Flask
import logging
log = logging.getLogger()

from flask_cors import CORS
from flask_restful import Api
import os

from setup import setup_db
from db import db
from endpointresources.HealthCheckResource import HealthCheckResource
from endpointresources.DatasetResource import DomainDatasetResource, LexicalDatasetResource
from endpointresources.ModelAccuracyResource import ModelAccuracyResource
from endpointresources.SinglePredictionResource import SinglePredictionResource

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db/datasets.db')
app.config.from_pyfile('config.cfg')

db.init_app(app)
db.app = app

with app.app_context():
    setup_db('domain')
    setup_db('lexical')

api = Api(app)
api.add_resource(HealthCheckResource, '/')
api.add_resource(DomainDatasetResource, '/datasets/domain')
api.add_resource(LexicalDatasetResource, '/datasets/lexical')
api.add_resource(ModelAccuracyResource, '/model_accuracy')
api.add_resource(SinglePredictionResource, '/single_prediction')

