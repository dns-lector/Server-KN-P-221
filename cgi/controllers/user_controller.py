from controllers.controller_rest import RestController, RestMeta, RestStatus, RestCache
import base64, binascii, re, datetime, helper
from dao.data_accessor import DataAccessor

class UserController(RestController) :

    def serve(self) :
        # формуємо REST відповідь
        self.response.meta=RestMeta(
            service="User API",
            links={
                "get": "GET /user",
                "post": "POST /user",
            }
        )
        super().serve()
        

    def do_get(self) :
        self.response.meta.service += ": authentication"
        # Перевірити чи є заголовок 'Authorization' у запиті
        auth_header = self.request.headers.get('Authorization', None)
        if not auth_header :
            self.send_401("Missing required header 'Authorization'")
            return
        
        # Перевірити чи заголовок 'Authorization' має схему 'Basic'
        auth_scheme = 'Basic '
        if not auth_header.startswith(auth_scheme) :
            self.send_401(f"Invalid Authorization scheme: {auth_scheme} only")
            return
        
        credentials = auth_header[len(auth_scheme):]
        # Перевірити мінімальну валідність даних: base64 при логіні в 2 символи 
        #  і паролі в 1 символ буде мати довжину 7 символів
        if len(credentials) < 7 :
            self.send_401(f"{auth_scheme} credentials too short")
            return
        
        # Оскільки Python ігнорує символи, що не є base64, то їх наявність
        # ми контролюємо окремо, регулярними виразами
        match = re.search(r"[^a-zA-Z0-9+/=]", credentials)
        if match:
            self.send_401(f"Format error (invalid symbol) for credential: {credentials}")
            return

        user_pass = None
        try :
            user_pass = base64.standard_b64decode(credentials).decode(encoding="utf-8")
        except binascii.Error :
            self.send_401(f"Padding error for credential: {credentials}")
            return
        except Exception as err :
            self.send_401(f"Decode error '{err}' for credential: {credentials}")
            return

        if not user_pass :
            self.send_401(f"Decode error for credential: {credentials}")
            return
        
        if not ':' in user_pass :
            self.send_401(f"User-pass format error (missing ':') {user_pass}")
            return

        login, password = user_pass.split(':', 1)
        data_accessor = DataAccessor()
        user = data_accessor.authenticate(login, password)

        if not user :
            self.send_401(f"Credentials rejected")
            return
        
        self.response.meta.cache = RestCache.hrs1
        self.response.meta.dataType = "token"
        payload = {
            "sub": str(user['user_id']),
            "iss": "Server-KN-P-221",
            "aud": user['role_id'],
            "iat": datetime.datetime.now().timestamp(),
            "name": user['user_name'],
            "email": user['user_email'],
        }
        self.response.data = helper.compose_jwt( payload )


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
Д.З. Реалізувати тести (кнопки на сторінці /usertest) для помилкових даних автентифікації
- відсутній заголовок авторизації
- неправильна схема
- закороткі дані
- неправильні символи base64
* інші ситуації
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