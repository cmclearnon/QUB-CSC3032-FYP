from . import FeatureEngineering
import numpy as np
import pandas as pd

import logging

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, f_classif, chi2
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, RobustScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

from pickle import load

from ml.utils import Serialiser

log = logging.getLogger()

# class URLFeatureExtractor(TransformerMixin):
#     """
#     Custom transformer for extracting different feature sets from
#     input data. Supports either: 
#     - Lexical-based features
#     - Host-based features
#     """
#     def __init__(self, feature_type="lexical"):
#         self.feature_type = feature_type

#     def transform(self, df):
#         feature_list = []
#         for idx, row in df.iterrows():
#             row["URL"] = FeatureEngineering.clean_data(row["URL"])
#             if self.feature_type is "lexical":
#                 feature_dict = FeatureEngineering.lexical_extract(row["URL"])
#             elif self.feature_type is "host":
#                 feature_dict = FeatureEngineering.host_extract(row["URL"])
#             if "URLType" in feature_dict:
#                 feature_dict.update({"URLType": row["URLType"]})
#             # feature_dict.update({"URLType": row["URLType"]})
#             feature_list.append(feature_dict)

#         feature_df = pd.concat(feature_list)
#         return feature_df

# class FeatureImportanceSelector(TransformerMixin):
#     def __init__(self, k_best, feature_type):
#         self.k_best = k_best
#         self.selector = SelectKBest(chi2, k=k_best)

    
#     def transform(self, X, Y, columns: list):
#         log.debug(f"Feature set before Chi^2 Analysis: {columns}")
#         log.debug(f"\n\nFitting dataset to selector: {self.selector.get_params()}")
#         x_fit = self.selector.fit(X, Y)
#         log.debug(f"\n\nRelationship scores for feature set: {x_fit.scores_}")

#         return x_fit.transform(X)

#     def fit(self, *_):
#         return self


class DomainFeatureExtractor(TransformerMixin):
    def fit(self, *_):
        return self

    def transform(self, df):
        feature_list = []
        for idx, row in df.iterrows():
            row["URL"] = FeatureEngineering.clean_data(row["URL"])
            feature_df = FeatureEngineering.host_extract(row['URL'])
            feature_list.append(feature_df)

        feature_df = pd.concat(feature_list)
        return feature_df

class DateEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, col_names=[]):
        self.col_names = col_names

    def fit(self, *_):
        return self

    def transform(self, X):
        df_list = []
        for column in self.col_names:
            dt = X[column].dt
            year_series = dt.year
            month_series = dt.month
            day_series = dt.day

            frame = {
                f'{column}_year': year_series,
                f'{column}_month': month_series,
                f'{column}_day': day_series
            }
            dt_df = pd.DataFrame.from_dict(frame)
            if ((dt_df.isnull().values.all()) == False):
                dt_df = dt_df.astype(np.int64)
            df_list.append(dt_df)

        df_list.append(X)
        dfs = pd.concat(df_list, axis=1)
        dfs = dfs.drop(self.col_names, axis=1)
        return dfs

class MissingValueImputer(TransformerMixin):
    def __init__(self, strategy, missing_values):
        self.missing_values = missing_values
        self.strategy = strategy
        self.imputer = SimpleImputer

    def fit(self, X, *_):
        self.imputer = self.imputer(missing_values=self.missing_values, strategy=self.strategy)
        self.imputer.fit(X)
        return self

    def transform(self, X, *_):
        transformed = self.imputer.transform(X)
        return transformed
class CategoryEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, handle_unknown='ignore', columns=[], has_fit=False, encoder=OneHotEncoder):
        self.handle_unknown = handle_unknown
        self.columns = columns
        self.encoder = encoder
        self.categories = []
        self.has_fit = has_fit

    def fit(self, X, *_):
        if self.has_fit:
            self.encoder = self.encoder(handle_unknown=self.handle_unknown, categories=categories)
            self.encoder.fit(X)
            return self
        else:
            self.encoder = self.encoder(handle_unknown='ignore')
            self.encoder.fit(X)
            self.categories = self.encoder.categories_
            self.has_fit = True
            return self

    def transform(self, X, *_):
        self.encoder = OneHotEncoder
        self.encoder = self.encoder(handle_unknown=self.handle_unknown, categories=self.categories)
        df = pd.DataFrame(X[self.columns[0]])
        self.encoder.fit(df)
        encoded = self.encoder.transform(np.array(X[self.columns[0]]).reshape(-1, 1))
        return encoded

class DomainFeatureScaler(BaseEstimator, TransformerMixin):
    def __init__(self, scaler=MinMaxScaler, has_fit=False, scaler_loc=""):
        self.scaler = scaler
        self.has_fit = has_fit
        self.scaler_loc = scaler_loc

    def fit(self, X, *_):
        if self.has_fit:
            self.scaler = deserialize(json_to_data(MinMaxScaler(), json_to_data("", self.scaler_loc)))
        else:
            self.scaler = self.scaler()
            self.scaler.fit(X)
            self.has_fit=True
        return self

    def transform(self, X, *_):
        scaled = self.scaler.transform(X)
        return scaled


class LexicalFeatureScaler(BaseEstimator, TransformerMixin):
    def __init__(self, scaler=MinMaxScaler):
        self.scaler = scaler

    def fit(self, X, *_):
        self.scaler = self.scaler()
        self.scaler.fit(X)
        return self

    def transform(self, X, *_):
        scaled = self.scaler.transform(X)
        return scaled