# Getting Start Unit Test for HTTP REST API Application with Python
- version: 1.0
- Last update: Jul 2022
- Environment: Windows
- Prerequisite: [Access to RDP credentials](#prerequisite)

Example Code Disclaimer:
ALL EXAMPLE CODE IS PROVIDED ON AN “AS IS” AND “AS AVAILABLE” BASIS FOR ILLUSTRATIVE PURPOSES ONLY. REFINITIV MAKES NO REPRESENTATIONS OR WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, AS TO THE OPERATION OF THE EXAMPLE CODE, OR THE INFORMATION, CONTENT, OR MATERIALS USED IN CONNECTION WITH THE EXAMPLE CODE. YOU EXPRESSLY AGREE THAT YOUR USE OF THE EXAMPLE CODE IS AT YOUR SOLE RISK.

## <a id="intro"></a>Introduction

Today, applications are bigger and more complex. A few changes to the source code to add more features or fix bugs can make unexpected behavior in an application. Developers cannot just wait for the test result from the QA team anymore. They need to do unit testing regularly as an integral part of the development process. 

Unit testing is a software testing method that helps developers verify if any changes break the code. Unit testing significantly improves code quality, saves time to find software bugs in an early stage of the development lifecycle, and improves deployment velocity. Unit testing is currently the main process of a modern Agile software development practice such as CI/CD (Continuous Integration/Continuous Delivery), TDD (Test-driven development), etc.

Modern applications also need to connect to other services like APIs, databases, data storage, etc. The unit testing needs to cover those modules too. This example project shows how to run unit test cases for a [Python](https://www.python.org/) application that performs HTTP REST operations which is the most basic task of today's application functionality. With unit testing, developers can verify if their code can connect and consume content via HTTP REST API in any code updates. 

The demo application uses a de-facto [Requests](https://requests.readthedocs.io/en/latest/) library to connect to the [Refinitiv Data Platform (RDP) APIs](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis) as the example HTTP REST APIs and uses the Python built-in [unittest](https://docs.python.org/3.9/library/unittest.html) as a test framework.

**Note**:
This demo project is not cover all test cases for the HTTP operations and all RDP APIs services. It aims to give the readers an idea about how to unit test an application that makes an HTTP connection with Python only. 

## Unit Testing Overview

[Unit testing](https://en.wikipedia.org/wiki/Unit_testing) is the smallest test that focuses on checking that a single part of the application operates correctly. It breaks an application into the smallest, isolated, testable component called *units*, and then tests them individually. The unit is mostly a function or method call or procedure in the application source code. Developers and QA can test each unit by sending any data into that unit and see if it functions as intended. 

A unit test helps developers to isolate what is broken in their application easier and faster than testing an entire system as a whole. It is the first level of testing done during the development process before integration testing. It is mostly done by the developers automated or manually to verify their code.

You can find more detail about the unit test concept from the following resources:
- [Python Guide: Testing Your Code](https://docs.python-guide.org/writing/tests/) article.
- [How and when to use Unit Testing properly](https://softwareengineering.stackexchange.com/questions/89064/how-and-when-to-use-unit-testing-properly) post.

## Introduction to Python Unittest framework

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

## <a id="testsuite_detail"></a>Test Suit Development Detail

Please see the full details over the test suite implementation on the [unittest-article.md](unittest-article.md) file.

## <a id="prerequisite"></a>Prerequisite

This demo project requires the following dependencies.

1. RDP Access credentials.
2. Python [Anaconda](https://www.anaconda.com/distribution/) or [MiniConda](https://docs.conda.io/en/latest/miniconda.html) distribution/package manager.
3. [Docker Desktop/Engine](https://docs.docker.com/get-docker/) application for running the test suite with Docker.
5. Internet connection.

Please contact your Refinitiv representative to help you to access the RDP account and services. You can find more detail regarding the RDP access credentials set up from the lease see the *Getting Started for User ID* section of the [Getting Start with Refinitiv Data Platform](https://developers.refinitiv.com/en/article-catalog/article/getting-start-with-refinitiv-data-platform) article.


## <a id="how_to_run"></a>How to run the example test suite

The first step is to unzip or download the example project folder into a directory of your choice, then set up Python or Docker environments based on your preference.

### <a id="python_example_run"></a>Run example test suite in a console

1. Open Anaconda Prompt and go to the project's folder.
2. Run the following command in the Anaconda Prompt application to create a Conda environment named *http_unittest* for the project.
    ```
    (base) $>conda create --name http_unittest python=3.9
    ```
3. Once the environment is created, activate a Conda *http_unittest* environment with this command in Anaconda Prompt.
    ```
    (base) $>conda activate http_unittest
    ```
4. Run the following command to the dependencies in the *http_unittest* environment 
    ```
    (http_unittest) $>pip install -r requirements.txt
    ```
5. Once the dependencies installation process success, Go to the project's *tests* folder, then run the following command to run the ```test_rdp_http_controller.py``` test suite.
    ```
    (http_unittest) $>tests\python -m unittest test_rdp_http_controller
    ```
6. To run all test suites (```test_rdp_http_controller.py`` and ```test_app.py``` files), run the following command in the project's *tests* folder.
    ```
    (http_unittest) $>tests\python -m unittest discover
    ```
Example Result:

```
(http_unittest) $>tests\python -m unittest test_rdp_http_controller

RDP authentication failure: 401 Unauthorized
Text: {"error": "invalid_client", "error_description": "Invalid Application Credential."}
..Authentication success
.Authentication success
.Receive ESG Data from RDP APIs
.Receive ESG Data from RDP APIs
..RDP APIs: ESG data request failure: 401 Unauthorized
Text: {"error": {"id": "XXXXXXXXXX", "code": "401", "message": "token expired", "status": "Unauthorized"}}
.Receive Search Explore Data from RDP APIs
.RDP APIs: Search Explore request failure: 400 Bad Request
Text: {"error": {"id": "00000000-0000-0000-0000-000000000000", "code": "400", "message": "Validation error", "status": "Bad Request", "errors": [{"key": "json", "reason": "json.View in body should be one of [CatalogItems Entities]"}]}}
.Receive Search Explore Data from RDP APIs
..RDP APIs: Search Explore request failure: 401 Unauthorized
Text: {"error": {"id": "XXXXXXXXXX", "code": "401", "message": "token expired", "status": "Unauthorized"}}
.
----------------------------------------------------------------------
Ran 13 tests in 0.031s

OK
```

### <a id="docker_example_run"></a>Run example test suite in Docker

1. Start Docker
2. Open a console, then go to the *project root* and run the following command to build a Docker image.
    ```
    $> docker build . -t python_unittest
    ```
3. Run a Docker container with the following command: 
    ```
    $> docker run -it --name python_unittest python_unittest
    ```
4. To stop and delete a Docker container, press ``` Ctrl+C``` (or run ```docker stop python_unittest```) then run the following command:
    ```
    $> docker rm python_unittest
    ```



That covers how to run an example test suite.

## <a id="summary"></a>Conclusion and Next Steps

Unit testing is now the mandatory process of a software development lifecycle for both modern and legacy applications. It helps to expose unintentional behaviors of a tiny part of the application quicker than trying to find bugs in a big complex phase. It speeds up the overall feedback loop and improves trust among the project team. Unit testing also helps improves application source code quality, developers have more confidence in refactoring the source code for better performance and cleaner code. As the author of this article, I also have learned a lot from this project. There are a lot of error handlers or code logic that I never think of until I started to write unit test cases. 

This example project demonstrates the manual unit testing method. However, developers should run unit test cases automatically every time they made changes to the code (or configurations). The most practical technique is running automated unit tests as part of the developers' Continuous Integration/Continuous Delivery (CI/CD) pipeline. Developers can apply the TDD (Test-driven development) practice that writing and correcting the failed tests before writing new code with their project too.

The [unittest](https://docs.python.org/3.9/library/unittest.html) framework and [Responses](https://github.com/getsentry/responses) mocking library are very good starting points to learn a unit test with [Python](https://www.python.org/) and build a simple test suite to test HTTP operations source code. If developers need more advanced features, they can explore other Python unit test frameworks such as [pytest](https://docs.pytest.org/en/7.1.x/), [nose2](https://github.com/nose-devs/nose2), or [doctest](https://github.com/doctest/doctest).

At the same time, the [Refinitiv Data Platform (RDP) APIs](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis) provide various Refinitiv data and content for developers via an easy-to-use Web-based API. The APIs are easy to integrate into any application and platform that supports the HTTP protocol and JSON message format. 


## <a id="references"></a>References

That brings me to the end of my unit test example project. For further details, please check out the following resources:
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

