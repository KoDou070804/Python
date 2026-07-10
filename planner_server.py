"""暑期学习计划 - 本地服务器
自动记录 Claude 对话中的知识点 + 提供 planner 页面
"""
import http.server
import json
import os
import webbrowser
import urllib.parse

PORT = 8888
AUTO_NOTES_FILE = os.path.join(os.path.dirname(__file__), 'kb-auto.json')

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/notes':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            notes = []
            if os.path.exists(AUTO_NOTES_FILE):
                with open(AUTO_NOTES_FILE, 'r', encoding='utf-8') as f:
                    try: notes = json.load(f)
                    except: notes = []
            self.wfile.write(json.dumps(notes, ensure_ascii=False).encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/notes':
            length = int(self.headers['Content-Length'])
            body = self.rfile.read(length).decode('utf-8')
            try: new_notes = json.loads(body)
            except: new_notes = []

            old = []
            if os.path.exists(AUTO_NOTES_FILE):
                with open(AUTO_NOTES_FILE, 'r', encoding='utf-8') as f:
                    try: old = json.load(f)
                    except: old = []

            merged = old + new_notes
            with open(AUTO_NOTES_FILE, 'w', encoding='utf-8') as f:
                json.dump(merged, f, ensure_ascii=False, indent=2)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "count": len(merged)}).encode('utf-8'))

    def log_message(self, format, *args):
        pass  # 不刷屏

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    webbrowser.open(f'http://localhost:{PORT}/planner.html')
    print(f'已启动: http://localhost:{PORT}/planner.html')
    httpd = http.server.HTTPServer(('', PORT), Handler)
    httpd.serve_forever()
