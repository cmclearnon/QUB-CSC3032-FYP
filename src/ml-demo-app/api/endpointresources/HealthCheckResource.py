from flask_restful import Resource, fields, marshal_with, reqparse
from req_param_parser import params_parser
from flask import current_app as app

'''
Root API Endpoint for checking health of API service
'''
class HealthCheckResource(Resource):
    """ 
    GET Resource endpoint for retrieving paginated data from domain_full_featureset table

    Args:

    Returns:
        (dict): 200 success OK response code
                'message': Simple message to verify API server is running

    """
    def get(self):
        return {
            'message': 'API Server running',
        }, 200
