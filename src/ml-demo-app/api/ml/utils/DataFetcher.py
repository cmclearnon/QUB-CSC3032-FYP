import pandas as pd
import numpy as np
import scipy.sparse

class DataFetcher():
    def fetch_csv():
        try:
            data = pd.read_csv(self.csv)
            return data
        except FileNotFoundError:
            return 'File does not exist'
        except TypeError:
            return 'File cannot be converted into Pandas DataFrame'

    def fetch_train_data():
        try:
            X_train= scipy.sparse.load_npz('/Users/chrismclearnon/Developer/QUB-CSC3032-FYP/src/data/x_train.npz')
            Y_train = pd.read_csv('/Users/chrismclearnon/Developer/QUB-CSC3032-FYP/src/data/y_train.csv')
            return X_train, Y_train
        except FileNotFoundError:
            raise 'File Not Found error'

    def fetch_test_data():
        try:
            X_test= scipy.sparse.load_npz('/Users/chrismclearnon/Developer/QUB-CSC3032-FYP/src/data/x_test.npz')
            Y_test = pd.read_csv('/Users/chrismclearnon/Developer/QUB-CSC3032-FYP/src/data/y_test.csv')
            return X_test, Y_test
        except FileNotFoundError:
            raise 'File Not Found error'