import math


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


class RestLink:
    def __init__(self, name:str, url:str):
        self.name = name
        self.url = url

    def __json__(self):
        return {
            "name": self.name,
            "url": self.url,
        }


class RestPagination :
    def __init__(self, per_page:int, page:int, total_items:int, total_pages:int|None, links):
        self.per_page = per_page
        self.page = page
        self.total_items = total_items
        self.total_pages = total_pages if total_pages != None else math.ceil(total_items / per_page)
        self.links = links

    def __json__(self):
        return {
            "perPage": self.per_page,
            "currentPage": self.page,
            "totalItems": self.total_items,
            "totalPages": self.total_pages,
            "links": self.links,
        }
    


class RestMeta :
    def __init__(self, pagination:RestPagination|None):
        self.pagination = pagination


    def __json__(self):
        return {
            "pagination": self.pagination,
        }



class RestResponse :
    def __init__(self, status:RestStatus|None=None, meta:RestMeta|None=None, data:any=None):
        self.status = status if status != None else RestStatus()
        self.meta = meta
        self.data = data


    def __json__(self):
        return {
            "status": self.status,
            "meta": self.meta,
            "data": self.data
        }    


'''
Д.З. Реалізувати статичні поля RestStatus для стандартних
HTTP-кодів. У starter.py підібрати правильні статуси для 
помилкових ситуацій
'''