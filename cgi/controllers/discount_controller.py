from controllers.controller_rest import RestController, RestMeta, RestStatus, RestCache
import helper, datetime

class DiscountController(RestController) :

    def serve(self) :
        # формуємо REST відповідь
        self.response.meta=RestMeta(
            service="Discount API",
            links={
                "bonuses": "GET /discount",
                "program": "GET /discount/program",
                "post": "POST /discount",
            }
        )
        super().serve() 


    def do_get(self) :
        # Відгалуження за адресою /program
        if len(self.request.path_parts) > 1 :
            if self.request.path_parts[1] == "program" :
                return self.get_program()               
        self.get_default()

        

    def get_default(self) :
        self.response.meta.service += ": User's bonuses"
        try :   # TODO: перенести до RestController::get_payload_or_exit 
            payload = helper.jwt_payload_from_request(self.request, True)
        except ValueError as err :
            self.send_401(str(err))
            return
        
        self.response.meta.cache = RestCache.hrs1
        self.response.meta.dataType = "object"
        self.response.data = payload


    def get_program(self) :        
        self.response.meta.service += ": Bonus program info"
        payload = helper.jwt_payload_from_request(self.request)
        
        self.response.meta.cache = RestCache.hrs1
        self.response.meta.dataType = "object"
        self.response.data = {
            "5%": "1000-10000",
            "10%": "10001-50000",
            "payload": payload
        }
    
'''
Д.З. Розширити внутрішню валідацію токенів:
- sub має бути, формат - UUID
- iss має бути, формат - "Server-KN-P-221"
- має бути хоча б одне з: name, email
* якщо є email, то правильного формату
'''