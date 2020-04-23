from flask_restful import Resource, fields, marshal_with, reqparse
from models.FeatureSets import DomainFeatureSet, LexicalFeatureSet
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

lexical_fields = {
    'id': fields.Integer,
    'URLLength': fields.Integer,
    'HostLength': fields.Integer,
    'TLDLength': fields.Integer,
    'DotCount': fields.Integer,
    'DashCount': fields.Integer,
    'AtSymbolCount': fields.Integer,
    'PercentSymbolCount': fields.Integer,
    'EqualsSymbolCount': fields.Integer,
    'QuestionMarkCount': fields.Integer,
    'DigitCount': fields.Integer,
    'UniqueCharCount': fields.Integer,
    'URLType': fields.Integer
}

'''
Function to return dictionary of paginated request results

Args:
    queried_object_fields (dict): The columns/fields of the table being queried

Returns:
    (dict): Key-value pair dictionary of table pagination query results
            'items': Rows returned from table query
            'total': Total number of rows in table
            'page': Current page of table pagination
            'pages': Total number of pages in pagination result
            'per_page': Number of rows in each page to be returned
'''
def paginated(queried_object_fields):
    return {
        'items': fields.Nested(queried_object_fields),
        'total': fields.Integer,
        'page': fields.Integer,
        'pages': fields.Integer,
        'per_page': fields.Integer
    }

'''
API Resource for retrieval of domain_full_featureset data from SQLite database.db
'''
class DomainDatasetResource(Resource):
    @params_parser(
        reqparse.Argument('page', type=int, required=False, location='args', default=0),
        reqparse.Argument('size', type=int, required=False, location='args', default=10),
    )

    @marshal_with(paginated(dataset_fields))
    def get(self, page, size):
        """ 
        GET Resource endpoint for retrieving paginated data from domain_full_featureset table

        Args:
            page (int): Requested page of paginated domain_full_featureset table data
            size (int): Length of the table data to be returned

        Returns:
            result (dict): Returned dictionary from paginated function
                           Values populated with domain_full_featureset table paginate query results

        """
        result = DomainFeatureSet.query.paginate(page, size, False)
        print(result.page)
        return result

'''
API Resource for retrieval of lexical_full_featureset data from SQLite database.db
'''
class LexicalDatasetResource(Resource):
    @params_parser(
        reqparse.Argument('page', type=int, required=False, location='args', default=0),
        reqparse.Argument('size', type=int, required=False, location='args', default=10),
    )

    @marshal_with(paginated(lexical_fields))
    def get(self, page, size):
        """ 
        GET Resource endpoint for retrieving paginated data from lexical_full_featureset table

        Args:
            page (int): Requested page of paginated lexical_full_featureset table data
            size (int): Length of the table data to be returned

        Returns:
            result (dict): Returned dictionary from paginated function
                           Values populated with lexical_full_featureset table paginate query results

        """
        result = LexicalFeatureSet.query.paginate(page, size, False)
        print(result.page)
        return result