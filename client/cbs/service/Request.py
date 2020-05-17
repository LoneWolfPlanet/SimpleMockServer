
import requests
import enum
from urllib.parse import urljoin
from unittest.mock import patch
# Third-party imports...
import requests
from service.service_route import *
from mock.mock_server import  *


# Local imports...
from constants import BASE_URL
USERS_URL = urljoin(BASE_URL, 'users')

'''
#Define the HTTP Response Status Code
#UNKNOWN -> unknown response
#INFORMATIONAL_RESPONSE (100 -199) -> the request is ongoing
#SUCCESFUL_RESPONSE(200-299) -> the request is succesful
#REDIRECT(300-399) -> for redirection request
#CLIENT_ERROR_RESPONSE(400-499) -> bad request
#SERVER_ERROR_RESPONSE(500-599) -> server encountered an error
'''
class ResponseStatusCode(enum.Enum):
    UNKNOWN = 0,
    INFORMATIONAL_RESPONSE = 1,
    SUCCESFUL_RESPONSE  = 2,
    REDIRECT = 3,
    CLIENT_ERROR_RESPONSE = 4,
    SERVER_ERROR_RESPONSE = 5

'''
Class Model for RESPONSE Data
'''
class Response():

    def __init__(self):
        self.status_code = ResponseStatusCode.UNKNOWN
        self.text = ''
        self.history = ''
        self.headers =  None
        self.data = None
'''
Static Methods for sending request
'''
class Request():

    mockStarted = False
    userPort = 0
    @staticmethod
    def startMock():
        if not Request.mockStarted:
            mock_server_port = get_free_port()
            start_mock_server(mock_server_port)
            Request.userPort = mock_server_port
            Request.mockStarted = True

    @staticmethod
    def parseResponse( resp):

        response = Response()
        if resp is None:
            return response

        if resp.status_code >= 100 and resp.status_code <= 199:
            response.status_code = ResponseStatusCode.INFORMATIONAL_RESPONSE
        elif resp.status_code >= 200 and resp.status_code <= 299:
            response.status_code = ResponseStatusCode.SUCCESFUL_RESPONSE
        elif resp.status_code >=300 and resp.status_code <= 399:
            response.status_code =ResponseStatusCode.REDIRECT
        elif resp.status_code >=400 and resp.status_code <= 499:
            response.status_code = ResponseStatusCode.CLIENT_ERROR_RESPONSE
        elif resp.status_code >= 500 and resp.status_code <= 599:
            response.status_code = ResponseStatusCode.SERVER_ERROR_RESPONSE

        try:
            response.text = resp.text
            response.data = resp.json()
            response.headers = resp.headers
        except Exception as e:
            pass
        return response


    @staticmethod
    def getMethod1( url):
        response = None
        try:
            mock_users_url = 'http://localhost:{port}/API300'.format(port=8000)
            # Patch USERS_URL so that the service uses the mock server URL instead of the real URL.
            with patch.dict('service.service_route.__dict__', {'USERS_URL': mock_users_url}):
                response = get_users()
        except Exception as e:
           print(str(e))
        return Request.parseResponse(response)

    @staticmethod
    def getMethod2(url, query):
        response = None
        try:
            response = requests.get(url, params=query)
            response.raise_for_status()
        except Exception as e:
            pass
        return Request.parseResponse(response)

    @staticmethod
    def getMethod3(url, query, headers):
        response = None
        try:
            response = requests.get(url,params=query, headers = headers)
            response.raise_for_status()
        except Exception as e:
            pass
        return Request.parseResponse(response)

    #tuple or dictionary
    def postMethod1(url, data):

           response = None
           try:
               response = requests.post(url, data = data)
               response.raise_for_status()
           except Exception as e:
               pass

           return Request.parseResponse(response)

    def postMethod2(url, json_data):
            response = None
            try:
                response = requests.post(url, json= json_data)
                response.raise_for_status()
            except Exception as e:
                pass
            return Request.parseResponse(response)



    



