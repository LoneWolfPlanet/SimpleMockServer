# Standard library imports...
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
import socket
from threading import Thread
import json
import os
from urllib.parse import urlparse, parse_qs

# Third-party imports...
import requests


class MockServerRequestHandler(BaseHTTPRequestHandler):
    API100_PATTERN = re.compile(r'/API100') #AUTHENTICATION FOR OPERATOR CREDENTIALS
    API200_PATTERN = re.compile(r'/API200') #GET RAW DATA
    API300_PATTERN = re.compile(r'/API300')  #GET SHAPED DATA
    API400_PATTERN = re.compile(r'/API400')  # POST
    API500_PATTERN = re.compile(r'/API500')  # DELETE
    API600_PATTERN = re.compile(r'/API600')  # PUT

    '''
    ///////////////////////////////////////////////////////////////
    ////Override DELETE method
    //////////////////////////////////////////////////////////////
    '''
    def do_DELETE(self):
        if re.search(self.API500_PATTERN, self.path):
            print('Delete success')
            return

    '''
    //////////////////////////////////////////////////////////////
    ////Override the PUT method
    /////////////////////////////////////////////////////////////
    '''
    def do_PUT(self):
        if re.search(self.API600_PATTERN, self.path):
            print('PUT success')
            return
    '''
    /////////////////////////////////////////////////////////////
    /////// Override the POST method
    ////////////////////////////////////////////////////////////
    '''
    def do_POST(self):
        if re.search(self.API400_PATTERN, self.path):
            self.send_response(requests.codes.ok)

            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            response_content = json.dumps(["Test Post"])

            self.wfile.write(response_content.encode('utf-8'))

    '''
    //////////////////////////////////////////////////////////
    ////get the field in the url query string
    /////////////////////////////////////////////////////////
    '''
    def get_query_field(self,url, field):
        try:
            return parse_qs(urlparse(url).query)[field]
        except KeyError:
            return []

    '''
    ///////////////////////////////////////////////////////
    ///Override the HTTP get method
    /////////////////////////////////////////////////////
    '''
    def do_GET(self , payload= None):
        username = self.get_query_field(self.path, 'userName')
        if re.search(self.API100_PATTERN, self.path):
            # Add response status code.
            self.send_response(requests.codes.ok)

            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            response_content = None
            try:
                path = os.getcwd()
                with open('./tests/test_data/success01.json' , encoding="utf-8") as json_file:
                    data = json.load(json_file)
                    response_content = json.dumps(data , ensure_ascii=False)
            except Exception as e:
                print(str(e))
            if response_content:
                self.wfile.write(response_content.encode('utf-8'))
            return
        elif re.search(self.API200_PATTERN, self.path):
            # Add response status code.
            self.send_response(requests.codes.ok)

            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            response_content = None
            try:
                path = os.getcwd()
                with open('./tests/test_data/success02.json' , encoding="utf-8") as json_file:
                    data = json.load(json_file)
                    response_content = json.dumps(data , ensure_ascii=False)
            except Exception as e:
                print(str(e))
            if response_content:
                self.wfile.write(response_content.encode('utf-8'))
            return
        elif re.search(self.API300_PATTERN, self.path):
            # Add response status code.
            self.send_response(requests.codes.ok)

            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            response_content = None
            try:
                path = os.getcwd()
                with open('./tests/test_data/success03.json' , encoding="utf-8") as json_file:
                    data = json.load(json_file)
                    response_content = json.dumps(data , ensure_ascii=False)
            except Exception as e:
                print(str(e))
            if response_content:
                self.wfile.write(response_content.encode('utf-8'))
            return

def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port):
    mock_server = HTTPServer(('localhost', port), MockServerRequestHandler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()