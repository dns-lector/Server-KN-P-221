from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# plus_encoded_string = 'My+name+is+John'
# decoded_with_unquote = urllib.parse.unquote(plus_encoded_string)
# decoded_with_unquote_plus = urllib.parse.unquote_plus(plus_encoded_string)
def url_decode(input:str|None) -> str|None :
     return None if input is None else urllib.parse.unquote_plus(input)


class RequestHandler(BaseHTTPRequestHandler) :
    def do_GET(self) :        # https://uk.wikipedia.org/wiki/%D0%A3%D0%BD%D1%96%D1%84%D1%96%D0%BA%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B9_%D0%BB%D0%BE%D0%BA%D0%B0%D1%82%D0%BE%D1%80_%D1%80%D0%B5%D1%81%D1%83%D1%80%D1%81%D1%96%D0%B2
        print(self.path)      # /user/auth?hash=1a2d==&p=50/50&q=who?&x=10&y=20&x=30&json -- повний шлях + параметри
        print(self.command)   # GET
        # print(self.request)  -- socket
        # Маршрутизація за різними підходами
        # MVC: /controller/action/id?
        # API: METHOD /service/section?
        parts = self.path.split('?', 1)
        path = parts[0]  # /user/auth
        query_string = parts[1] if len(parts) > 1 else ""  # hash=1a2d==&p=50/50&q=who?&&x=10&y=20&x=30&json
        # розібрати параметри запиту, очікуваний рез-т: {"hash": "1a2d==", "p": "50/50", "q":"who?", x: [10, 30], y: 20, json: None}
        query_params = {}        
        for key, value in ( map(url_decode, (item.split('=', 1) if '=' in item else [item, None])) 
            for item in query_string.split('&') if len(item) > 0 ) :
                query_params[key] = value if not key in query_params  else  [
                    *(query_params[key] if isinstance(query_params[key], (list, tuple)) else [query_params[key]]), 
                    value
                ]
                
        self.send_response(200, "OK")
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"""<h1>HTTP</h1>
        self.path = {self.path}<br/>   
        path = {path}<br/>   
        query_string = {query_string}<br/>   
        query_params = {query_params}<br/>   
        """.encode())



def main() :
    host = '127.0.0.1'
    port = 8080
    endpoint = (host, port)
    http_server = HTTPServer(endpoint, RequestHandler)
    try :
        print(f"Try start server http://{host}:{port}")
        http_server.serve_forever()
    except :
        print("Server stopped")


if __name__ == '__main__' :
    main()


'''
Модуль НТТР
Альтернативний до CGI підхід у створенні серверних застосунків
полягає у створенні власного (програмного)
сервера, що є частиною загального проєкту.
+ використовуємо єдину мову програмування (непотрібна конфігурація
   стороннього сервера окремою мовою)
+ уніфікуються ліцензійні умови
- дотримання стандартів і протоколів перекладається на проєкт
- частіше за все, програмні сервери більш повільні і не сертифіковані
- необхідність перезапуску сервера після внесення змін до скриптів

У Python такі засоби надає пакет http.server:
HTTPServer - клас управління сервером (слухання порту, прийом запитів), 
BaseHTTPRequestHandler - продовження оброблення, формування відповіді

У результаті досліджень з'ясовуємо
- на кожен запит утворюється новий об'єкт класу RequestHandler
- print виводить на консоль запуску, а не до відповіді сервера
- path відповідає за повний шлях запиту + параметри (query string)
- command відповідає за методи запиту
- маршрутизація не здійснюється

MVC                                            API
GET  /user/auth    | один                    GET  /user/auth    | різні 
POST /user/auth    | обробник                POST /user/auth    | обробники     
GET  /user/profile - інший обробник          GET  /user/profile - той самий, що й для GET  /user/auth       
'''

        # if query_string != None :
        #     for item in query_string.split('&') :
        #         if len(item) == 0 : continue
        #         key, value = item.split('=', 1) if '=' in item else [item, None]
        #         query_params[key] = value if not key in query_params  else  [
        #             *(query_params[key] if isinstance(query_params[key], (list, tuple)) else [query_params[key]]), 
        #             value
        #         ]

        # if query_string != None :
        #     for item in query_string.split('&') :
        #         if len(item) == 0 : continue
        #         parts = item.split('=', 1)
        #         key = parts[0]
        #         value = parts[1] if len(parts) > 1 else None
        #         query_params[key] = value if not key in query_params  else  [
        #             *(query_params[key] if isinstance(query_params[key], (list, tuple)) else [query_params[key]]), 
        #             value
        #         ]            

'''
Д.З. Додати на сайт (стартову сторінку) декілька посилань на цю ж адресу для 
випробування алгоритму розділення параметрів:
- посилання без параметрів (/user/auth)
- посилання без параметрів але з ? (/user/auth?)
- посилання з параметрами, у т.ч. повторами ключів (/user/auth?hash=1a2d==&p=50/50&q=who?&x=10&y=20&x=30&json)
- посилання з URL-кодованими ключами та значеннями (?hash=1a2d==&p=50/50&q=who?&&x=10&y=20&x=30&json&url=%D0%A3%D0%BD%D1%96%D1%84%D1%96%D0%BA%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B9&%D0%BB%D0%BE%D0%BA%D0%B0%D1%82%D0%BE%D1%80=%D1%80%D0%B5%D1%81%D1%83%D1%80%D1%81%D1%96%D0%B2&2+2=4)
'''