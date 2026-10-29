import http.server, urllib.request, json, os

PORT = int(os.environ.get("PORT", 8000))
NASA = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/exoplanet-explorer.html"):
            with open("exoplanet-explorer.html", "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path.startswith("/api/exo"):
            u = NASA + self.path[len("/api/exo"):]
            try:
                with urllib.request.urlopen(u, timeout=30) as r:
                    body, code = r.read(), r.status
            except Exception as e:
                body, code = json.dumps({"error": str(e)}).encode(), 502
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()
    def log_message(self, *a): pass

print(f"Serving on http://localhost:{PORT}  (Ctrl+C to stop)")
http.server.HTTPServer(("", PORT), H).serve_forever()
