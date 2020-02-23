# from ml.featureprocessing import DomainFeatureProcessing as df
# from ml.featureprocessing import LexicalFeatureProcessing as lf
# from urllib.parse import urlparse
# from ml.datacleaning import URLDataCleaning

from ml.pipeline.BaseModelPipeline import DatasetPreprocessingPipeline
from ml.DatasetFetcher import DatasetFetcher
# dataset = lf.extract('http://abcnews.go.com/US/wireStory/regulators-delays-georgia-nuclear-plant-31020059')
# print(dataset)
# print(df.extract('http://abcnews.go.com/'))
# pipeline_obj = DatasetPreprocessingPipeline('/Users/chrismclearnon/Developer/QUB-CSC3032-FYP/src/data/dataset.csv', 'lexical')
# pipeline_obj.run_pipeline()

# fetch = DatasetFetcher(source='url', file_path='https://www.researchgate.net/profile/Christian_Urcuqui_Lopez/publication/322087462_Malicious_and_benign_websites/data/5ad18285458515c60f4fe743/dataset.csv')
# fetch.fetch_file_local('https://www.researchgate.net/profile/Christian_Urcuqui_Lopez/publication/322087462_Malicious_and_benign_websites/data/5ad18285458515c60f4fe743/dataset.csv','new_data')
from ml.pipeline.BaseModelPipeline import BayesianHyperparamModelSelector

import pandas as pd
import numpy as np

from sklearn import preprocessing
from sklearn.preprocessing import RobustScaler
import feather
from sklearn.model_selection import train_test_split

df_ft = feather.read_dataframe('/Users/chrismclearnon/Developer/QUB-CSC3032-FYP/src/data/tmp/df_ft.feather')

correlations = df_ft.corr()
correlations = correlations['URLType']
print(correlations)

robust = RobustScaler()

x = df_ft.drop('URLType', axis=1)
y = df_ft["URLType"]

X_train, x_test, Y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)

for (column_name, column_data) in X_train.iteritems():
    X_train[column_name] = robust.fit_transform(X_train[column_name].values.reshape(-1, 1))

for (column_name, column_data) in x_test.iteritems():
    x_test[column_name] = robust.fit_transform(x_test[column_name].values.reshape(-1, 1))

searchcv = BayesianHyperparamModelSelector(10, 3, 'SVC')
search_cv = searchcv.build_bayesian_search()
searchcv.run_search(X_train, Y_train, search_cv)

from flask import flask


