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
        def _get_header():
            if 'access_token' not in session:
                return redirect('/login')

            if datetime.now().timestamp() > session['expires_in']:
                return redirect('/refresh_token')

            return {
                'Authorization': f"Bearer {session['access_token']}"
            }

        @self.app.route('/play')
        def play_playback():
            requests.put(self.auth.api_base_url + 'me/player/play', headers=_get_header())
            return 'Successfully played music!'

        @self.app.route('/stop')
        def stop_playback():
            requests.put(self.auth.api_base_url + 'me/player/pause', headers=_get_header())
            return 'Successfully stopped music!'
