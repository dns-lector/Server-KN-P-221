from controllers.controller_rest import ControllerRest
from controllers.rest_error import RestError


class UserController(ControllerRest) :

    def do_GET(self) :        
        self.rest_response.data = {
            "x": 10,
            "y": 20,
            "w": 30,
            "t": "Вітання"
        }

    def do_POST(self) :
        # Використання винятків як передачу даних про аварійне завершення  
        raise RestError(code=422, phrase="Unprocessable Entity", 
                        data="Invalid format for E-mail")
    
'''
Д.З. Включити до self.rest_response.data UserController
відомості про 
- query_string
- api параметри
'''

        
