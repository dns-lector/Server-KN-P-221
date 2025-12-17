from models.request import CgiRequest
import io, sys


class UsertestController :

    def __init__(self, request:CgiRequest):
        self.request = request


    def serve(self) :    
        # шукаємо в об'єкті метод action та виконуємо його
        action = (self.request.path_parts[1].lower() 
                  if len(self.request.path_parts) > 1 
                    and len(self.request.path_parts[1].strip()) > 0 
                  else 'index')
        controller_action = getattr(self, action)
        controller_action()


    def index(self) :        
        with open("./views/_layout.html", mode="rt", encoding="utf-8") as file :
            layout = file.read()

        with open("./views/usertest_index.html", mode="rt", encoding="utf-8") as file :
            body = file.read()

        print("Content-Type: text/html; charset=utf-8\n")
        print( layout.replace("<!-- RenderBody -->", body) )
