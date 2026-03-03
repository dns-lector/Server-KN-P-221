from http.server import BaseHTTPRequestHandler
from controllers.controller_rest import ControllerRest


class UserController(ControllerRest) :
    def __init__(self, handler:BaseHTTPRequestHandler):
        super().__init__(handler)


    def do_GET(self) :        
        self.rest_response.data = {
            "x": 10,
            "y": 20,
            "w": 30,
            "t": "Вітання"
        }
'''
Д.З. Включити до self.rest_response.data UserController
відомості про 
- query_string
- api параметри
'''

        
