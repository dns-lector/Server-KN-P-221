from models.request import CgiRequest
import datetime, io, json, sys

class RestStatus :
    def __init__(self, is_ok:bool, code:int, message:str) :
        self.is_ok = is_ok
        self.code = code
        self.message = message

    def to_json(self) :
        return {
            "isOk": self.is_ok,
            "code": self.code,
            "message": self.message,
        }

RestStatus.status200 = RestStatus(True,  200, "OK")        
RestStatus.status405 = RestStatus(False, 405, "Method Not Allowed")



class RestCache :
    def __init__(self, exp:str|int|None=None, lifetime:int|None=None):
        self.exp = exp
        self.lifetime = lifetime
        
    def to_json(self) :
        return {
            "exp": self.exp,
            "lifetime": self.lifetime,
            "units": "seconds",
        }

RestCache.no = RestCache()
RestCache.hrs1 = RestCache(lifetime=60*60)



class RestMeta :
    def __init__(self, service:str, requestMethod:str,  dataType:str="null",
                 cache:RestCache=RestCache.no, authUserId:str|int|None=None,
                 serverTime:int|None=None, params:dict|None=None, links:dict|None=None):
        self.service = service
        self.requestMethod = requestMethod
        self.authUserId = authUserId
        self.dataType = dataType
        self.cache = cache
        self.serverTime = serverTime if serverTime != None else datetime.datetime.now().timestamp()
        self.params = params
        self.links = links
        
    def to_json(self) :
        return {
            "service": self.service,
            "requestMethod": self.requestMethod,
            "dataType": self.dataType,
            "cache": self.cache.to_json(),
            "serverTime": self.serverTime,
            "params": self.params,
            "links": self.links,
            "authUserId": self.authUserId,
        }



class RestResponse :
    def __init__(self, 
                 meta:RestMeta,
                 status:RestStatus=RestStatus.status200,
                 data:any=None):
        self.status = status
        self.meta = meta
        self.data = data
        
    def to_json(self) :
        return {
            "status": self.status,
            "meta": self.meta,
            "data": self.data,
        }



class UserController :

    def __init__(self, request:CgiRequest):
        self.request = request


    def serve(self) :
        # формуємо REST відповідь
        self.response = RestResponse(
            meta=RestMeta(
                service="User API",
                requestMethod=self.request.request_method,
                links={
                    "get": "GET /user",
                    "post": "POST /user",
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


    def do_post(self) :
        self.response.meta.service += ": registration"
        self.response.meta.dataType = "object"
        self.response.data = {
            "int": 10,
            "float": 1e-3,
            "str": "POST",
            "cyr": "Вітання",
            "headers": self.request.headers
        }

'''
Д.З. Реалізувати відповіді API /order (попереднє ДЗ) у формалізмі REST
Додати скріншоти результатів роботи
'''

'''
REST
Layered system – A client cannot ordinarily tell whether it is connected directly to the end server, or to an intermediary along the way
Client      Server                     Client      Server          
GET -------->                          GET -------->     
       time:1234760123                        404                   
Data <------ Response                  Data <------ Response             

Client      Proxy      Server          Client      Proxy      Server           
GET ----->  GET ----->                 GET ----->  GET ----->    
    time:1234    time:1233                    500        404              
Data <-----     <----- Response        Data <-----     <----- Response       

Рішення: розділення статусів проходження запиту та статусів оброблення запиту
Client      Proxy      Server    
GET ----->  GET ----->    
    200{404}      200{404}            
Data <-----     <----- Response  

Поєднуючи усі вимоги, можна дати пропозицію 
response: 
{
    status: {
        message: "Conflict",
        code: 409,
        isOk: false
    },
    meta: {
        service: "Shop API: Add new product",
        requestMethod: "POST",
        serverTime: 1021394671221,
        cache: {
            exp: "2025-12-12 10:00:00", | 1021394673456
            lifetime: 100500,
        },
        authUserId: "1021394671221",
        params: {
            id: 123,
            content: "New Item"
        },
        links: {
            "create": "POST /product/{id}",
            "read": "GET /product/{id}",
            "update": "PATCH /product/{id}",
            "delete": "DELETE /product/{id}",
        },
        dataType: "string"
    },
    data: "Item with ID given is already exist"
}
'''