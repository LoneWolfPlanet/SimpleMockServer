from flask import Flask
from initialize import *
from mock.mock_server import  *

if __name__ == '__main__':

   app = create_app()
   app.run(debug = True)

