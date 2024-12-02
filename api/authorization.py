import urllib.parse
import requests
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from handler.auth_json import AuthJson as auth

class Authorization:
    def __init__(self):
        self.client_id = auth.get_client_id()
        self.client_secret = auth.get_client_secret()
        self.redirect_uri = "http://localhost:8080/callback"
        self.auth_url = "https://accounts.spotify.com/authorize"
        self.token_url = "https://accounts.spotify.com/api/token"
        self.api_base_url = "https://api.spotify.com/v1/"
        self.access_token = None
        self.refresh_token = None
        self.expires_in = None
        self.get_auth_tokens()

    def get_auth_tokens(self):
        tokens = auth.read_auth_tokens()
        self.access_token = tokens['access_token']
        self.refresh_token = tokens['refresh_token']
        self.expires_in = tokens['expires_in']

    def authenticate(self):
        if not self.access_token or datetime.now().timestamp() > self.expires_in:
            scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-private user-read-email'
            params = {
                'client_id': self.client_id,
                'response_type': 'code',
                'scope': scope,
                'redirect_uri': self.redirect_uri,
            }
            auth_url = f"{self.auth_url}?{urllib.parse.urlencode(params)}"
            webbrowser.open(auth_url)
            self._start_http_server()

    def _start_http_server(self):
        class AuthHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if '/callback' in self.path:
                    query = urllib.parse.urlparse(self.path).query
                    code = urllib.parse.parse_qs(query).get('code')
                    if code:
                        self.server.auth_code = code[0]
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b'Authentication successful! You can close this window.')
                    else:
                        self.send_response(400)
                        self.end_headers()
                        self.wfile.write(b'Authentication failed!')

        server = HTTPServer(('localhost', 8080), AuthHandler)
        server.handle_request()
        self._exchange_code_for_token(server.auth_code)

    def _exchange_code_for_token(self, code):
        request_body = {
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(self.token_url, data=request_body)
        token_info = response.json()
        self.access_token = token_info['access_token']
        self.refresh_token = token_info['refresh_token']
        self.expires_in = datetime.now().timestamp() + token_info['expires_in']
        auth.save_auth_tokens(self.access_token, self.refresh_token, self.expires_in)

    def get_header(self):
        if datetime.now().timestamp() > self.expires_in:
            self._refresh_token()
        return {
            'Authorization': f"Bearer {self.access_token}"
        }

    def _refresh_token(self):
        request_body = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(self.token_url, data=request_body)
        new_token_info = response.json()
        self.access_token = new_token_info['access_token']
        self.expires_in = datetime.now().timestamp() + new_token_info['expires_in']
        auth.save_auth_tokens(self.access_token, self.refresh_token, self.expires_in)