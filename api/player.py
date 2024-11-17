import requests
from datetime import datetime
from flask import Flask, redirect, session, request
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

        @self.app.route('/next')
        def skip_to_next():
            requests.post(self.auth.api_base_url + 'me/player/next', headers=_get_header())
            return 'Successfully skipped track!'

        @self.app.route('/previous')
        def skip_to_previous():
            requests.post(self.auth.api_base_url + 'me/player/previous', headers=_get_header())
            return 'Successfully returned to previous track!'

        @self.app.route('/to_position')
        def seek_to_position():
            seconds = request.args.get('sec', default=1, type=int)
            requests.put(self.auth.api_base_url + f'me/player/seek?position_ms={seconds * 1000}', headers=_get_header())
            return f'Successfully moved track to {seconds} seconds position!'

        @self.app.route('/volume')
        def set_volume():
            volume_percent = request.args.get('percent', default=50, type=int)
            requests.put(self.auth.api_base_url + f'me/player/volume?volume_percent={volume_percent}', headers=_get_header())
            return f'Successfully changed volume to {volume_percent}%!'

        @self.app.route('/repeat_mode')
        def set_repeat_mode():
            repeat_mode = request.args.get('mode', default='context', type=str)

            # check if user entered the right mode, if not: set the repeat mode to 'context'
            if repeat_mode == 'off' or repeat_mode == 'context' or repeat_mode == 'track':
                pass
            else:
                repeat_mode = 'context'

            requests.put(self.auth.api_base_url + f'me/player/repeat?state={repeat_mode}', headers=_get_header())
            return f'Successfully set the repeat mode to {repeat_mode}!'

        @self.app.route('/shuffle')
        def set_shuffle_mode():
            shuffle = request.args.get('enable', default=False, type=bool)
            requests.put(self.auth.api_base_url + f'me/player/shuffle?state={shuffle}', headers=_get_header())
            return f'Successfully set the shuffle to {shuffle}!'
