from ml.featureprocessing.DataTransformers import DomainFeatureScaler, DateEncoder, CategoryEncoder
from ml.featureprocessing.FeatureEngineering import host_extract
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

# from skopt import BayesSearchCV
# from skopt.space import Real, Categorical, Integer

from flask import current_app as app

log = logging.getLogger()

# class BayesianHyperparamModelSelector():

#     def __init__(self, n_iter: int, cv: int, estimator: str):
#         self.n_iter = n_iter
#         self.cv = cv
#         self.estimator = estimator

#     def build_bayesian_search(self):
#         estimator_search = {} 
#         if self.estimator == 'SVC':
#             pipe = Pipeline([
#                 ('model', SVC())
#             ])
#             estimator_search = {
#                 'model': Categorical([SVC()]),
#                 'model__C': Real(0.01, 100.0, 'log-uniform'),
#                 'model__kernel': Categorical(['poly', 'rbf']),
#             }

#             searchcv = BayesSearchCV(
#                 pipe,
#                 search_spaces = estimator_search,
#                 n_iter=self.n_iter,
#                 cv=self.cv,
#                 verbose=5,
#                 n_jobs=-1
#             )

#         return searchcv

#     def run_search(self, X_train, Y_train, search_cv):
#         log.debug(f"Beginning Bayesian Search CV for {self.estimator} - Num of iterations: {search_cv.total_iterations}")
#         search_cv.fit(X_train, Y_train)
#         log.debug(f'Best Estimator found: {search_cv.best_estimator_}')

#         dump(search_cv.best_estimator_, 'ml/models/best_estim.joblib')
      

class DataPreprocessingEngine():
    def __init__(self, feature_type):
        self.feature_type = feature_type

    def get_model(self, model):
        if (model == 'BaseSVC'):
            model = Serialiser.deserialize(SVC(), Serialiser.json_to_data("", app.config['BASE_SVC_LOC']))
        elif (model == 'OptimisedSVC'):
            model = Serialiser.deserialize(SVC(), Serialiser.json_to_data("", app.config['BAYESIAN_SVC_LOC']))
        elif (model == 'BaseKNN'):
            model = Serialiser.deserialize(KNeighborsClassifier(), Serialiser.json_to_data("", app.config['BASE_KNN_LOC']))
        elif (model == 'OptimisedKNN'):
            model = Serialiser.deserialize(KNeighborsClassifier(), Serialiser.json_to_data("", app.config['BAYESIAN_KNN_LOC']))
        
        return model

    def get_estimators(self):
        date_enc = Serialiser.deserialize(DateEncoder(), Serialiser.json_to_data("", app.config['DATE_ENC_LOC']))
        cat_enc = Serialiser.deserialize(CategoryEncoder(), Serialiser.json_to_data("", app.config['CATEGORY_ENC_LOC']))
        scaler = DomainFeatureScaler(scaler_loc=app.config['SCALER_LOC'], has_fit=True)

        return date_enc, cat_enc, scaler

    def extract_features(self, url: str):
        url_features = host_extract(url)

        return url_features

    def predict_url(self, feature_vectors, model: str):
        classifier = self.get_model(model)
        class_prediction = classifier.predict(feature_vectors)
        prediction_probability = classifier.predict_proba(feature_vectors)

        return class_prediction, prediction_probability

    def process_url(self, url: str, model: str):
        date_enc, cat_enc, scaler = self.get_estimators()

        x_train = pd.read_csv(app.config['X_TRAIN_LOC'])
        y_train = pd.read_csv(app.config['Y_TRAIN_LOC'], header=None)
        y_train = y_train[1]

        scaler = DomainFeatureScaler()
        encoder = CategoryEncoder(handle_unknown='ignore', columns=['HostCountry'])
        t =[('categorial_encoder', encoder, ['HostCountry']),]
        transformer = ColumnTransformer(t, remainder=scaler)

        pipeline = Pipeline(steps=[
            ('full_column_transformer', transformer)
        ])
        pipeline.fit(x_train, y_train)

        features = self.extract_features(url)
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
            print(fail_result)
            return fail_result


        original_features = features.to_dict('records')

        feature_vectors = pipeline.transform(features)
        processed_features = (feature_vectors.toarray()).tolist()

        class_prediction, prediction_probabilities = self.predict_url(feature_vectors, odel)

        success_result = {
            'url': url,
            'prediction': int(class_prediction[0]),
            'probability': prediction_probabilities.tolist(),
            'original_features': original_features,
            'processed_features': processed_features[0],
            'error': False,
            'message': 'URL Classification successful'
        }

        print(success_result)

        return success_result

