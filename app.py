# app.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import os, mimetypes, urllib.parse

HOST = "127.0.0.1"
PORT = 8000
ROOT = os.getcwd()
CONTACTS = os.path.join(ROOT, "templates", "contacts.html")  # путь к contacts.html

class Handler(BaseHTTPRequestHandler):
    def send_file(self, full_path):
        """Send a file with guessed mime-type. Returns True on success."""
        if not os.path.isfile(full_path):
            return False
        ctype, _ = mimetypes.guess_type(full_path)
        if ctype is None:
            ctype = "application/octet-stream"
        # add charset for text types
        if ctype.startswith("text/"):
            self.send_header("Content-type", f"{ctype}; charset=utf-8")
        else:
            self.send_header("Content-type", ctype)
        self.end_headers()
        with open(full_path, "rb") as f:
            self.wfile.write(f.read())
        return True

    def do_GET(self):
        path = urllib.parse.unquote(self.path)
        # serve CSS/JS/images from /css, /js, /img etc
        if path.startswith("/css/") or path.startswith("/js/") or path.startswith("/img/"):
            fs_path = os.path.join(ROOT, path.lstrip("/"))
            if os.path.commonpath([os.path.abspath(fs_path), ROOT]) != os.path.abspath(ROOT):
                self.send_error(403)
                return
            if os.path.exists(fs_path) and os.path.isfile(fs_path):
                self.send_response(200)
                self.send_file(fs_path)
            else:
                self.send_error(404)
            return

        # Serve specific HTML files if requested (optional)
        # But per task: any GET -> contacts.html
        try:
            with open(CONTACTS, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(500, "contacts.html not found")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8", errors="replace")
        # печатаем данные в консоль — дополнительное задание
        print("=== POST DATA START ===")
        print(body)
        print("=== POST DATA END ===")
        # возвращаем страницу контактов
        self.do_GET()

if __name__ == "__main__":
    print(f"Server running at http://{HOST}:{PORT}")
    HTTPServer((HOST, PORT), Handler).serve_forever()
