class RestStatus:
    def __init__(self, is_ok:bool=True, code:int=200, phrase:str="OK"):
        self.is_ok  = is_ok
        self.code   = code
        self.phrase = phrase


    def __json__(self):
        return {
            "isOk": self.is_ok,
            "code": self.code,
            "phrase": self.phrase,
        }
RestStatus.no_found_404 = RestStatus(False, 404, "Not Found")
RestStatus.service_unavailable_503  = RestStatus(False, 503, "Service Unavailable")
'''
Д.З. Реалізувати статичні поля RestStatus для стандартних
HTTP-кодів. У starter.py підібрати правильні статуси для 
помилкових ситуацій
'''

class RestResponse :
    def __init__(self, status:RestStatus|None=None, data:any=None):
        self.status = status if status != None else RestStatus()
        self.data = data


    def __json__(self):
        return {
            "status": self.status,
            "data": self.data
        }    
