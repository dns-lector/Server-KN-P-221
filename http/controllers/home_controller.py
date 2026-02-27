from http.server import BaseHTTPRequestHandler


class HomeController :
    def __init__(self, handler:BaseHTTPRequestHandler):
        self.handler = handler

    def do_GET(self) :        
        self.handler.send_response(200, "OK")
        self.handler.send_header("Content-Type", "text/html; charset=utf-8")
        self.handler.end_headers()
        self.handler.wfile.write(f"""<h1>HTTP</h1>
        <img src="/img/Python.png" alt="logo" width=150 />
        <hr/>
        <button onclick="linkClick()">LINK</button>
        <p id=out></p>
        <script>
            function linkClick() {{
                fetch("/", {{
                    method: "LINK"
                }}).then(r => r.text()).then(t => out.innerText = t);
            }}
        </script>
        """.encode())


    def do_LINK(self) :
        self.handler.send_response(200, "OK")
        self.handler.send_header("Content-Type", "text/plain; charset=utf-8")
        self.handler.end_headers()
        self.handler.wfile.write("LINK method response".encode())    