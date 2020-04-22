from flask_restful import Resource, fields, marshal_with, reqparse
from req_param_parser import params_parser
from sklearn.svm import SVC

from ml.pipeline.DataPredictionPipeline import DataPreprocessingEngine

from ml.utils import Serialiser
from ml.utils import Metrics
import scipy.sparse
import pandas as pd

model_params_loc='/Users/chrismclearnon/Developer/QUB-CSC3032-FYP/src/ml-demo-app/api/ml/models/bayesian_svc_model.json'

'''
API Resource for retrieval of specified model performance metrics from testing
'''
class ModelAccuracyResource(Resource):
    @params_parser(
        reqparse.Argument('model', type=str, required=False, location='args', default='SVC'),
        reqparse.Argument('featureType', type=str, required=False, location='args', default='domain'),
    )

    def get(self, model, featureType):
        """ 
        GET Resource endpoint for model performance metrics retrieval
        Args:
            model (str): Model requested
            featureType (str): The feature type of the requested model

        Returns:
            result (dict): Returned dictionary of performance metrics
                           'tpr': True Positive Rate of model classification
                           'fnr': False Negative Rate of model classification
                           'accuravy': Overall Accuracy Score of model classification
                           'auc_score': Area under Curve score of model
                           'error': Error flag
                           'message': 

        """
        engine = DataPreprocessingEngine(feature_type=featureType)
        classifier = engine.get_model(model)

        if (classifier is None):
            failed_result = {
                'tpr': 0,
                'fnr': 0,
                'accuracy': 0,
                'auc_score': 0,
                'error': True,
                'message': f'{model} not found'
            }

            return failed_result, 422

        x_test, y_test = engine.get_test_datasets()
        y_pred=classifier.predict(x_test)
        
        tpr = Metrics.tpr(y_test, y_pred)
        fnr = Metrics.fnr(y_test, y_pred)
        acc = Metrics.accuracy(y_test, y_pred)

        if (model != 'KNN'):
            y_score = classifier.decision_function(x_test)
            auc_score = Metrics.auc_score(y_test, y_score)
        else:
            auc_score = 0

        result = {
            'tpr': tpr,
            'fnr': fnr,
            'accuracy': acc,
            'auc_score': auc_score,
            'error': False,
            'message': f'{model} performance metrics retrieved'
        }
        return result, 200
