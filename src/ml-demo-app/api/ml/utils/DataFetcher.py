import pandas as pd
import numpy as np

class DataFetcher():
    def __init__(self, csv:str):
        self.csv = csv

    def fetch_csv():
        try:
            data = pd.read_csv(self.csv)
            return data
        except FileNotFoundError:
            return 'File does not exist'
        except TypeError:
            return 'File cannot be converted into Pandas DataFrame'
        