import os
import socketserver
from datetime import datetime
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from typing import Dict
from urllib.parse import parse_qs

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")

PROJECT_DIR = Path(__file__).parent.resolve()
print(f"PROJECT_DIR = {PROJECT_DIR}")

TEMPLATES_DIR = PROJECT_DIR / "templates"
print(f"TEMPLATES_DIR = {TEMPLATES_DIR}")

class NotFound(Exception):
    pass

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path, *_qs = self.path.split("?") if '?' in self.path else [self.path, ""]
        print(path)

        handlers = {
            "/goodbye": self.say_goodbye,
            "/hello": self.say_hello,
            "/projects": self.show_projects,
            "/resume": self.show_resume,
        }

        default_handler = super().do_GET

        handler = handlers.get(path, default_handler)

        try:
            handler()
        except NotFound:
            print("NotFound")
            self.respond_404()

    def show_projects(self) -> None:
        html = TEMPLATES_DIR / "projects" / "index.html"
        contents = self.get_file_contents(html)

        print("method name: show_projects")
        print(f"value html: {html}")

        self.respond(contents, "text/html")

    def show_resume(self) -> None:
        html = TEMPLATES_DIR / "resume" / "index.html"
        contents = self.get_file_contents(html)

        print("method name: show_resume")
        print(f"value html: {html}")

        self.respond(contents, "text/html")

    def get_file_contents(self, fp: Path) -> str:
        print("method name: get_file_contents")
        print(f"value fp: {fp}")


        if not fp.is_file():
            raise NotFound

        with fp.open("r") as src:
            ct = src.read()

        print(f"value contents: {ct}")


        return ct

    def say_hello(self) -> None:
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

    def say_goodbye(self) -> None:
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

    def respond(self, msg: str, сontent_type="text/plain") -> None:
        self.send_response(200)
        self.send_header("Content-type", сontent_type)
        self.send_header("Content-length", len(msg))
        self.end_headers()

        self.wfile.write(msg.encode())

    def respond_404(self) -> None:
        msg = "Ooops! Nothing found!"
        self.send_response(404)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", str(len(msg)))
        self.end_headers()

        self.wfile.write(msg.encode())


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it works")
    httpd.serve_forever()
