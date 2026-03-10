import math

from controllers.controller_rest import ControllerRest
from controllers.rest_error import RestError
from controllers.rest_response import RestLink, RestMeta, RestPagination

products = [
    {"id": 1,  "name": "Product 1",  "price": 91.50 },
    {"id": 2,  "name": "Product 2",  "price": 92.50 },
    {"id": 3,  "name": "Product 3",  "price": 93.50 },
    {"id": 4,  "name": "Product 4",  "price": 94.50 },
    {"id": 5,  "name": "Product 5",  "price": 95.50 },
    {"id": 6,  "name": "Product 6",  "price": 96.50 },
    {"id": 7,  "name": "Product 7",  "price": 97.50 },
    {"id": 8,  "name": "Product 8",  "price": 98.50 },
    {"id": 9,  "name": "Product 9",  "price": 99.50 },
    {"id": 10, "name": "Product 10", "price": 100.50},
    {"id": 11, "name": "Product 11", "price": 110.50},
    {"id": 12, "name": "Product 12", "price": 120.50},
]

class ProductController(ControllerRest) :
    def do_GET(self) :
        # pagination
        # - total items
        # - items per page
        # - total pages
        # - page number
        total_items = len(products)   # SELECT COUNT(*) FROM Products WHERE filter(s)
        per_page = self.query_params.get('perpage', 5)   # default 5
        if not isinstance(per_page, int) :
            try :
                per_page = int(per_page)
            except :
                per_page = 0

        if per_page <= 0 :
            raise RestError(code=400, phrase="Bad Request", 
                            data="Pagination error: perpage is not valid (positive number expected)")
        
        total_pages = math.ceil(total_items / per_page)

        page = self.query_params.get('page', 1)  # default 1, not greater than total_pages
        if not isinstance(page, int) :
            try :
                page = int(page)
            except :
                page = 0
        if page <= 0 or page > total_pages :
            raise RestError(code=400, phrase="Bad Request", 
                            data=f"Pagination error: page is not valid, must be in range (1 - {total_pages})")

        self.rest_response.meta = RestMeta(pagination=RestPagination(
            page=page,total_items=total_items,per_page=per_page,total_pages=total_pages,
            links=[
                RestLink("1", f"?perpage={per_page}"),
                RestLink(str(total_pages), f"?page={total_pages}&perpage={per_page}"),
                RestLink(str(page + 1), f"?page={page + 1}&perpage={per_page}" if page < total_pages else None),
                RestLink(str(page - 1), f"?page={page - 1}&perpage={per_page}" if page > 1 else None),
            ]
        ))
        # Д.З. Розширити метадані RestPagination: включити відмості про наявність/відсутність
        # посилань на попередню та наступну сторінки. Реалізувати вибірку товарів за даними пагінації

'''
{
    "prev": "url",
    "1": "url",
    "...": null,
    "5": "url",
    "6": null,
    "7": "url",
    "...": null,
    "112": "url",
    "next": "url"
}
'''