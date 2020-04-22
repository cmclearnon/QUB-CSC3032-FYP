from flask_restful import Resource, fields, marshal_with, reqparse
from req_param_parser import params_parser
from sklearn.svm import SVC
from sklearn.compose import ColumnTransformer

from flask import current_app as app

from ml.utils import Serialiser
from ml.utils import Metrics
from ml.featureprocessing.DataTransformers import DomainFeatureScaler, DateEncoder, CategoryEncoder
from ml.featureprocessing.FeatureEngineering import host_extract
from ml.pipeline.DataPredictionPipeline import DataPreprocessingEngine

import scipy.sparse
import pandas as pd
import numpy as np

'''
API Resource for requesting prediction of a submitted URL
'''
class SinglePredictionResource(Resource):
    @params_parser(
        reqparse.Argument('url', type=str, required=False, location='args', default=''),
        reqparse.Argument('model', type=str, required=False, location='args', default='SVC'),
        reqparse.Argument('featureType', type=str, required=False, location='args', default='domain'),
    )

    def get(self, url, model, featureType):
        """ 
        GET Resource endpoint for model classification of submitted URL
        Args:
            url (str): URL to be classified
            model (str): Model requested
            featureType (str): The feature type of the requested model

        Returns:
            result (dict): Returned dictionary of URL prediction information from DataPreprocessingEngine
                           'url': URL that was submitted in request,
                           'prediction': The classification value of the prediction outcome (0 = Benign, 1 = Malicious),
                           'probability': Array containing the model's probabilities of predicting URL as each class,
                           'original_features': Dictionary of the features extracted from the URL,
                           'error': Error flag,
                           'message': Message for 

        """
        engine = DataPreprocessingEngine(feature_type=featureType)
        result = engine.process_url(url, model)

        if (result.get('error')):
            return result, 422

        return result, 200

