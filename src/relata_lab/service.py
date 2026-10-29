"""Loopback-only single-writer transport. Opening a page never executes a study."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import secrets
import subprocess
from urllib.parse import urlsplit

from .application import Application, ATLAS, REPO
from .core import LabError

MAX_BODY = 4 * 1024 * 1024


def make_server(workspace, port=0):
    app = Application(workspace)
    token = secrets.token_urlsafe(32)
    assets = REPO / 'apps' / 'studio'
    component = subprocess.run(['node', str(ATLAS / 'studio-payload.cjs'), '--component'],
                               capture_output=True, check=True, timeout=30).stdout

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass  # URLs and author material are not server logs.

        def send(self, data, status=200, media='application/json; charset=utf-8'):
            if isinstance(data, (dict, list)):
                data = json.dumps(data, ensure_ascii=False, allow_nan=False).encode()
            elif isinstance(data, str):
                data = data.encode()
            self.send_response(status)
            self.send_header('Content-Type', media)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self'; frame-src 'self' blob:; frame-ancestors 'none'; object-src 'none'; base-uri 'none'")
            self.end_headers()
            self.wfile.write(data)

        def allowed(self, api=False):
            host = '127.0.0.1:' + str(self.server.server_port)
            if self.headers.get('Host') != host:
                self.send({'error': 'host', 'message': 'Use the exact loopback address.'}, 403)
                return False
            origin = self.headers.get('Origin')
            if origin and origin != 'http://' + host:
                self.send({'error': 'origin', 'message': 'Cross-origin requests are not accepted.'}, 403)
                return False
            if api and not secrets.compare_digest(self.headers.get('X-Relata-Token', ''), token):
                self.send({'error': 'token', 'message': 'Reopen this local Studio session.'}, 403)
                return False
            return True

        def do_GET(self):
            path = urlsplit(self.path).path
            if not self.allowed(path.startswith('/api/')):
                return
            try:
                if path == '/':
                    self.send((assets / 'index.html').read_text().replace('__SESSION_TOKEN__', token), media='text/html; charset=utf-8')
                elif path in ('/studio.js', '/analysis.js', '/studio.css', '/clinic.js', '/clinic.html'):
                    media = 'text/css' if path.endswith('.css') else 'text/html' if path.endswith('.html') else 'text/javascript'
                    self.send((assets / path[1:]).read_bytes(), media=media + '; charset=utf-8')
                elif path == '/atlas.js':
                    self.send(component, media='text/javascript; charset=utf-8')
                elif path == '/legacy-clinic.html':
                    self.send((REPO / 'case-lab/reviews/workbench/index.html').read_bytes(),
                              media='application/octet-stream')
                elif path == '/api/state':
                    self.send(app.state())
                elif path.startswith('/api/object/'):
                    parts = path.split('/')
                    self.send(app.lab.get_object(parts[3], int(parts[4]) if len(parts) > 4 else None))
                elif path.startswith('/api/artifact/'):
                    # Always text: no imported active HTML/SVG ever receives app origin.
                    self.send(app.lab.read_artifact(path.split('/')[-1]), media='text/plain; charset=utf-8')
                else:
                    self.send({'error': 'not_found'}, 404)
            except (LabError, ValueError, KeyError) as exc:
                self.send({'error': getattr(exc, 'code', 'invalid'), 'message': str(exc)}, 400)

        def do_POST(self):
            if not self.allowed(True):
                return
            if self.path != '/api/command':
                self.send({'error': 'not_found'}, 404)
                return
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= MAX_BODY:
                    self.send({'error': 'size', 'message': 'Request exceeds the 4 MiB local command limit.'}, 413)
                    return
                if self.headers.get_content_type() != 'application/json':
                    self.send({'error': 'media_type'}, 415)
                    return
                data = json.loads(self.rfile.read(length))
                result = app.command(data['name'], data['payload'], data['command_id'])
                self.send(result)
            except (LabError, ValueError, KeyError, TypeError) as exc:
                self.send({'error': getattr(exc, 'code', 'invalid'), 'message': str(exc),
                           'detail': getattr(exc, 'detail', None)}, 409 if getattr(exc, 'code', '') == 'conflict' else 400)
            except (OSError, subprocess.SubprocessError) as exc:
                self.send({'error': 'local_operation', 'message': str(exc)}, 500)

    server = HTTPServer(('127.0.0.1', port), Handler)
    server.application = app
    return server


def serve(workspace, port):
    server = make_server(workspace, port)
    print('Relata Studio: http://127.0.0.1:' + str(server.server_port), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.application.close()
        server.server_close()
