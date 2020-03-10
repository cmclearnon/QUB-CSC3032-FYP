from . import FeatureEngineering
import numpy as np
import pandas as pd

import logging

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, f_classif, chi2
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, RobustScaler
from sklearn.model_selection import train_test_split

log = logging.getLogger()

class URLFeatureExtractor(TransformerMixin):
    """
    Custom transformer for extracting different feature sets from
    input data. Supports either: 
    - Lexical-based features
    - Host-based features
    """
    def __init__(self, feature_type="lexical"):
        self.feature_type = feature_type

    def transform(self, df):
        feature_list = []
        for idx, row in df.iterrows():
            row["URL"] = FeatureEngineering.clean_data(row["URL"])
            if self.feature_type is "lexical":
                feature_dict = FeatureEngineering.lexical_extract(row["URL"])
            elif self.feature_type is "host":
                feature_dict = FeatureEngineering.host_extract(row["URL"])
            if "URLType" in feature_dict:
                feature_dict.update({"URLType": row["URLType"]})
            # feature_dict.update({"URLType": row["URLType"]})
            feature_list.append(feature_dict)

        feature_df = pd.concat(feature_list)
        return feature_df

class FeatureImportanceSelector(TransformerMixin):
    def __init__(self, k_best, feature_type):
        self.k_best = k_best
        self.selector = SelectKBest(chi2, k=k_best)

    
    def transform(self, X, Y, columns: list):
        log.debug(f"Feature set before Chi^2 Analysis: {columns}")
        log.debug(f"\n\nFitting dataset to selector: {self.selector.get_params()}")
        x_fit = self.selector.fit(X, Y)
        log.debug(f"\n\nRelationship scores for feature set: {x_fit.scores_}")

        return x_fit.transform(X)

    def fit(self, *_):
        return self

class XYTransformer(TransformerMixin):
    def __init__(self, test_size, random_state):
        self.test_size = test_size
        self.random_state = random_state
        self.scaler = RobustScaler()

    # def transform(self, X, Y):
    def transform(self, X):
        transformed_x = pd.DataFrame(columns = None)
        for (column_name, column_data) in X.iteritems():
            transformed_x[column_name] = self.scaler.fit_transform(X[column_name].values.reshape(-1, 1))
        # enc = preprocessing.LabelEncoder()
        # Y = enc.fit_transform(Y)
        
        # return X, Y
        return transformed_x

    def fit(self, *_):
        return self

