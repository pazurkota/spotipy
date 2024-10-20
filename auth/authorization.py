import urllib.parse
from flask import Flask, redirect
from handler.auth_json import AuthJson as auth

class Authorization:
    def __init__(self, app: Flask):
        self.app = app
        self.client_id = auth.get_client_id()
        self.client_secret = auth.get_client_secret()
        self.redirect_uri = "http://localhost:8080/callback"
        self.auth_url = "https://accounts.spotify.com/authorize"
        self.token_url = "https://accounts.spotify.com/api/token"
        self.api_base_url = "https://api.spotify.com/v1/"
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return "Welcome to spotiplay! <a href='/login'>Login with Spotify</a>"

        @self.app.route('/login')
        def login():
            scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

            params = {
                'client_id': self.client_id,
                'response_type': 'code',
                'scope': scope,
                'redirect_uri': self.redirect_uri,
            }

            auth_url = f"{self.auth_url}?{urllib.parse.urlencode(params)}"

            return redirect(auth_url)