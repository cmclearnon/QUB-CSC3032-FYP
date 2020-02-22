from ml.featureprocessing.DataTransformers import URLFeatureExtractor, FeatureImportanceSelector, XYTransformer

import numpy as np
import pandas as pd

import logging

from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV

from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer

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
      

class DatasetPreprocessingPipeline():
    def __init__(self, path_to_dataset, feature_type):
        self.path_to_dataset = path_to_dataset
        self.feature_type = feature_type

    def run_pipeline(self):
        pipeline = Pipeline([
            ('ftextract', URLFeatureExtractor()),
            ('ftanalysis', FeatureImportanceSelector(k_best=5, feature_type=self.feature_type)),
            ('xytransform', XYTransformer(test_size=0.2, random_state=42)),
            # ('clf', SVC()),
        ])

        df = pd.read_csv(self.path_to_dataset)
        df_new = pipeline['ftextract'].transform(df)

        df_values = df_new.values
        n_columns = df_new.shape[1]
        columns = list(df_new.columns)
        x = df_values[:, 0:n_columns-1]
        y = df_values[:, n_columns-1]
        x_analysed = pipeline['ftanalysis'].transform(x, y, columns)
        x_scaled = pipeline['xytransform'].transform(x_analysed)

        print(f"Original dataset:\n{df.head}\n\nDataset with features:\n{df_new[:10]}\n\nChosen features:\n{x_analysed[:10]}\n\nScaled dataset:\n{x_scaled[:10]}")