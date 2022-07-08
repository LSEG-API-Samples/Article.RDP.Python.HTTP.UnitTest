#|-----------------------------------------------------------------------------
#|            This source code is provided under the MIT license             --
#|  and is provided AS IS with no warranty or guarantee of fit for purpose.  --
#|                See the project's LICENSE.md for details.                  --
#|           Copyright Refinitiv 2022.       All rights reserved.            --
#|-----------------------------------------------------------------------------

"""
Example Code Disclaimer:
ALL EXAMPLE CODE IS PROVIDED ON AN “AS IS” AND “AS AVAILABLE” BASIS FOR ILLUSTRATIVE PURPOSES ONLY. REFINITIV MAKES NO REPRESENTATIONS OR WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, AS TO THE OPERATION OF THE EXAMPLE CODE, OR THE INFORMATION, CONTENT, OR MATERIALS USED IN CONNECTION WITH THE EXAMPLE CODE. YOU EXPRESSLY AGREE THAT YOUR USE OF THE EXAMPLE CODE IS AT YOUR SOLE RISK.
"""

import unittest
import responses
import requests
import json
import sys
import os
from dotenv import dotenv_values
config = dotenv_values("../.env.test")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rdp_controller import rdp_http_controller

class TestRDPHTTPController(unittest.TestCase):

    # A class method called before all tests in an individual class are run
    @classmethod
    def setUpClass(cls):
        # Create an app object for the RDPHTTPController class
        cls.app = rdp_http_controller.RDPHTTPController()
        # Getting the RDP APIs https://api.refinitiv.com base URL. 
        cls.base_URL = config['RDP_BASE_URL']
        # Loading Mock the RDP Auth Token success Response JSON
        with open('./fixtures/rdp_test_auth_fixture.json', 'r') as auth_fixture_input:
            cls.mock_valid_auth_json = json.loads(auth_fixture_input.read())
        
        # Mock the RDP Auth Token Expire Response JSON
        with open('./fixtures/rdp_test_token_expire_fixture.json', 'r') as auth_expire_fixture_input:
            cls.mock_token_expire_json = json.loads(auth_expire_fixture_input.read())
        
        # Mock the RDP Search Explore request message object
        cls.search_explore_payload = {
            'View': 'Entities',
            'Filter': '',
            'Select': 'IssuerCommonName,DocumentTitle,RCSExchangeCountryLeaf,IssueISIN,ExchangeName,ExchangeCode,SearchAllCategoryv3,RCSTRBC2012Leaf'
        }
        
    
    @responses.activate
    def test_login_rdp_success(self):
        """
        Test that it can log in to the RDP Auth Service
        """
        auth_endpoint = self.base_URL + config['RDP_AUTH_URL']
        
        mock_rdp_auth = responses.Response(
            method= 'POST',
            url = auth_endpoint,
            json = self.mock_valid_auth_json,
            status= 200,
            content_type= 'application/json'
        )
        responses.add(mock_rdp_auth)

        username = config['RDP_USERNAME']
        password = config['RDP_PASSWORD']
        client_id = config['RDP_CLIENTID']
        access_token = None
        refresh_token = None
        expires_in = 0

        # Calling RDPHTTPController rdp_authentication() method
        access_token, refresh_token, expires_in = self.app.rdp_authentication(auth_endpoint, username, password, client_id)

        self.assertIsNotNone(access_token) # Check if access_token is not None or Empty 
        self.assertIsNotNone(refresh_token) # Check if refresh_token is not None or Empty 
        self.assertGreater(expires_in, 0) # Check if expires_in is greater then 0
    
    @responses.activate
    def test_login_rdp_refreshtoken(self):
        """
        Test that it can handle token renewal using the refresh_token
        """
        auth_endpoint = self.base_URL + config['RDP_AUTH_URL']

        self.mock_valid_auth_json['access_token'] = 'new_access_token_mock1mock2mock3mock4mock5mock6'

        mock_rdp_auth = responses.Response(
            method= 'POST',
            url = auth_endpoint,
            json = self.mock_valid_auth_json,
            status= 200,
            content_type= 'application/json'
        )
        responses.add(mock_rdp_auth)

        username = config['RDP_USERNAME']
        password = config['RDP_PASSWORD']
        client_id = config['RDP_CLIENTID']
        access_token = None
        refresh_token = self.mock_valid_auth_json['refresh_token']
        expires_in = 0

        access_token, refresh_token, expires_in = self.app.rdp_authentication(auth_endpoint, username, password, client_id, refresh_token)

        self.assertIsNotNone(access_token) # Check if access_token is not None or Empty 
        self.assertIsNotNone(refresh_token) # Check if refresh_token is not None or Empty
        self.assertGreater(expires_in, 0) # Check if expires_in is greater then 0
    
    @responses.activate
    def test_login_rdp_invalid(self):
        """
        Test that it can handle some invalid credentials
        """
        auth_endpoint = self.base_URL + config['RDP_AUTH_URL']

        mock_rdp_auth_invalid = responses.Response(
            method= 'POST',
            url = auth_endpoint,
            json = {
                'error': 'invalid_client',
                'error_description':'Invalid Application Credential.'
            },
            status= 401,
            content_type= 'application/json'
        )
        responses.add(mock_rdp_auth_invalid)
        username = 'wrong_user1'
        password = 'wrong_password1'
        client_id = 'XXXXX'
        access_token = None
        refresh_token = None
        expires_in = 0
        with self.assertRaises(requests.exceptions.HTTPError) as exception_context:
            access_token, refresh_token, expires_in = self.app.rdp_authentication(auth_endpoint, username, password, client_id)

        self.assertIsNone(access_token)
        self.assertIsNone(refresh_token)
        self.assertEqual(expires_in, 0)
        self.assertEqual(exception_context.exception.response.status_code, 401)
        self.assertEqual(exception_context.exception.response.reason, 'Unauthorized')

        json_error = json.loads(exception_context.exception.response.text)
        self.assertIsInstance(json_error, dict) #Check if return data is  JSON (dict)
        self.assertIn('error', json_error)
        self.assertIn('error_description', json_error)
    
    def test_login_rdp_none_empty_params(self):
        """
        Test that the function can handle none/empty input
        """
        # Set None or Empty parameters
        auth_endpoint = None
        username = ''
        password = None
        client_id = 'XXXXX'
        
        access_token = None
        refresh_token = None
        expires_in = 0

        # Check if TypeError exception is raised
        with self.assertRaises(TypeError) as exception_context:
            access_token, refresh_token, expires_in = self.app.rdp_authentication(auth_endpoint, username, password, client_id)

        self.assertIsNone(access_token) # Check if access_token is None
        self.assertIsNone(refresh_token) # Check if refresh_token is None
        self.assertEqual(expires_in, 0) # Check if expires_in is 0
        # Check if the exception message is correct
        self.assertEqual(str(exception_context.exception),'Received invalid (None or Empty) arguments')


    @responses.activate
    def test_request_esg(self):
        """
        Test that it can request ESG Data
        """
        esg_endpoint = self.base_URL + config['RDP_ESG_URL']

        #Mock RDP ESG View Score valid response JSON
        with open('./fixtures/rdp_test_esg_fixture.json', 'r') as esg_fixture_input:
            mock_esg_data = json.loads(esg_fixture_input.read())

        mock_rdp_esg_viewscore = responses.Response(
            method= 'GET',
            url = esg_endpoint,
            json = mock_esg_data,
            status= 200,
            content_type= 'application/json'
        )
        responses.add(mock_rdp_esg_viewscore)

        esg_endpoint = self.base_URL + config['RDP_ESG_URL']
        universe = 'TEST.RIC'
        response = self.app.rdp_request_esg(esg_endpoint, self.mock_valid_auth_json['access_token'], universe)

        # verifying basic response
        self.assertIsInstance(response, dict) #Check if return data is  JSON (dict)
        self.assertIn('data', response) #Check if return JSON has 'data' fields
        self.assertIn('headers', response) #Check if return JSON has 'headers' fields
        self.assertIn('universe', response) #Check if return JSON has 'universe' fields

    @responses.activate
    def test_request_esg_token_expire(self):
        """
        Test that it can handle token expiration requests
        """
        esg_endpoint = self.base_URL + config['RDP_ESG_URL']
        universe = 'TEST.RIC'
        mock_rdp_esg_viewscore = responses.Response(
            method= 'GET',
            url = esg_endpoint,
            json = self.mock_token_expire_json,
            status= 401,
            content_type= 'application/json'
        )
        responses.add(mock_rdp_esg_viewscore)

        with self.assertRaises(requests.exceptions.HTTPError) as exception_context:
            response = self.app.rdp_request_esg(esg_endpoint, self.mock_valid_auth_json['access_token'], universe)
        
        self.assertEqual(exception_context.exception.response.status_code, 401)
        self.assertEqual(exception_context.exception.response.reason, 'Unauthorized')

        json_error = json.loads(exception_context.exception.response.text)
        self.assertIsInstance(json_error, dict) #Check if return data is  JSON (dict)
        self.assertIn('error', json_error)
        self.assertIn('message',json_error['error'])
        self.assertIn('status', json_error['error'])
  
    @responses.activate
    def test_request_esg_invalid_ric(self):
        """
        Test that it can handle invalid RIC request
        """
        esg_endpoint = self.base_URL + config['RDP_ESG_URL']
        mock_rdp_esg_viewscore = responses.Response(
            method= 'GET',
            url = esg_endpoint,
            json = {
                'error': {
                    'code': 412,
                    'description': 'Unable to resolve all requested identifiers.'
                }
            },
            status= 200,
            content_type= 'application/json'
        )
        responses.add(mock_rdp_esg_viewscore)

        universe = 'INVALID.RIC'

        response = self.app.rdp_request_esg(esg_endpoint, self.mock_valid_auth_json['access_token'], universe)

        self.assertIsInstance(response, dict) #Check if return data is  JSON (dict)
        self.assertIn('error', response)
        self.assertIn('code', response['error'])
        self.assertIn('description', response['error'])
    
    def test_request_esg_none_empty(self):
        """
        Test that the ESG function can handle none/empty input
        """
        esg_endpoint = None

        universe = '' 
        with self.assertRaises(TypeError) as exception_context:
            response = self.app.rdp_request_esg(esg_endpoint, self.mock_valid_auth_json['access_token'], universe)

        self.assertEqual(str(exception_context.exception),'Received invalid (None or Empty) arguments')
        
    
    @responses.activate
    def test_request_search_explore(self):
        """
        Test that it can get RIC's metadata via the RDP Search Explore Service
        """
        search_endpoint = self.base_URL + config['RDP_SEARCH_EXPLORE_URL']

        universe = 'TEST.RIC'
        # Set payload
        payload = self.search_explore_payload
        payload['Filter'] =f'RIC eq \'{universe}\''
        #Mock RDP Search Explore valid response JSON
        with open('./fixtures/rdp_test_search_fixture.json', 'r') as search_fixture_input:
            mock_search_data = json.loads(search_fixture_input.read())

        mock_rdp_search_explorer = responses.Response(
            method= 'POST',
            url = search_endpoint,
            json = mock_search_data,
            status= 200,
            content_type= 'application/json'
        )
        responses.add(mock_rdp_search_explorer)

        response = self.app.rdp_request_search_explore(search_endpoint, self.mock_valid_auth_json['access_token'], payload)

        self.assertIsInstance(response, dict) #Check if return data is  JSON (dict)
        self.assertIn('Total', response) # Check if response data has 'Total' field
        self.assertIn('Hits', response)  # Check if response data has 'Hits' field

    @responses.activate
    def test_request_search_explore_token_expire(self):
        """
        Test that it can handle token expiration requests
        """
        search_endpoint = self.base_URL + config['RDP_SEARCH_EXPLORE_URL']

        universe = 'TEST.RIC'
        # Set payload
        payload = self.search_explore_payload
        payload['Filter'] = f'RIC eq \'{universe}\''

        mock_rdp_search_explorer = responses.Response(
            method= 'POST',
            url = search_endpoint,
            json = self.mock_token_expire_json,
            status= 401,
            content_type= 'application/json'
        )
        responses.add(mock_rdp_search_explorer)

        with self.assertRaises(requests.exceptions.HTTPError) as exception_context:
            response = self.app.rdp_request_search_explore(search_endpoint, self.mock_valid_auth_json['access_token'], payload)
        
        self.assertEqual(exception_context.exception.response.status_code, 401)
        self.assertEqual(exception_context.exception.response.reason, 'Unauthorized')

        json_error = json.loads(exception_context.exception.response.text)
        self.assertIsInstance(json_error, dict) #Check if return data is  JSON (dict)
        self.assertIn('error', json_error)
        self.assertIn('message',json_error['error'])
        self.assertIn('status', json_error['error'])
    
    @responses.activate
    def test_request_search_explore_invalid_ric(self):
        """
        Test that it can handle invalid RIC request
        """
        search_endpoint = self.base_URL + config['RDP_SEARCH_EXPLORE_URL']

        universe = 'INVALID.RIC'
        payload = {
            'View': 'Entities',
            'Filter': f'RIC eq "{universe}"',
            'Select': 'IssuerCommonName,DocumentTitle,RCSExchangeCountryLeaf,IssueISIN,ExchangeName,ExchangeCode,SearchAllCategoryv3,RCSTRBC2012Leaf'
        }
        mock_rdp_search_explorer = responses.Response(
            method= 'POST',
            url = search_endpoint,
             json = {
                'Total': 0,
                'Hits': []
            },
            status= 200,
            content_type= 'application/json'
        )
        responses.add(mock_rdp_search_explorer)

        response = self.app.rdp_request_search_explore(search_endpoint, self.mock_valid_auth_json['access_token'], payload)
        
        self.assertIsInstance(response, dict) #Check if return data is  JSON (dict)
        self.assertIn('Hits', response)
        self.assertIn('Total', response)
        self.assertEqual(response['Total'], 0)
        self.assertEqual(len(response['Hits']), 0)
    
    @responses.activate
    def test_request_search_explore_invalid_json(self):
        """
        Test that it can handle invalid JSON request payload
        """
        search_endpoint = self.base_URL + config['RDP_SEARCH_EXPLORE_URL']
        payload = {'TestKey': 'InvalidValue'}

        mock_rdp_search_explorer = responses.Response(
            method= 'POST',
            url = search_endpoint,
             json = {
                'error': {
                    'id': '00000000-0000-0000-0000-000000000000',
                    'code': '400',
                    'message': 'Validation error',
                    'status': 'Bad Request',
                    'errors': [
                        {
                            'key': 'json',
                            'reason': 'json.View in body should be one of [CatalogItems Entities]'
                        }
                    ]
                }
            },
            status= 400,
            content_type= 'application/json'
        )
        responses.add(mock_rdp_search_explorer)

        with self.assertRaises(requests.exceptions.HTTPError) as exception_context:
            response = self.app.rdp_request_search_explore(search_endpoint, self.mock_valid_auth_json['access_token'], payload)
        
        self.assertEqual(exception_context.exception.response.status_code, 400)
        self.assertEqual(exception_context.exception.response.reason, 'Bad Request')

        json_error = json.loads(exception_context.exception.response.text)
        self.assertIsInstance(json_error, dict) #Check if return data is  JSON (dict)
        self.assertIn('error', json_error)
        self.assertIn('errors',json_error['error'])
        self.assertGreater(len(json_error['error']['errors']), 0)
        self.assertIn('key',json_error['error']['errors'][0])
        self.assertIn('reason',json_error['error']['errors'][0])
    
    def test_request_search_explore_none_empty(self):
        """
        Test that the Search Explore function can handle none/empty input
        """
        search_endpoint = ''

        payload = {}
        with self.assertRaises(TypeError) as exception_context:
            response = self.app.rdp_request_search_explore(search_endpoint, self.mock_valid_auth_json['access_token'], payload)

        self.assertEqual(str(exception_context.exception),'Received invalid (None or Empty) arguments')
        
if __name__ == '__main__':
    unittest.main()

