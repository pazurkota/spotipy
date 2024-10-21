import urllib.parse
from datetime import datetime

import requests
from flask import Flask, redirect, request, jsonify, session
from urllib3 import request

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

        @self.app.route('/callback')
        def callback():
            if 'error' in request.args:
                return jsonify({"error": request.args['error']})

            if 'code' in request.args:
                request_body = {
                    'code': request.args['code'],
                    'grant_type': 'authorization_code',
                    'redirect_uri': self.redirect_uri,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret
                }

                response = requests.post(self.token_url, data=request_body)
                token_info = response.json()

                session['access_token'] = token_info['access_token']
                session['refresh_token'] = token_info['refresh_token']
                session['expires_in'] = datetime.now().timestamp() + token_info['expires_in']

        @self.app.route('/refresh_token')
        def refresh_token():
            if 'refresh_token' not in session:
                return redirect('/login')

            if datetime.now().timestamp() > session['expires_at']:
                request_body = {
                    'grant_type': 'refresh_token',
                    'refresh_token': session['refresh_token'],
                    'client_id': self.client_id,
                    'client_secret': self.client_secret
                }

                response = requests.post(self.token_url, data=request_body)
                new_token_info = response.json()

                session['access_token'] = new_token_info['access_token']
                session['expires_in'] = datetime.now().timestamp() + new_token_info['expires_in']