from models.request import CgiRequest


class HomeController :

    def __init__(self, request:CgiRequest):
        self.request = request


    def serve(self) :        
        # шукаємо в об'єкті метод action та виконуємо його
        action = (self.request.path_parts[1].lower() 
                  if len(self.request.path_parts) > 1 
                    and len(self.request.path_parts[1].strip()) > 0 
                  else 'index')
        # print("parts=", self.request.path_parts)
        # print("action=", action)
        controller_action = getattr(self, action)
        controller_action()


    def privacy(self) :
        html = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AM-CGI</title>
            <link rel="icon" href="/img/python.png" />
            <link rel="stylesheet" href="/css/site.css" />
        </head>
        <body>
        <h1>Політика конфіденційності</h1>
        <p>
            Згідно з принципів CGI всі параметри від сервера (Apache) до скрипту
            передаються як змінні оточення.
        <p>
        </body>
        </html>
        """
        print("Content-Type: text/html; charset=utf-8")
        print()
        print(html)


    def index(self) :        
        envs = "<ul>\n" + "".join(f"<li>{k} = {v}</li>\n" for k,v in self.request.server.items()) + "</ul>\n"
        hdrs = "<ul>\n" + "".join(f"<li>{k} = {v}</li>\n" for k,v in self.request.headers.items()) + "</ul>\n"
        qp = "<ul>\n" + "".join(f"<li>{k} = {v}</li>\n" for k,v in self.request.query_params.items()) + "</ul>\n"
        
        with open("./views/_layout.html", mode="rt", encoding="utf-8") as file :
            layout = file.read()

        with open("./views/home_index.html", mode="rt", encoding="utf-8") as file :
            body = file.read()

        html = layout.replace("<!-- RenderBody -->", 
            (body
                .replace("{envs}", envs)    
                .replace("{hdrs}", hdrs)    
                .replace("{qp}", qp))    
        )

        print("Content-Type: text/html; utf-8")
        print()
        print(html)


'''
Д.З. Додати до головного контролера метод params, який візьме на себе
відображення таблиці з усіма параметрами, що передаються від 
диспетчера доступу.
На головній сторінці (Index) залишити лише посилання на інші сторінки
'''