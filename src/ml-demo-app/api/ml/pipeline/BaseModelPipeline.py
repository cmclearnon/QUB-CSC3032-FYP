# from ml.featureprocessing.DataTransformers import URLFeatureExtractor, FeatureImportanceSelector, XYTransformer
from ml.featureprocessing.DataTransformers import DomainFeatureScaler, DateEncoder, CategoryEncoder
from ml.featureprocessing.FeatureEngineering import host_extract

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

from ml.utils import Serialiser, Metrics

from flask import current_app as app

from joblib import dump, load

log = logging.getLogger()

class BayesianHyperparamModelSelector():

    def __init__(self, n_iter: int, cv: int, estimator: str):
        self.n_iter = n_iter
        self.cv = cv
        self.estimator = estimator

    def build_bayesian_search(self):
        estimator_search = {} 
        if self.estimator == 'SVC':
            pipe = Pipeline([
                ('model', SVC())
            ])
            estimator_search = {
                'model': Categorical([SVC()]),
                'model__C': Real(0.01, 100.0, 'log-uniform'),
                'model__kernel': Categorical(['poly', 'rbf']),
            }

            searchcv = BayesSearchCV(
                pipe,
                search_spaces = estimator_search,
                n_iter=self.n_iter,
                cv=self.cv,
                verbose=5,
                n_jobs=-1
            )

        return searchcv

    def run_search(self, X_train, Y_train, search_cv):
        log.debug(f"Beginning Bayesian Search CV for {self.estimator} - Num of iterations: {search_cv.total_iterations}")
        search_cv.fit(X_train, Y_train)
        log.debug(f'Best Estimator found: {search_cv.best_estimator_}')

        dump(search_cv.best_estimator_, 'ml/models/best_estim.joblib')
      

class DataPreprocessingEngine():
    def __init__(self, feature_type):
        self.feature_type = feature_type

    def get_estimators(self):
        model = Serialiser.deserialize(SVC(), Serialiser.json_to_data("", app.config['MODEL_PARAMS_LOC']))
        date_enc = Serialiser.deserialize(DateEncoder(), Serialiser.json_to_data("", app.config['DATE_ENC_LOC']))
        cat_enc = Serialiser.deserialize(CategoryEncoder(), Serialiser.json_to_data("", app.config['CATEGORY_ENC_LOC']))
        scaler = DomainFeatureScaler(scaler_loc=app.config['SCALER_LOC'], has_fit=True)

        return model, date_enc, cat_enc, scaler

    def process_full_dataset():
        return

    def process_single_datapoint(self, url: str):
        model, date_enc, cat_enc, scaler = self.get_estimators()

        x_train = pd.read_csv(app.config['X_TRAIN_LOC'])
        y_train = pd.read_csv(app.config['Y_TRAIN_LOC'], header=None)
        y_train = y_train[1]

        encoder = CategoryEncoder(handle_unknown='ignore', columns=['HostCountry'])
        t =[('categorial_encoder', encoder, ['HostCountry']),]
        scaler = DomainFeatureScaler()
        transformer = ColumnTransformer(t, remainder=scaler)

        pipeline = Pipeline(steps=[
            ('full_column_transformer', transformer)
        ])

        pipeline.fit(x_train, y_train)

        features = host_extract(url)
        features = date_enc.transform(features)

        if (features.isnull().values.any()):
            result = {
                'url': url,
                'prediction': np.nan,
                'probability': [],
                'original_features': {},
                'processed_features': [],
                'error': True,
                'message': 'Cannot retrieve required data for URL'
            }

            return result

        original_features = features.to_dict('records')

        feature_vectors = pipeline.transform(features)
        processed_features = (feature_vectors.toarray()).tolist()

        prediction = model.predict(feature_vectors)
        prediction_probability = model.predict_proba(feature_vectors)

        result = {
            'url': url,
            'prediction': int(prediction[0]),
            'probability': prediction_probability.tolist(),
            'original_features': original_features,
            'processed_features': processed_features[0]
        }

        return result

