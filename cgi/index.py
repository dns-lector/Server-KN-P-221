#!C:/Python/Python313/python.exe

import os

envs = "<ul>\n" + "".join(f"<li>{k} = {v}</li>\n" for k,v in os.environ.items()) + "</ul>\n"

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="windows-1251">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Py-CGI</title>
    <link rel="icon" href="/python.png" />
</head>
<body>
<h1>Змінні оточення</h1>
<p>
    Згідно з принципів CGI всі параметри від сервера (Apache) до скрипту
    передаються як змінні оточення.
<p>
{envs}
</body>
</html>
"""

print("Content-Type: text/html; charset=cp1251")
# print(f"Content-Length: {len(html)}")
print()
print(html)

'''
Д.З. Реалізувати виведення параметрів оточення у вигляді HTML-таблиці 
Забезпечити сортування параметрів за абеткою (по ключу - імені параметра)
'''