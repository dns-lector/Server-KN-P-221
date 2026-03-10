from http.server import BaseHTTPRequestHandler
from controllers.controller_rest import ControllerRest


class HomeController(ControllerRest) :

    def do_GET(self) :        
        self.html = f"""<h1>HTTP</h1>
        <img src="/img/Python.png" alt="logo" width=150 />
        {self.query_params}
        <hr/>
        <button onclick="onClick('LINK')">LINK</button>
        <button onclick="onClick('POST')">POST</button>
        <button onclick="onClick('GET', 'user')">GET user</button>
        <button onclick="onClick('POST', 'user')">POST user</button>

        <button onclick="onClick('GET', 'no')">GET no module</button>
        <button onclick="onClick('GET', 'noclass')">GET no controller</button>
        <button onclick="onClick('GET', 'noinit')">GET no constructor</button>
        <button onclick="onClick('GET', 'noserve')">GET no serve method</button>
        <button onclick="onClick('GET', 'exserve')">GET exc in serve</button>
        <br/>
        <button onclick="onClick('GET', 'product')">GET product</button>
        <p id=out></p>
        <script>
            function onClick(method, service='') {{
                fetch(`/${{service}}`, {{
                    method: method
                }}).then(r => r.text()).then(t => out.innerText = t);
            }}
        </script>
        """
        self.content_type = "text/html; charset=utf-8"


    def do_LINK(self) :
        self.html = "LINK method response"
        self.content_type = "text/plain; charset=utf-8"


    def send_success(self):
        self.handler.send_response(200, "OK")
        self.handler.send_header("Content-Type", self.content_type)
        self.handler.end_headers()
        self.handler.wfile.write(self.html.encode())

'''
ТЗ: HomeController має спадкуватись від REST
у випадку помилки має повертатись JSON відповідь
у випадку успіху - тип, визначений контролером (text/plain чи text/html)
'''