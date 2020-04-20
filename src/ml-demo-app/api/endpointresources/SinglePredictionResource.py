from flask_restful import Resource, fields, marshal_with, reqparse
from req_param_parser import params_parser
from sklearn.svm import SVC
from sklearn.compose import ColumnTransformer

from flask import current_app as app

from ml.utils import Serialiser
from ml.utils import Metrics
from ml.featureprocessing.DataTransformers import DomainFeatureScaler, DateEncoder, CategoryEncoder
from ml.featureprocessing.FeatureEngineering import host_extract
from ml.pipeline.BaseModelPipeline import DataPreprocessingEngine

import scipy.sparse
import pandas as pd
import numpy as np

class SinglePredictionResource(Resource):
    @params_parser(
        reqparse.Argument('url', type=str, required=False, location='args', default=''),
        reqparse.Argument('model', type=str, required=False, location='args', default='BaseSVC'),
        reqparse.Argument('featureType', type=str, required=False, location='args', default='host'),
    )

    def get(self, url, model, featureType):
        engine = DataPreprocessingEngine(feature_type=featureType)
        result = engine.process_single_datapoint(url, model)

        if (result.get('errors')):
            return result, 422

        return result, 200

