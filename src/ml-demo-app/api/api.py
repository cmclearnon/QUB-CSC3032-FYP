from flask import render_template, Blueprint, request, Response, jsonify, Flask
from joblib import load
import pandas as pd
import logging

from ml.featureprocessing.DataTransformers import URLFeatureExtractor, DomainFeatureExtractor, DateEncoder, DomainFeatureScaler

from sklearn.preprocessing import RobustScaler

log = logging.getLogger()

from flask_cors import CORS
from flask_restful import Api
import os

from setup import setup_db
from db import db
from endpointresources.DatasetResource import DatasetResource

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db/datasets.db')

db.init_app(app)
db.app = app
setup_db()

api = Api(app)
api.add_resource(DatasetResource, '/datasets')


@app.route('/predict')
def get_current_time():
    clf = load('../../ml/models/best_bayes_estim.joblib')
    url_to_predict = request.args.get('url', type = str)
    d = {'URL': [url_to_predict]}
    pred_df = pd.DataFrame(data=d)

    ft_extractor = URLFeatureExtractor()
    pred_df_ft = ft_extractor.transform(pred_df)

    df_values = pred_df_ft.values
    n_columns = pred_df_ft.shape[1]
    columns = list(pred_df_ft.columns)
    x = df_values[:, 0:n_columns]

    scaler = RobustScaler()

    transformed_x = pd.DataFrame(columns = None)
    # for (column_name, column_data) in pred_df_ft.iteritems():
    #     log.error(f'Values: {pred_df_ft[column_name]}')
    #     transformed_x[column_name] = scaler.fit_transform(pred_df_ft[column_name].values.reshape(-1, 1))
    log.error(f'X: {x}')
    pred_proba = clf.predict_proba(x)
    log.error(f'Predict_proba: {pred_proba}')
    return_d = {
        'predict_proba': pred_proba.tolist(),
    }
    # return json.dumps({'predict_proba': pred_proba[0][1]})
    return jsonify(return_d)

@app.route('/domain_predict')
def domain_prediction():
    url = request.args.get('url', type=str)
    d = {'URL': [url]}
    df = pd.DataFrame(data=d)

    extractor = DomainFeatureExtractor()
    base_df = extractor.transform(df)
    date_encoder = DateEncoder()
    dates_to_encode = base_df[['RegistryDate', 'ExpirationDate']]
    encoded_dates_df = date_encoder.transform(dates_to_encode)
    log.error(f'Encoded Dates: {encoded_dates_df}')

    base_df = base_df.drop(['RegistryDate', 'ExpirationDate'], axis=1)
    log.error(f'BEFORE SCALING: {base_df}')
    df_to_scale = pd.concat([base_df, encoded_dates_df])

    scaler = DomainFeatureScaler()
    scaled_df = scaler.transform(df_to_scale)
    log.error(f'X: {scaled_df}')

    return jsonify({'OK'})

