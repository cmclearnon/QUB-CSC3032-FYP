import os
import unittest
 
from api import app
from flask import json
import numpy as np
import math
 
TEST_DB = 'db/datasets.db'
 
 
class BasicTests(unittest.TestCase):
 
    ###############
    ## Setup App ##
    ###############

    # Setup - executed before each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        self.assertEqual(app.debug, False)
 
    # Teardown - executed after each test
    def tearDown(self):
        pass
 
    
    ################
    ## Test Cases ##
    ################
 
    def test_health_check_resource(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{"message": "API Server running"}\n')

    def test_single_prediction_bad_url_error(self):
        model = 'OptimisedSVC'
        url = 'http://web196.login-4.loginserver.ch/Joomla25/templates/atomic/zyqhjnnl.php?id=1836636'
        response = self.app.get(f'/single_prediction?url={url}&model={model}')
        resp_json = json.loads(response.data)
        self.assertEqual(resp_json['error'], True)
        self.assertEqual(resp_json['message'], 'Cannot retrieve required data for URL')

    def test_single_prediction_bad_url_values(self):
        model = 'OptimisedSVC'
        url = 'http://web196.login-4.loginserver.ch/Joomla25/templates/atomic/zyqhjnnl.php?id=1836636'
        response = self.app.get(f'/single_prediction?url={url}&model={model}')
        resp_json = json.loads(response.data)
        self.assertTrue(math.isnan(resp_json['prediction']))
        self.assertEqual(resp_json['probability'], [])
        self.assertEqual(resp_json['original_features'], {})
        self.assertEqual(resp_json['processed_features'], [])

    def test_single_prediction_valid_url_values(self):
        model = 'OptimisedSVC'
        url = 'http://www.824555.com/app/member/BrowseSport/browse.php?ptype=S'
        response = self.app.get(f'/single_prediction?url={url}&model={model}')
        resp_json = json.loads(response.data)
        self.assertTrue((math.isnan(resp_json['prediction'])) == False)
        self.assertEqual(len(resp_json['probability'][0]), 2)

        expected_keys = [
            'RegistryDate_year',
            'RegistryDate_month',
            'RegistryDate_day',
            'ExpirationDate_year',
            'ExpirationDate_month',
            'ExpirationDate_day',
            'HostCountry',
            'DomainAge'
        ]
        for key in expected_keys:
            self.assertTrue((key in resp_json['original_features'][0].keys()))
 
 
if __name__ == "__main__":
    unittest.main()