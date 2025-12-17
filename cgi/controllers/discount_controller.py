from models.request import CgiRequest
import datetime, io, json, sys

class DiscountController :

    def __init__(self, request:CgiRequest):
        self.request = request


    def serve(self) :
        # формуємо REST відповідь
        self.response = RestResponse(
            meta=RestMeta(
                service="Discount API",
                requestMethod=self.request.request_method,
                links={
                    "get": "GET /discount",
                    "post": "POST /discount",
                }
            )
        )
        # шукаємо в об'єкті метод action та виконуємо його
        action = "do_" + self.request.request_method.lower() 
        controller_action = getattr(self, action, None)

        if controller_action :
            controller_action()
        else :
            self.response.status = RestStatus.status405

        sys.stdout.buffer.write(b"Content-Type: application/json; charset=utf-8\n\n")
        sys.stdout.buffer.write(
            json.dumps(
                self.response, 
                ensure_ascii=False,
                default=lambda x: x.to_json() if hasattr(x, 'to_json') else str
            ).encode())    


    def do_get(self) :
        self.response.meta.service += ": authentication"
        self.response.meta.cache = RestCache.hrs1
        self.response.meta.dataType = "object"
        self.response.data = {
            "int": 10,
            "float": 1e-3,
            "str": "GET",
            "cyr": "Вітання",
            "headers": self.request.headers
        }