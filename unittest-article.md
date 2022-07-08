# Getting Start Unit Test for HTTP REST API Application with Python
- version: 1.0
- Last update: Jul 2022
- Environment: Windows
- Prerequisite: [Access to RDP credentials](#prerequisite)

Example Code Disclaimer:
ALL EXAMPLE CODE IS PROVIDED ON AN “AS IS” AND “AS AVAILABLE” BASIS FOR ILLUSTRATIVE PURPOSES ONLY. REFINITIV MAKES NO REPRESENTATIONS OR WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, AS TO THE OPERATION OF THE EXAMPLE CODE, OR THE INFORMATION, CONTENT, OR MATERIALS USED IN CONNECTION WITH THE EXAMPLE CODE. YOU EXPRESSLY AGREE THAT YOUR USE OF THE EXAMPLE CODE IS AT YOUR SOLE RISK.

## <a id="unittest_intro"></a>Introduction to Python Unittest framework

The [unittest](https://docs.python.org/3.9/library/unittest.html) is a Python-built unit testing framework. It supports both **test case** (the individual unit of testing) and **test runner** (a special application designed for running test cases and provides the output result).

The unittest framework has the following requirements:
1. The test cases must be methods of the class.
2. That class must be defined as a subclass of ```unittest.TestCase``` class.
3. Use a series of special assertion methods in the ```unittest.TestCase``` class instead of the built-in assert statement.
4. The methods' names must start with the letter ```test``` as a naming convention for the test runner.
5. The test cases file name must start with ```test_``` as a naming convention for the test runner.

Example from [unittest official page](https://docs.python.org/3.9/library/unittest.html):
```
# test_sample.py
import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
```

To run the test, just run the following command:
```
python -m unittest test_sample
```
Result:
```
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```
Please find more detail about the unittest framework from the following resources:
- [unittest standard library documentation](https://docs.python.org/3.9/library/unittest.html).
- [Getting Started With Testing in Python](https://realpython.com/python-testing/).

## <a id="rdp_workflow"></a>RDP APIs Application Workflow

Refinitiv Data Platform entitlement check is based on OAuth 2.0 specification. The first step of an application workflow is to get a token from RDP Auth Service, which will allow access to the protected resource, i.e. data REST API's. 

The API requires the following access credential information:
- Username: The username. 
- Password: Password associated with the username. 
- Client ID: This is also known as ```AppKey```, and it is generated using an App key Generator. This unique identifier is defined for the user or application and is deemed confidential (not shared between users). The client_id parameter can be passed in the request body or as an “Authorization” request header that is encoded as base64.

Once the authentication success, the function gets the RDP Auth service response message and keeps the following RDP token information in the variables.
- **access_token**: The token used to invoke REST data API calls as described above. The application must keep this credential for further RDP APIs requests.
- **refresh_token**: Refresh token to be used for obtaining an updated access token before expiration. The application must keep this credential for access token renewal.
- **expires_in**: Access token validity time in seconds.

Next, after the application received the Access Token (and authorization token) from RDP Auth Service, all subsequent REST API calls will use this token to get the data. Please find more detail regarding RDP APIs workflow in the following resources:
- [RDP APIs: Introduction to the Request-Response API](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials#introduction-to-the-request-response-api) page.
- [RDP APIs: Authorization - All about tokens](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials#authorization-all-about-tokens) page.

## <a id="project_info"></a>Project Structure

This example project is a Python console application that login to the RDP platform, then requests the company's Environmental Social and Governance (ESG) data and meta information from the RDP ESG and Search Explore services respectively. The project structure is as follows:


```
.
├── LICENSE.md
├── README.md
├── app.py
├── rdp_controller
│   ├── __init__.py
│   └── rdp_http_controller.py
├── requirements.txt
└── tests
    ├── __init__.py
    ├── fixtures
    │   ├── rdp_test_auth_fixture.json
    │   ├── rdp_test_esg_fixture.json
    │   ├── rdp_test_esg_fixture_tmp.json
    │   ├── rdp_test_search_fixture.json
    │   └── rdp_test_token_expire_fixture.json
    ├── test_app.py
    └── test_rdp_http_controller.py
```
* app.py: The main console application.
* rdp_controller/rdp_http_controller.py: The main HTTP operations class. This is our focusing class for unit testing.
* tests/test_rdp_http_controller.py: The main test cases class that tests all rdp_http_controller.py class's methods. This is our focus test suite in this project.
* tests/test_app.py: The test suite class that tests some app.py methods.
* tests/fixtures: The test suite fixture/resource files.

### <a id="unittest_rdp_authen"></a>Unit Testing RDP APIs Authentication

Let’s start with the class that operates HTTP request-response messages with the RDP services. The ```rdp_controller/rdp_http_controller.py``` class uses the Requests library to send and receive data with the RDP HTTP REST APIs. The code for the RDP authentication is shown below.

```
# rdp_controller/rdp_http_controller.py

import requests
import json

class RDPHTTPController():

    # Constructor Method
    def __init__(self):
        self.scope = 'trapi'
        self.client_secret = ''
        pass
    
    # Send HTTP Post request to get Access Token (Password Grant and Refresh Grant) from the RDP Auth Service
    def rdp_authentication(self, auth_url, username, password, client_id, old_refresh_token = None):

        if not auth_url or not username or not password or not client_id:
            raise TypeError('Received invalid (None or Empty) arguments')

        access_token = None
        refresh_token = None
        expires_in = 0
        if old_refresh_token is None: # For the Password Grant scenario
            payload=f'username={username}&password={password}&grant_type=password&scope={self.scope}&takeExclusiveSignOnControl=true&client_id={client_id}'
        else:  # For the Refresh Token scenario
            payload=f'username={username}&refresh_token={old_refresh_token}&grant_type=refresh_token&client_id={client_id}'

        # Send HTTP Request
        try:
            response = requests.post(auth_url, 
                headers = {'Content-Type':'application/x-www-form-urlencoded'}, 
                data = payload, 
                auth = (client_id, self.client_secret)
                )
        except Exception as exp:
            print(f'Caught exception: {exp}')
    

        if response.status_code == 200:  # HTTP Status 'OK'
            print('Authentication success')
            access_token = response.json()['access_token']
            refresh_token = response.json()['refresh_token']
            expires_in = int(response.json()['expires_in'])
        if response.status_code != 200:
            print(f'RDP authentication failure: {response.status_code} {response.reason}')
            print(f'Text: {response.text}')
            raise requests.exceptions.HTTPError(f'RDP authentication failure: {response.status_code} - {response.text} ', response = response )
        
        return access_token, refresh_token, expires_in
```

The ```rdp_authentication()``` method above just create the request message payload, and send it to the RDP Auth service as an HTTP Post request. The return values can be as follows
- If the authentication success, returns the access_token, refresh_token, and expires_in information to the caller.
- If the URL or credentials parameters are empty or none, raise the TypeError exception to the caller.
- If the authentication fails, raise the Requests' HTTPError exception to the caller with HTTP status response information.

Let’s leave the ```rdp_authentication()``` method there and continue with the test case. The basic test case scenario is to check if the ```rdp_authentication()``` method can handle a valid RDP login and empty parameters scenarios. 

The test class is ```tests\test_rdp_http_controller.py``` file (please noticed a *tests* folder). It loads the test configurations such as the RDP APIs URLs from a ```.env.test``` environment variables file.

```
# test_rdp_http_controller.py

import unittest
import json
import sys
import os
from dotenv import dotenv_values
config = dotenv_values("../.env.test")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rdp_controller import rdp_http_controller

class TestRDPHTTPController(unittest.TestCase):

    # A class method called before tests in an individual class are run
    @classmethod
    def setUpClass(cls):
        # Create an app object for the RDPHTTPController class
        cls.app = rdp_http_controller.RDPHTTPController()
        # Getting the RDP APIs https://api.refinitiv.com base URL. 
        cls.base_URL = config['RDP_BASE_URL']
    
    def test_login_rdp_success(self):
        """
        Test that it can log in to the RDP Auth Service
        """
        auth_endpoint = self.base_URL + config['RDP_AUTH_URL']
        
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
        
if __name__ == '__main__':
    unittest.main()
```

The ```setUpClass()``` is a class method that is called only once for the whole class before all the tests. The function is useful for setting up a *fixture* which can be sample data, preconditions states, context, or resources needed to run a test. We initialize the RDPHTTPController object (as ```app``` class variable)  and the RDP Base URL string (as ```base_URL``` class variable)  as our fixture here.

Note: The counterpart method of ```setUpClass()``` method is ```tearDownClass()``` which is called after all tests in the class have run.

The ```test_login_rdp_success()``` is a test case for the success RDP Authentication login scenario. It just sends the RDP Auth Service URL and RDP credentials to the ```rdp_authentication()``` method and checks the response token information. Please noticed that a unit test just focuses on if the rdp_authentication() returns no empty/zero token information only. The token content validation would be in a system test (or later) phase.

```
self.assertIsNotNone(access_token) # Check if access_token is not None or Empty 
self.assertIsNotNone(refresh_token) # Check if refresh_token is not None or Empty 
self.assertGreater(expires_in, 0) # Check if expires_in is greater then 0
```

Please see more detail about the supported assertion methods on the [unittest framework](https://docs.python.org/3.9/library/unittest.html) page.

The ```test_login_rdp_none_empty_params()``` is a test case that check if the ```rdp_authentication()``` method handles empty or none parameters as expected (throws the TypeError exception and not return token information to a caller).

```
# Check if TypeError exception is raised
with self.assertRaises(TypeError) as exception_context:
    access_token, refresh_token, expires_in = self.app.rdp_authentication(auth_endpoint, username, password, client_id)

self.assertIsNone(access_token) # Check if access_token is None
...
self.assertEqual(str(exception_context.exception),'Received invalid (None or Empty) arguments')
```
The example of a test runner result is shown below.

```
$>tests> python -m unittest test_rdp_http_controller
.Authentication success
.
----------------------------------------------------------------------
Ran 2 tests in 0.014s

OK
```

If you input invalid RDP credentials in a ```.env.test``` file, a  test runner shows the following test failure result (Do not worry, I will cover fail test cases later).

```
$>python -m unittest test_rdp_http_controller
.RDP authentication failure: 401 Unauthorized
Text: {"error":"invalid_client"  ,"error_description":"Invalid Application Credential." } 
E
======================================================================
ERROR: test_login_rdp_success (test_rdp_http_controller.TestRDPHTTPController)
Test that it can logged in to the RDP Auth Service
----------------------------------------------------------------------
Traceback (most recent call last):
  File "....\rdp_python_unittest\tests\test_rdp_http_controller.py", line 72, in test_login_rdp_success
    access_token, refresh_token, expires_in = self.app.rdp_authentication(auth_endpoint, username, password, client_id)
  File "....\rdp_python_unittest\rdp_controller\rdp_http_controller.py", line 48, in rdp_authentication
    raise requests.exceptions.HTTPError(f'RDP authentication failure: {response.status_code} - {response.text} ', response = response )
requests.exceptions.HTTPError: RDP authentication failure: 401 - {"error":"invalid_client"  ,"error_description":"Invalid Application Credential." }    

----------------------------------------------------------------------
Ran 2 tests in 0.816s

FAILED (errors=1)
```

However, the test suite above makes HTTP requests to RDP APIs in every run. It is not a good idea to flood requests to external services every time developers run a test suite when they have updated the code or configurations. 

Unit test cases should be able to run independently without relying on external services or APIs. The external dependencies add uncontrolled factors (such as network connection, data reliability, etc) to unit test cases. Those components-to-components testing should be done in an integration testing phase. 

So, how can we unit test HTTP request method calls without sending any HTTP request messages to an actual server? Fortunately, developers can simulate the HTTP request and response messages with *a mock object*.

## <a id="unittest_mocking"></a>Mocking Python HTTP API call with Responses

A mock is a fake object that is constructed to look and act like real data within a testing environment. We can simulate the various scenario of the real data with a mock object, then use a mock library to trick the system into thinking that that mock is the real one. 

The purpose of mocking is to isolate and focus on the code being tested and not on the behavior or state of external dependencies. By mocking out external dependencies, developers can run tests as often without being affected by any unexpected changes or irregularities of those dependencies. Mocking also helps developers save time and computing resources if they have to test HTTP requests that fetch a lot of data.

This example project uses the [Responses](https://github.com/getsentry/responses) library for mocking the Requests library. 

### <a id="add_mock_test"></a>Adding a mock Object to the test case

So, I will start with a mock object for testing a successful RDP login case. Firstly, create a *rdp_test_auth_fixture.json* fixture file with a dummy content of the RDP authentication success response message in a *tests/fixtures* folder. 

```
{
    "access_token": "access_token_mock1mock2mock3mock4mock5",
    "refresh_token": "refresh_token_mock1mock2mock3mock4mock5",
    "expires_in": "600",
    "scope": "test1 test2 test3 test4 test5",
    "token_type": "Bearer"
}
```

Next, load this *rdp_test_auth_fixture.json* file in the ```setUpClass()``` method to a ```mock_valid_auth_json``` class variable. The other test cases can use this mock json object for the dummy access token information.

```
# test_rdp_http_controller.py

import unittest
import requests
import json
import sys
import os
from dotenv import dotenv_values
config = dotenv_values("../.env.test")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rdp_controller import rdp_http_controller

class TestRDPHTTPController(unittest.TestCase):

    # A class method called before tests in an individual class are run
    @classmethod
    def setUpClass(cls):
        # Create an app object for the RDPHTTPController class
        cls.app = rdp_http_controller.RDPHTTPController()
        # Getting the RDP APIs https://api.refinitiv.com base URL. 
        cls.base_URL = config['RDP_BASE_URL']
        # Loading Mock RDP Auth Token success Response JSON
        with open('./fixtures/rdp_test_auth_fixture.json', 'r') as auth_fixture_input:
            cls.mock_valid_auth_json = json.loads(auth_fixture_input.read())
        
```

The Responses library lets developers register mock responses to the Requests library and cover the test method with ```responses.activate``` decorator. Developers can specify the endpoint URL, HTTP method, status response, response message, etc of that request via a ```responses.add()``` method. 

Example Code:

```
# test_rdp_http_controller.py

import unittest
import responses
import requests
import json
import sys
import os

...

class TestRDPHTTPController(unittest.TestCase):

    # A class method called before tests in an individual class are run
    @classmethod
    def setUpClass(cls):
        ...
        
    
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

        # Assertions
        ...
```

The code above set a Responses mock object with the *https://api.refinitiv.com/auth/oauth2/v1/token* URL and HTTP *POST* method. The Requests library then returns a ```mock_valid_auth_json``` JSON message with HTTP status *200* and Content-Type *application/json* to the application for all HTTP *POST* request messages to *https://api.refinitiv.com/auth/oauth2/v1/token* URL without any network operations between the machine and the actual RDP endpoint.

### <a id="unittest_rdp_authen_fail"></a>Testing Invalid RDP Authentication Request-Response

This mock object is also useful for testing false cases such as invalid login too.  The ```test_login_rdp_invalid()``` method is a test case for the RDP Authentication login failure scenario. We set a Responses mock object for the *https://api.refinitiv.com/auth/oauth2/v1/token* URL and HTTP *POST* method with the expected error response message and status (401 - Unauthorized). 

```
# test_rdp_http_controller.py

...

class TestRDPHTTPController(unittest.TestCase):

    ...        
    
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
        ...
```

Once the ```rdp_authentication()``` method is called, the test case verifies if the method raises the ```requests.exceptions.HTTPError``` exception with the expected error message and status. The test case also makes assertions to check if the method does not return token information to a caller.

```
# test_rdp_http_controller.py

...

class TestRDPHTTPController(unittest.TestCase):

    ...    
    
    @responses.activate
    def test_login_rdp_invalid(self):
        """
        Test that it handle some invalid credentials
        """
        ...
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
```

With mocking, a test case never needs to send actual request messages to the RDP APIs, so we can test more scenarios for other RDP services too.

## <a id="rdp_get_data"></a>Unit Testing for RDP APIs Data Request

That brings us to requesting the RDP APIs data. All subsequent REST API calls use the Access Token via the *Authorization* HTTP request message header as shown below to get the data. 
- Header: 
    * Authorization = ```Bearer <RDP Access Token>```

Please notice *the space* between the ```Bearer``` and ```RDP Access Token``` values.

The application then creates a request message in a JSON message format or URL query parameter based on the interested service and sends it as an HTTP request message to the Service Endpoint. Developers can get RDP APIs the Service Endpoint, HTTP operations, and parameters from Refinitiv Data Platform's [API Playground page](https://api.refinitiv.com/) - which is an interactive documentation site developers can access once they have a valid Refinitiv Data Platform account.

The example console application consumes content from the following RDP Services:
- ESG Service ```/data/environmental-social-governance/<version>/views/scores-full``` endpoint that provides full coverage of Refinitiv's proprietary ESG Scores with full history for consumers.
- Discovery Search Explore Service ```/discover/search/<version>/explore``` endpoint that explore Refinitiv data based on searching options.

However, this development article covers the ESG Service test cases only. The Discovery Search Explore Service's test cases have the same test logic as the ESG's test cases.

## <a id="unittest_rdp_esg"></a>Unit Testing HTTP Request Source Code for The RDP ESG Service

Now let me turn to test the Environmental Social and Governance (ESG) service endpoint. The code in the ```rdp_controller/rdp_http_controller.py``` class for requesting the ESG data is shown below.

```
# rdp_controller/rdp_http_controller.py

import requests
import json

class RDPHTTPController():

    ...
    # Send HTTP Get request to the RDP ESG Service
    def rdp_request_esg(self, esg_url, access_token, universe):

        if not esg_url or not access_token or not universe:
            raise TypeError('Received invalid (None or Empty) arguments')

        payload = {'universe': universe}
        # Request data for ESG Score Full Service
        try:
            response = requests.get(esg_url, headers={'Authorization': f'Bearer {access_token}'}, params = payload)
        except Exception as exp:
            print(f'Caught exception: {exp}')

        if response.status_code == 200:  # HTTP Status 'OK'
            print('Receive ESG Data from RDP APIs')
        else:
            print(f'RDP APIs: ESG data request failure: {response.status_code} {response.reason}')
            print(f'Text: {response.text}')
            raise requests.exceptions.HTTPError(f'ESG data request failure: {response.status_code} - {response.text} ', response = response )

        return response.json()
```

The ```rdp_request_esg()``` method above just create the request message payload, and send it to the RDP ESG service as HTTP GET request with the Requests ```requests.get()``` method. The return values can be as follows
- If the request success (HTTP status is 200), returns the response data in JSON message format.
- If the URL or access token, or universe values are empty or none, raise the TypeError exception to the caller.
- If the request fails, raise the Requests' HTTPError exception to the caller with HTTP status response information.


### <a id="unittest_rdp_esg_success"></a>Testing a valid RDP ESG Request-Response

The first test case is the request success scenario. I will begin by creating a fixture file with a valid ESG dummy response message. A file is *rdp_test_esg_fixture.json* in a *tests/fixtures* folder.

```
{
  "links": {
    "count": 5
  },
  "variability": "variable",
  "universe": [
    {
      "Instrument": "TEST.RIC",
      "Company Common Name": "TEST ESG Data",
      "Organization PermID": "XXXXXXXXXX",
      "Reporting Currency": "USD"
    }
  ],
  "data": [
    [
      "TEST.RIC",
      "2021-12-31",
      99.9999999999999,
      99.9999999999999,
      ...
    ],
   ...
  ],
  ...
  ,
  "headers": [
    ....
    {
      "name": "TEST 1",
      "title": "ESG Score",
      "type": "number",
      "decimalChar": ".",
      "description": "TEST description"
    }...
  ]
}
```

Next, create the ```test_request_esg()``` method in the test_rdp_http_controller.py file to test the easiest test case, the successful ESG data request-response scenario.  This method creates a mock object for the RDP ```https://api.refinitiv.com/data/environmental-social-governance/v2/views/scores-full``` endpoint URL with the HTTP *GET* method. 

```
# test_rdp_http_controller.py
...

class TestRDPHTTPController(unittest.TestCase):
     
    ...

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
        ...

```
When the Requests library receives the HTTP GET request for that URL, it returns a mock ESG data JSON object with HTTP Status *200* and Content-Type *application/json* to the application. The ```test_request_esg()``` method then verifies if the response data is in JSON/[Dictionaries](https://docs.python.org/3.9/tutorial/datastructures.html#dictionaries) type, and checks if the message contains the basic ESG fields. 

```
# test_rdp_http_controller.py

class TestRDPHTTPController(unittest.TestCase):
  
    ...

    @responses.activate
    def test_request_esg(self):
        """
        Test that it can request ESG Data
        """
        ...
        response = self.app.rdp_getESG(esg_endpoint, self.mock_valid_auth_json['access_token'], universe)

        # verifying basic response
        self.assertIsInstance(response, dict) #Check if return data is  JSON (dict)
        self.assertIn('data', response) #Check if return JSON has 'data' fields
        self.assertIn('headers', response) #Check if return JSON has 'headers' fields
        self.assertIn('universe', response) #Check if return JSON has 'universe' fields
```

### <a id="unittest_rdp_esg_expire"></a>Testing Requesting RDP ESG data with an expired token

That brings us to one of the most common RDP APIs failure scenarios, applications request data from RDP with an expired access token. 
The ```test_request_esg_token_expire()``` method is the one for testing this case with the RDP ESG Service. 

The first step is to create a JSON file ```tests/rdp_test_token_expire_fixture.json``` as a test fixture with the following content.

```
{
    "error": {
        "id": "XXXXXXXXXX",
        "code": "401",
        "message": "token expired",
        "status": "Unauthorized"
    }
}
```

All RDP data services use the same token expire error message, so we load this fixture file as a class variable named ```mock_token_expire_json``` to use in all test case methods. 

```
# test_rdp_http_controller.py

class TestRDPHTTPController(unittest.TestCase):

    # A class method called before tests in an individual class are run
    @classmethod
    def setUpClass(cls):
        # Set up previous class variables
        ...
        
        # Mock RDP Auth Token Expire Response JSON
        with open('./fixtures/rdp_test_token_expire_fixture.json', 'r') as auth_expire_fixture_input:
            cls.mock_token_expire_json = json.loads(auth_expire_fixture_input.read())

```

The token expires error message is sent from the RDP services to applications with HTTP error status (401 - **As of July 2022**), the ```test_request_esg_token_expire()``` method simulates the token expire error message and HTTP 401 status with a mock object as follows.

```
# test_rdp_http_controller.py

class TestRDPHTTPController(unittest.TestCase):

    # Previous test cases
    ...

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

```

Next, this test case verifies if the ```rdp_request_esg()``` method raises the ```requests.exceptions.HTTPError``` exception with the expected error message and status.

```
# test_rdp_http_controller.py

class TestRDPHTTPController(unittest.TestCase):

    # Previous test cases
    ...

    @responses.activate
    def test_request_esg_token_expire(self):
        """
        Test that it can handle token expire requests
        """
        # Previous code
        ...
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
  
```

The other common RDP APIs failure scenarios is the application sends the request message to RDP without the access token in the HTTP request' header. However, the *access token* is one of the ```rdp_request_esg()``` method required parameters. If the access token is not presented (None or Empty), the method raise the TypeError exception and not send HTTP request message to the RDP. The ```test_request_esg_none_empty()``` method is the one that covers this test case.


### <a id="unittest_rdp_esg_invalid"></a>Testing Requesting RDP ESG data with an invalid item

Now we come to other common test cases, what if users request invalid item name data from the RDP ESG service? We can use a mock object to simulate invalid item request-response messages too.

When the ESG Service receives a request message with an invalid item name, it returns the following error response message to the applications as HTTP Status *200* (**As of July 2022**):

```
{
    'error': {
        'code': 412,
        'description': 'Unable to resolve all requested identifiers.'
    }
}
```

The ```test_request_esg_invalid_ric()``` method set a mock invalid item request-response messages to the Requests library, and check if the ```rdp_request_esg()``` method returns the error message with HTTP status *200* as expected. 

```
# test_rdp_http_controller.py

class TestRDPHTTPController(unittest.TestCase):

    # Previous Code
    ...
  
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
        
```

That covers all I wanted to say about unit testing the HTTP requests for the RDP ESG service.

## <a id="unittest_rdp_search"></a>Unit Testing HTTP Request Source Code for the RDP Search Explore Service

The source code that uses the Request library ```requests.post()``` method to send HTTP POST request message to the RDP Search Explore is available at the ```rdp_request_search_explore()``` method of the ```rdp_controller/rdp_http_controller.py``` class. 

The test cases for this ```rdp_request_search_explore()``` method have the same testing and mocking logic as all previous cases that I have mentions above. You can find more details in the following test cases methods:
- ```test_request_search_explore()``` method: Unit testing a valid request-response
- ```test_request_search_explore_token_expire()``` method: Unit testing a token expired case
- ```test_request_search_explore_invalid_ric()``` method: Unit testing an invalid ric case
- ```test_request_search_explore_invalid_json()``` method: Unit testing an invalid JSON post message case
- ```test_request_search_explore_none_empty()```method: Unit testing an empty (or None) input parameters case

That’s all I have to say about unit testing the Python HTTP code with Requests and Responses libraries.

## <a id="how_to_run"></a>How to run the example test suite

Please see how to run the project test suit in the [README.md](README.md#how_to_run) file.

## <a id="references"></a>References

For further details, please check out the following resources:
* [Refinitiv Data Platform APIs page](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis) on the [Refinitiv Developer Community](https://developers.refinitiv.com/) website.
* [Refinitiv Data Platform APIs Playground page](https://api.refinitiv.com).
* [Refinitiv Data Platform APIs: Introduction to the Request-Response API](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials#introduction-to-the-request-response-api).
* [Refinitiv Data Platform APIs: Authorization - All about tokens](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials#authorization-all-about-tokens).
* [Limitations and Guidelines for the RDP Authentication Service](https://developers.refinitiv.com/en/article-catalog/article/limitations-and-guidelines-for-the-rdp-authentication-service) article.
* [Getting Started with Refinitiv Data Platform](https://developers.refinitiv.com/en/article-catalog/article/getting-start-with-refinitiv-data-platform) article.
* [Python unittest framework official page](https://docs.python.org/3/library/unittest.html).
* [Responses library page](https://github.com/getsentry/responses).
* [Python Guide: Testing Your Code](https://docs.python-guide.org/writing/tests/) article.
* [Getting Started With Testing in Python](https://realpython.com/python-testing/) article.
* [Mocking External APIs in Python](https://realpython.com/testing-third-party-apis-with-mocks/) article.
* [How To Use unittest to Write a Test Case for a Function in Python](https://www.digitalocean.com/community/tutorials/how-to-use-unittest-to-write-a-test-case-for-a-function-in-python) article.
* [Mocking API calls in Python](https://auth0.com/blog/mocking-api-calls-in-python/) article.
* [How and when to use Unit Testing properly](https://softwareengineering.stackexchange.com/questions/89064/how-and-when-to-use-unit-testing-properly) post.
* [13 Tips for Writing Useful Unit Tests](https://betterprogramming.pub/13-tips-for-writing-useful-unit-tests-ca20706b5368) blog post.

For any questions related to Refinitiv Data Platform APIs, please use the [RDP APIs Forum](https://community.developers.refinitiv.com/spaces/231/index.html) on the [Developers Community Q&A page](https://community.developers.refinitiv.com/).