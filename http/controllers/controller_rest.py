from http.server import BaseHTTPRequestHandler
from controllers.rest_response import RestResponse, RestStatus
from controllers.rest_error import RestError
import urllib.parse


class ControllerRest :   # з метою уникнення адреси /rest змінюємо правило іменування
    def __init__(self, handler:BaseHTTPRequestHandler):
        self.handler = handler        


    def before_execution(self):
        self.rest_response = RestResponse()


    def serve(self):   # Основний метод запуску контролера, який забезпечить життєвий цикл запиту
        # розібрати параметри запиту, очікуваний рез-т: {"hash": "1a2d==", "p": "50/50", "q":"who?", x: [10, 30], y: 20, json: None}
        self.query_params = {}
        for key, value in ( map(lambda input : None if input is None else urllib.parse.unquote_plus(input), 
                                (item.split('=', 1) if '=' in item else [item, None])) 
            for item in self.handler.query_string.split('&') if len(item) > 0 ) :
                self.query_params[key] = value if not key in self.query_params  else  [
                    *(self.query_params[key] if isinstance(self.query_params[key], (list, tuple)) else [self.query_params[key]]), 
                    value
                ]
        self.before_execution()
        mname = 'do_' + self.handler.command
        if not hasattr(self, mname):
            self.rest_response.status = RestStatus(
                is_ok = False,
                code = 405,
                phrase = "Unsupported method (%r) in '%r'" % (self.handler.command, self.__class__.__name__)
            )
        else :
            method = getattr(self, mname)
            try :
                method()
                self.send_success()
                return
            except RestError as err:
                self.rest_response.status = RestStatus(
                    is_ok = False,
                    code = err.code,
                    phrase = err.phrase)
                self.rest_response.data = err.data
            except Exception as ex:
                # print(str(ex))
                self.rest_response.status = RestStatus(
                    is_ok = False,
                    code = 500,
                    phrase = "Request processing error " + str(ex)
                )
        self.send_error()


    def send_success(self):
        self.handler.send_rest_response(self.rest_response)

        
    def send_error(self):
        self.handler.send_rest_response(self.rest_response)



