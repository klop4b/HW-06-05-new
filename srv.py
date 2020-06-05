import os
import socketserver
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime


PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/hello") and self.path.find('name') != -1 and self.path.find('age') != -1:
            path, name, age = self.path.split("?")
            name = parse_qs(name)
            age = parse_qs(age)
            name = name["name"][0]
            age = age["age"][0]
            year = datetime.now().year - int(age)
            born = 'You were born in ' + str(year) + ' year'

            msg = f"""
                            Hello {name}!
                            {born}
                            Your path: {path}
                        """

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg.encode())

        elif self.path.startswith("/hello") and self.path.find('name') != -1 and self.path.find('age') == -1:
            path, name = self.path.split("?")
            name = parse_qs(name)
            name = name["name"][0]


            msg = f"""
                                        Hello {name}!
                                        Your path: {path}
                                    """

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg.encode())

        elif self.path.endswith("/hello") or self.path.endswith("/hello/"):
            path = self.path.split("?")



            msg = f"""
                                                   Hello Anonymous!
                                                   Your path: {path}
                                               """

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg.encode())


        else:
            return SimpleHTTPRequestHandler.do_GET(self)




with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it works")
    httpd.serve_forever()

