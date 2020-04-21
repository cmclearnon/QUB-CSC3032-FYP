from flask_restful import Resource, fields, marshal_with, reqparse
from req_param_parser import params_parser
from flask import current_app as app

class HealthCheckResource(Resource):

    def get(self):
        return {
            'message': 'API Server running',
        }, 200
