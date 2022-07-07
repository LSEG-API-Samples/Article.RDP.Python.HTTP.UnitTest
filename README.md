# Getting Start Unit Test for HTTP REST API Application with Python
- version: 1.0
- Last update: Jul 2022
- Environment: Windows
- Prerequisite: [Access to RDP credentials](#prerequisite)

Example Code Disclaimer:
ALL EXAMPLE CODE IS PROVIDED ON AN “AS IS” AND “AS AVAILABLE” BASIS FOR ILLUSTRATIVE PURPOSES ONLY. REFINITIV MAKES NO REPRESENTATIONS OR WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, AS TO THE OPERATION OF THE EXAMPLE CODE, OR THE INFORMATION, CONTENT, OR MATERIALS USED IN CONNECTION WITH THE EXAMPLE CODE. YOU EXPRESSLY AGREE THAT YOUR USE OF THE EXAMPLE CODE IS AT YOUR SOLE RISK.

## <a id="intro"></a>Introduction

Today, applications are bigger and complex. A few changed on the source code to add more features or fix bugs can make unexpected behavior to an application. Developers cannot just wait for the test result from the QA team anymore. They needs to do a unit testing regularly as integral part of the development process. 

The unit testing is a software testing method that helps developers verify if any changes break the code. Unit testing significantly improves code quality, saves time to find software bugs in early stage of development lifecycle, and improve deployment velocity. Unit testing is currently a main process of a modern Agile software development practice such as CI/CD (Continuous Integration/Continuous Delivery), TDD (Test-driven development), etc.

The modern applications also need to connect to other services like APIs, Database, Data storage, etc. The unit testing needs to cover those modules too. This example project shows how to run unit test cases for a [Python](https://www.python.org/) application that performs HTTP REST operations which is the most basic task of today application functionality. With unit testing, developers can verify if their code can connect and consume content via HTTP REST API in any code updates. 

The demo application uses a de-facto [Requests](https://requests.readthedocs.io/en/latest/) library to connect to the [Refinitiv Data Platform (RDP) APIs](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis) as the example HTTP REST APIs, and uses the Python built-in [unittest](https://docs.python.org/3.9/library/unittest.html) as a test framework.

**Note**:
This demo project is not cover all test cases for the HTTP operations and all RDP APIs services. It aims to give the readers an idea about how to unit test an application that makes a HTTP connection with Python only. 

## Unit Testing Overview

Unit testing is a smallest test that focusing on checks that a single part of the application operates correctly. It breaks an application into a smallest, isolated, testable component called *units*, and then test them individually. The unit is mostly a function or method call or procedure in the application source code. Developers and QA can test each unit by sending any data into that unit and see if it functions as intended. 

A unit test helps developers to isolate what is broken in their application easier and faster then testing an entire system as a whole. It is the first level of testing done during the development process before integration testing. It is mostly done by the developers  automated or manually to verify their code.

## Introduction to Python Unittest framework

The [unittest](https://docs.python.org/3.9/library/unittest.html) is Python built unit testing framework. It supports both **test case** (the individual unit of testing) and **test runner** (a special application designed for running test cases and provides the output result).

The unittest framework has the following requirements:
1. The test cases must be methods of the class.
2. That class must be defined as a subclass of ```unittest.TestCase``` class.
3. Use a series of special assertion methods in the ```unittest.TestCase``` class instead of the built-in assert statement.
4. The methods names must be start with the letter ```test``` as a naming convention for the test runner.
5. The test cases file name must be start with ```test_``` as a naming convention for the test runner.

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

## <a id="whatis_rdp"></a>What is Refinitiv Data Platform (RDP) APIs?

The [Refinitiv Data Platform (RDP) APIs](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis) provide various Refinitiv data and content for developers via easy-to-use Web-based API.

RDP APIs give developers seamless and holistic access to all of the Refinitiv content such as Environmental Social and Governance (ESG), News, Research, etc, and commingled with their content, enriching, integrating, and distributing the data through a single interface, delivered wherever they need it.  The RDP APIs delivery mechanisms are the following:
* Request - Response: RESTful web service (HTTP GET, POST, PUT or DELETE) 
* Alert: delivery is a mechanism to receive asynchronous updates (alerts) to a subscription. 
* Bulks:  deliver substantial payloads, like the end-of-day pricing data for the whole venue. 
* Streaming: deliver real-time delivery of messages.

This example project is focusing on the Request-Response: RESTful web service delivery method only.  

For more detail regarding the Refinitiv Data Platform, please see the following APIs resources: 
- [Quick Start](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/quick-start) page.
- [Tutorials](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials) page.

### <a id="rdp_workflow"></a>RDP APIs Application Workflow

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

## Project Structure

This example project is a Python console application that login to RDP, then requests the company Environmental Social and Governance (ESG) data and information from the RDP ESG and Search Explore services respectively. The project structure is as follows:


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
    ├── test_app.py
    └── test_rdp_http_controller.py
```
* app.py: The main console application.
* rdp_controller/rdp_http_controller.py: The main HTTP operations class. This is our focusing class for unit testing.
* tests/test_rdp_http_controller.py: The main test cases class that test all rdp_http_controller.py class's methods. This is our focusing test cases in this project.
* tests/test_app.py: The main test cases class that test some app.py methods.

### Unit Testing RDP APIs Authentication

The ```rdp_controller/rdp_http_controller.py``` class uses the Requests library to send and receive data with the RDP HTTP REST APIs. The code for the RDP authentication is shown below.

```
import requests
import json

class RDPHTTPController():

    # Constructor Method
    def __init__(self):
        self.scope = 'trapi'
        self.client_secret = ''
        pass
    
    # Send HTTP Post request to get Access Token (Password Grant and Refresh Grant) from RDP Auth Service
    def rdp_authentication(self, auth_url, username, password, client_id, old_refresh_token = None):
        """
        Send Authentication to RDP Auth service
        """

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

The ```rdp_authentication``` method above just perform the following tasks:

The ```rdp_authentication()``` method above just create the request message payload, and send it to the RDP Auth service as HTTP Post request. The return values can be as follows
- If the authentication success, returns the access_token, refresh_token, and expires_in information to the caller.
- If the URL or credentials parameters are empty or none, raises TypeError exception to the caller.
- If the authentication fail, raises the Requests's HTTPError exception to the caller with HTTP status response information.

Let's start with the basic test cases to check if the ```rdp_authentication()``` method can handle a valid RDP login and empty parameters scenarios. 

The test class is ```tests\test_rdp_http_controller.py``` file (please noticed a *tests* folder). It loads the test configurations such as the RDP APIs URLs from a ```.env.test``` environment variables file.

```
#test_rdp_http_controller.py

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
        Test that it can logged in to the RDP Auth Service (using Mock)
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

The ```setUpClass()``` is a class method that is called only onces for the whole class before all the tests. The function is useful for set up a *fixture* which can be sample data, preconditions states, context or resources need to run a test. We initialize the RDPHTTPController object (as ```app``` class variable)  and the RDP Base URL string (as ```base_URL``` class variable)  as our fixture here.

Note: The counterpart method of ```setUpClass()``` method is ```tearDownClass()``` which is called after all tests in the class have run.

The ```test_login_rdp_success()``` is a test case for the success RDP Authentication login scenario. It just send the RDP Auth Service URL and RDP credentials to the ```rdp_authentication()``` method and check the response token information. Please noticed that a unit test just focusing on if the rdp_authentication() returns none empty/zero token information only. The token content validation would be in a system test (or later) phase.

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

However, the test suite above make HTTP requests to RDP APIs in every run. It is not a good idea to flood requests to external services every time developers run test suite when they have updated the code or configurations. 

Unit test cases should be able to run independently without rely on external services or APIs. The external dependencies add uncontrolled factors (such as network connection, data reliability, etc) to unit test cases. Those components-to-components testing should be done in an integration testing phase. 

So, how can we unit test HTTP request methods calls without sending any HTTP request messages to an actual server? Fortunately, developers can simulate the HTTP request and response messages with a Mock object.

## Mocking Python HTTP API call with Responses

A mock is a fake object that is constructed to look and act like real data within a testing environment. We can simulates various scenario of the real data with mock object, then use a mock library to trick the system into thinking that that mock is the real one. 

The purpose of mocking is to isolate and focus on the code being tested and not on the behavior or state of external dependencies. By mocking out external dependencies, developers can run tests as often without being affected by any unexpected changes or irregularities of those dependencies. Mocking also helps developers save time and computing resources if they have to test HTTP requests that fetch a lot of data.

This example project uses the [Responses](https://github.com/getsentry/responses) library for mocking the Requests library. 

So, I will start off with a mock object for testing a success RDP login case. Firstly, create a *rdp_test_auth_fixture.json* fixture file with a dummy content of the RDP authentication success response message in a *tests/fixtures* folder. 

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
#test_rdp_http_controller.py

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

The Responses library lets developers register mock responses to the Requests library and cover test method with ```responses.activate``` decorator. Developers can specify the endpoint URL, HTTP method, status response, response message, etc of that request via a ```responses.add()``` method. 

Example Code:

```
#test_rdp_http_controller.py

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
        Test that it can logged in to the RDP Auth Service (using Mock)
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

### Testing Invalid RDP Authentication Request-Response

This mock object also useful for testing the false cases such as invalid login too. 

```
#test_rdp_http_controller.py

...

class TestRDPHTTPController(unittest.TestCase):

    # A class method called before tests in an individual class are run
    @classmethod
    def setUpClass(cls):
        ...

    @responses.activate
    def test_login_rdp_success(self):
        ...
        
    
    @responses.activate
    def test_login_rdp_invalid(self):
        """
        Test that it handle some invalid credentials
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
        self.assertIn('error', json_error)
        self.assertIn('error_description', json_error)

```

The ```test_login_rdp_invalid()``` method is a test case for the failure RDP Authentication login scenario. We set a Responses mock object for the *https://api.refinitiv.com/auth/oauth2/v1/token* URL and HTTP *POST* method with the expected error response message and status (401 - Unauthorized). 

Once the ```rdp_authentication()``` method is called, the test case verify if the method raises the ```requests.exceptions.HTTPError``` exception with the expected error message and status. The test case also make assertions to check if the method not return token information to a caller.

With mocking, a test case never need to send actual request messages to the RDP APIs, so we can test more scenarios for other RDP services too.

## <a id="rdp_get_data"></a>Unit Testing for RDP APIs Data Request

That brings us to requesting the RDP APIs data. All subsequent REST API calls use the Access Token via the *Authorization* HTTP request message header as shown below to get the data. 
- Header: 
    * Authorization = ```Bearer <RDP Access Token>```

Please notice *the space* between the ```Bearer``` and ```RDP Access Token``` values.

The application then creates a request message in a JSON message format or URL query parameter based on the interested service and sends it as an HTTP request message to the Service Endpoint. Developers can get RDP APIs the Service Endpoint, HTTP operations, and parameters from Refinitiv Data Platform's [API Playground page](https://api.refinitiv.com/) - which is an interactive documentation site developers can access once they have a valid Refinitiv Data Platform account.

The example console application consume content from the following the RDP Services:
- ESG Service ```/data/environmental-social-governance/<version>/views/scores-full``` endpoint that provides full coverage of Refinitiv's proprietary ESG Scores with full history for consumers.
- Discovery Search Explore Service ```/discover/search/<version>/explore``` endpoint that explore Refinitiv data based on searching options.

However, this development article covers the ESG Service test cases only. The Discovery Search Explore Service's test cases have the same test logic as the ESG's test cases.

## Testing ESG Data 

Now let me turn to testing the Environmental Social and Governance (ESG) service endpoint. 

### Testing a valid RDP ESG Request-Response

I will begin by creating a fixture file with a valid ESG dummy response message. A file is *rdp_test_esg_fixture.json* in a *tests/fixtures* folder.

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
Next, create the ```test_request_esg()``` method in test_rdp_http_controller.py file to test the valid ESG data request-response test case. 

```
#test_rdp_http_controller.py
...

class TestRDPHTTPController(unittest.TestCase):

    # A class method called before tests in an individual class are run
    @classmethod
    def setUpClass(cls):
       ...
        
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
        response = self.app.rdp_getESG(esg_endpoint, self.mock_valid_auth_json['access_token'], universe)

        # verifying basic response
        self.assertIn('data', response) #Check if return JSON has 'data' fields
        self.assertIn('headers', response) #Check if return JSON has 'headers' fields
        self.assertIn('universe', response) #Check if return JSON has 'universe' fields

```

## Project Structure

## Python run app


## Python Test

```
python -m unittest test_http

python -m unittest test_rdp_http_controller

python -m unittest discover 

python -m unittest test_app
```

### Docker

```
docker build . -t python_unittest

docker run -it --name python_unittest python_unittest
```

## <a id="references"></a>References

https://realpython.com/python-testing/
https://realpython.com/testing-third-party-apis-with-mocks/

https://pymotw.com/2/unittest/

https://auth0.com/blog/mocking-api-calls-in-python/

https://www.digitalocean.com/community/tutorials/how-to-use-unittest-to-write-a-test-case-for-a-function-in-python

https://stackoverflow.com/questions/62938765/writing-a-unit-test-for-python-rest-api-function


https://docs.python.org/3/library/unittest.html

https://web.archive.org/web/20150315073817/http://www.xprogramming.com/testfram.htm

https://betterprogramming.pub/13-tips-for-writing-useful-unit-tests-ca20706b5368

https://docs.python-guide.org/writing/tests/

https://softwareengineering.stackexchange.com/questions/89064/how-and-when-to-use-unit-testing-properly

https://en.wikipedia.org/wiki/Mock_object

