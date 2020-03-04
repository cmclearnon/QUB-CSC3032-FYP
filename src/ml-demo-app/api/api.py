from flask import render_template, Blueprint, request, Response, jsonify, Flask
from joblib import load
import pandas as pd
import logging

from ml.featureprocessing.DataTransformers import URLFeatureExtractor

from sklearn.preprocessing import RobustScaler

log = logging.getLogger()

app = Flask(__name__)

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