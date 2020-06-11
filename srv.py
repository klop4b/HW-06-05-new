import os
import socketserver
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime


PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")

def create_page(raw_path):
    path, qs = raw_path.split("?") if '?' in raw_path else [raw_path, ""]

    paths = {
        '/hello': say_hello,
        '/goodbye': say_goodbye,
        }

    return paths[path](qs)

def say_hello(qs):
    print(qs)

    qs = parse_qs(qs)
    print("get_name: ")
    print(qs)
    return f"""
                    Hello {get_name(qs)}!
                    You were born in {get_year(qs)} year
                    Your path: /hello
                     """

def say_goodbye(qs):
    return say_bye(datetime.now().hour)

def get_name(qs):
    if 'name' in qs:
        print("get_name: ")
        print(qs)
        return qs["name"][0]
    else:
        return "Anonymous"

def get_year(qs):
    if 'age' in qs:
        print("get age: ")
        print(qs)
        return str(datetime.now().year - int(qs['age'][0]))
    else:
        return 'the best'


def say_bye(hour):
    if hour in range(13):
        return "Goodbye!"
    else:
        return "Goodnight!"

#def empty_path():
#    return SimpleHTTPRequestHandler.do_GET(MyHandler)

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        msg = create_page(self.path)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", len(msg))
        self.end_headers()

        self.wfile.write(msg.encode())


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it works")
    httpd.serve_forever()

