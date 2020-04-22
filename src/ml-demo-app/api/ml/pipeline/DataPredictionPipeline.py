from ml.featureprocessing.DataTransformers import DomainFeatureScaler, DateEncoder, CategoryEncoder, LexicalFeatureScaler
from ml.featureprocessing.FeatureEngineering import host_extract, lexical_extract
from ml.utils import Serialiser

import numpy as np
import pandas as pd

import logging

from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

from flask import current_app as app

log = logging.getLogger()
      

class DataPreprocessingEngine():
    def __init__(self, feature_type):
        self.feature_type = feature_type

    def get_model(self, model):
        if (self.feature_type ==  'domain'):
            if (model == 'SVC'):
                model = Serialiser.deserialize(SVC(), Serialiser.json_to_data("", app.config['DOMAIN_SVC_LOC']))
            elif (model == 'KNN'):
                model = Serialiser.deserialize(KNeighborsClassifier(), Serialiser.json_to_data("", app.config['DOMAIN_KNN_LOC']))
            else:
                return None
        elif (self.feature_type == 'lexical'):
            if (model == 'SVC'):
                model = Serialiser.deserialize(SVC(), Serialiser.json_to_data("", app.config['LEXICAL_SVC_LOC']))
            elif (model == 'KNN'):
                model = Serialiser.deserialize(KNeighborsClassifier(), Serialiser.json_to_data("", app.config['LEXICAL_KNN_LOC']))
            else:
                return None

        return model

    def get_estimators(self):
        date_enc = Serialiser.deserialize(DateEncoder(), Serialiser.json_to_data("", app.config['DATE_ENC_LOC']))
        cat_enc = Serialiser.deserialize(CategoryEncoder(), Serialiser.json_to_data("", app.config['CATEGORY_ENC_LOC']))
        scaler = DomainFeatureScaler(scaler_loc=app.config['SCALER_LOC'], has_fit=True)

        return date_enc, cat_enc, scaler

    def get_datasets(self):
        if (self.feature_type == 'domain'):
            x_train = pd.read_csv(app.config['DOMAIN_X_TRAIN_LOC'])
            y_train = pd.read_csv(app.config['DOMAIN_Y_TRAIN_LOC'], header=None)
            y_train = y_train[1]
        elif (self.feature_type == 'lexical'):
            x_train = pd.read_csv(app.config['LEXICAL_X_TRAIN_LOC'])
            y_train = pd.read_csv(app.config['LEXICAL_Y_TRAIN_LOC'], header=None)
            y_train = y_train[1]
        else:
            return None, None
        
        return x_train, y_train

    def get_transformers(self):
        if (self.feature_type == 'domain'):
            scaler = DomainFeatureScaler()
            encoder = CategoryEncoder(handle_unknown='ignore', columns=['HostCountry'])
            t =[('categorial_encoder', encoder, ['HostCountry']),]
            transformer = ColumnTransformer(t, remainder=scaler)
            return transformer
        elif (self.feature_type == 'lexical'):
            scaler = LexicalFeatureScaler()
            return scaler
        
        return None

    def extract_features(self, url: str):
        if (self.feature_type == 'domain'):
            url_features = host_extract(url)
        elif (self.feature_type == 'lexical'):
            url_features = lexical_extract(url)
        else:
            return None

        return url_features

    def predict_url(self, feature_vectors, model: str):
        classifier = self.get_model(model)

        if (classifier is None):
            return None, None

        class_prediction = classifier.predict(feature_vectors)
        prediction_probability = classifier.predict_proba(feature_vectors)

        return class_prediction, prediction_probability

    def process_url(self, url: str, model: str):
        x_train, y_train = self.get_datasets()
        transformers = self.get_transformers()
        pipeline = Pipeline(steps=[
            ('transformers', transformers)
        ])
        
        pipeline.fit(x_train, y_train)

        features = self.extract_features(url)

        if (self.feature_type == 'domain'):
            date_enc = Serialiser.deserialize(DateEncoder(), Serialiser.json_to_data("", app.config['DATE_ENC_LOC']))
            features = date_enc.transform(features)

            if (features.isnull().values.any()):
                fail_result = {
                    'url': url,
                    'prediction': np.nan,
                    'probability': [],
                    'original_features': {},
                    'processed_features': [],
                    'error': True,
                    'message': 'Cannot retrieve required data for URL'
                }
                return fail_result
            original_features = features.to_dict('records')
        elif (self.feature_type == 'lexical'):
            original_features = [features]
            features = pd.DataFrame(features, index=[0])

        feature_vectors = pipeline.transform(features)

        class_prediction, prediction_probabilities = self.predict_url(feature_vectors, model)
        if (class_prediction is None) & (prediction_probabilities is None):
            print('returning none model')
            fail_result = {
                'url': url,
                'prediction': np.nan,
                'probability': [],
                'original_features': {},
                'error': True,
                'message': f'{model} not found'
            }
            return fail_result

        success_result = {
            'url': url,
            'prediction': int(class_prediction[0]),
            'probability': prediction_probabilities.tolist(),
            'original_features': original_features,
            'error': False,
            'message': 'URL Classification successful'
        }

        print(success_result)

        return success_result

