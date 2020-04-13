from flask_restful import Resource, fields, marshal_with, reqparse
from req_param_parser import params_parser
from sklearn.svm import SVC
from sklearn.compose import ColumnTransformer

from flask import current_app as app

from ml.utils import Serialiser
from ml.utils import Metrics
from ml.featureprocessing.DataTransformers import DomainFeatureScaler, DateEncoder, CategoryEncoder
from ml.featureprocessing.FeatureEngineering import host_extract

import scipy.sparse
import pandas as pd
import numpy as np

class SinglePredictionResource(Resource):
    @params_parser(
        reqparse.Argument('url', type=str, required=False, location='args', default=''),
        reqparse.Argument('model', type=str, required=False, location='args', default='svc'),
        reqparse.Argument('featureType', type=str, required=False, location='args', default='host'),
    )

    def get(self, url, model, featureType):
        model = Serialiser.deserialize(SVC(), Serialiser.json_to_data("", app.config['MODEL_PARAMS_LOC']))
        date_enc = Serialiser.deserialize(DateEncoder(), Serialiser.json_to_data("", app.config['DATE_ENC_LOC']))
        cat_enc = Serialiser.deserialize(CategoryEncoder(), Serialiser.json_to_data("", app.config['CATEGORY_ENC_LOC']))
        scaler = DomainFeatureScaler(scaler_loc=app.config['SCALER_LOC'], has_fit=True)

        x_train = pd.read_csv(app.config['X_TRAIN_LOC'])
        y_train = pd.read_csv(app.config['Y_TRAIN_LOC'], header=None)
        y_train = y_train[1]

        encoder = CategoryEncoder(handle_unknown='ignore', columns=['HostCountry'])
        t =[('categorial_encoder', encoder, ['HostCountry']),]
        scaler = DomainFeatureScaler()
        transformer = ColumnTransformer(t, remainder=scaler)
        transformer.fit(x_train, y_train)

        features = host_extract(url)
        features = date_enc.transform(features)

        features.RegistryDate_year = features.RegistryDate_year.astype(np.int64)
        features.RegistryDate_month = features.RegistryDate_month.astype(np.int64)
        features.RegistryDate_day = features.RegistryDate_day.astype(np.int64)

        features.ExpirationDate_year = features.ExpirationDate_year.astype(np.int64)
        features.ExpirationDate_month = features.ExpirationDate_month.astype(np.int64)
        features.ExpirationDate_day = features.ExpirationDate_day.astype(np.int64)
        print(f'Features: {features}')
        feature_vectors = transformer.transform(features)

        prediction = model.predict(feature_vectors)
        prediction_probability = model.predict_proba(feature_vectors)

        result = {
            'url': url,
            'prediction': int(prediction[0]),
            'probability': prediction_probability.tolist()
        }

        return result

