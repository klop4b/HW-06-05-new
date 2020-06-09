import os
import socketserver
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime


PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")

def get_name(qs):
    if qs =="":
        return "Anonymous"
    elif qs.find('name') != -1:
        qs = parse_qs(qs)
        return qs["name"][0]
    else:
        return "Anonymous"

def get_age(qs):
    if qs == "":
        return "\\t"
    elif qs.find('age') != -1:
        qs = parse_qs(qs)
        return int(qs["age"][0])
    else:
        return "\\t"

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/hello") and self.path.find('name') != -1 and self.path.find('age')  != -1:
            path, qs = self.path.split("?")
            print(qs)
            age = str(datetime.now().year - get_age(qs))
            msg = f"""
                            Hello {get_name(qs)}!
                            You were born in {age} year
                            Your path: {path}
                        """



        elif self.path.startswith("/hello") and self.path.find('name') != -1 and self.path.find('age') == -1:
            path, qs = self.path.split("?")

            msg = f"""
                    Hello {get_name(qs)}!
                    Your path: {path}
                    """

        elif self.path.endswith("/hello") or self.path.endswith("/hello/"):

            msg = f"""
                    Hello Anonymous!
                    Your path: {self.path}
                    """

        else:
            return SimpleHTTPRequestHandler.do_GET(self)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", str(len(msg)))
        self.end_headers()
        self.wfile.write(msg.encode())


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it works")
    httpd.serve_forever()

