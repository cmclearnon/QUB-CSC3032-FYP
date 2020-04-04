from flask_restful import Resource, fields, marshal_with, reqparse
from models.DomainFeatureSet import DomainFeatureSet
from req_param_parser import params_parser

dataset_fields = {
    'id': fields.Integer,
    'RegistryDate_year': fields.Integer,
    'RegistryDate_month': fields.Integer,
    'RegistryDate_day': fields.Integer,
    'ExpirationDate_year': fields.Integer,
    'ExpirationDate_month': fields.Integer,
    'ExpirationDate_day': fields.Integer,
    'HostCountry': fields.String,
    'DomainAge': fields.Integer,
    'URLType': fields.Integer
}

def paginated(queried_object_fields):
    return {
        'items': fields.Nested(queried_object_fields),
        'total': fields.Integer,
        'page': fields.Integer,
        'pages': fields.Integer,
        'per_page': fields.Integer
    }

class DatasetResource(Resource):
    @params_parser(
        reqparse.Argument('page', type=int, required=False, location='args', default=0),
        reqparse.Argument('size', type=int, required=False, location='args', default=10),
    )
    @marshal_with(paginated(dataset_fields))
    def get(self, page, size):
        result = DomainFeatureSet.query.paginate(page, size, False)
        print(result.page)
        return result