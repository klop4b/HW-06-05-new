import os
import socketserver
from http.server import SimpleHTTPRequestHandler
from typing import Dict
from urllib.parse import parse_qs
from datetime import datetime


PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path, *_qs = self.path.split("?") if '?' in self.path else [self.path, ""]
        print(path)


        handlers = {
            "/goodbye": self.say_goodbye,
            "/hello": self.say_hello,
            }

        default_handler = super().do_GET

        handler = handlers.get(path, default_handler)
        handler()

    def say_hello(self):
        args = self.build_query_args()
        name = self.get_name(args)
        year = self.get_year(args)

        print("method name: say_hello")
        print(f"value name: {name}")
        print(f"value args: {args}")

        msg = f"Hello {name}!"
        if year:
            msg += f"\nYou was born at {year}."
        print(msg)
        self.respond(msg)

    def say_goodbye(self):
        print("say_goodbye")
        if datetime.now().hour in range(13):
            msg = "Goodbye!"
        else:
            msg = "Goodnight!"
        self.respond(msg)

    def build_query_args(self) -> Dict:
        _path, *qs = self.path.split("?")
        args = {}

        if len(qs) != 1:
            return args

        qs = qs[0]
        qs = parse_qs(qs)

        for key, values in qs.items():
            if not values:
                continue
            args[key] = values[0]

        print(f"value: args/n {args}")
        print("args type:")
        print(type(args))
        return args

    def get_name(self, qs) -> str:
        return qs.get("name", "Anonymous")

    def get_year(self, qs) -> int:
        if 'age' in qs:
            print("method name: get age")
            print(f"value age: {qs['age'][0]}")

            return datetime.now().year - int(qs.get('age'))
        else:
            return 'the best'


    def extract_path(self) -> str:
        if self.path.find("hello"):
            return "/hello"
        elif self.path.find("goodbye"):
            return "/goodbye"
        else:
            return None

    def respond(self, msg: str) -> None:
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", len(msg))
        self.end_headers()

        self.wfile.write(msg.encode())

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it works")
    httpd.serve_forever()