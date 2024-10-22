import requests
from datetime import datetime
from flask import Flask, redirect, jsonify, session
from api.authorization import Authorization

class SpotifyPlayer:
    def __init__(self, auth: Authorization, app: Flask):
        self.auth = auth
        self.app = app
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/playlists')
        def get_playlists():  # test method to check if it works. to be deleted soon
            if 'access_token' not in session:
                return redirect('/login')

            if datetime.now().timestamp() > session['expires_in']:
                return redirect('/refresh_token')

            headers = {
                'Authorization': f"Bearer {session['access_token']}"
            }

            response = requests.get(self.auth.api_base_url + 'me/playlists', headers=headers)
            playlists = response.json()

            return jsonify(playlists)
