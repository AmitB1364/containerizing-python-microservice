import http.server
import socketserver
import urllib.request

PORT = 8091
SERVER_URL = "http://server:8090/"

class ClientHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with urllib.request.urlopen(SERVER_URL) as fp:
                server_html = fp.read().decode("utf8")
        except Exception as e:
            server_html = f"<p style='color:red;'>Error reaching server: {e}</p>"

        with open("template.html", "r", encoding="utf8") as f:
            page = f.read().replace("{{SERVER_CONTENT}}", server_html)

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(page.encode("utf8"))

with socketserver.TCPServer(("", PORT), ClientHandler) as httpd:
    print(f"Client web UI running on port {PORT}...")
    httpd.serve_forever()
