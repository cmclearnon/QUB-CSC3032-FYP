from flask_restful import Resource, fields, marshal_with, reqparse
from req_param_parser import params_parser
from sklearn.svm import SVC

from ml.utils import Serialiser
from ml.utils import Metrics
import scipy.sparse
import pandas as pd

model_params_loc='/Users/chrismclearnon/Developer/QUB-CSC3032-FYP/src/ml-demo-app/api/ml/models/bayesian_svc_model.json'


class ModelAccuracyResource(Resource):
    @params_parser(
        reqparse.Argument('model', type=str, required=False, location='args', default='svc'),
    )

    def get(self, model):
        model = Serialiser.deserialize(SVC(), Serialiser.json_to_data("", model_params_loc))
        x_test = scipy.sparse.load_npz('/Users/chrismclearnon/Developer/QUB-CSC3032-FYP/src/data/x_test.npz')
        y_test = pd.read_csv('/Users/chrismclearnon/Developer/QUB-CSC3032-FYP/src/data/y_test.csv', header=None)
        # print(x_test.shape)
        y_pred=model.predict(x_test)
        y_test = y_test[1]
        # print(y_test.shape)
        # print(y_pred.shape)
        tpr = Metrics.tpr(y_test, y_pred)
        fnr = Metrics.fnr(y_test, y_pred)
        acc = Metrics.accuracy(y_test, y_pred)
        result = {
            'tpr': tpr,
            'fnr': fnr,
            'accuracy': acc
        }
        return result
