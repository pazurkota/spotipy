import requests
from api.authorization import Authorization

class SpotifyPlayer:
    def __init__(self, auth: Authorization):
        self.auth = auth

    def play_playback(self):
        requests.put(self.auth.api_base_url + 'me/player/play', headers=self.auth.get_header())
        return 'Successfully played music!'

    def stop_playback(self):
        requests.put(self.auth.api_base_url + 'me/player/pause', headers=self.auth.get_header())
        return 'Successfully stopped music!'

    def skip_to_next(self):
        requests.post(self.auth.api_base_url + 'me/player/next', headers=self.auth.get_header())
        return 'Successfully skipped track!'

    def skip_to_previous(self):
        requests.post(self.auth.api_base_url + 'me/player/previous', headers=self.auth.get_header())
        return 'Successfully returned to previous track!'

    def seek_to_position(self, seconds: int):
        requests.put(self.auth.api_base_url + f'me/player/seek?position_ms={seconds * 1000}', headers=self.auth.get_header())
        return f'Successfully moved track to {seconds} seconds position!'

    def set_volume(self, volume_percent: int):
        requests.put(self.auth.api_base_url + f'me/player/volume?volume_percent={volume_percent}', headers=self.auth.get_header())
        return f'Successfully changed volume to {volume_percent}%!'

    def set_repeat_mode(self, repeat_mode: str):
        # check if user entered the right mode, if not: set the repeat mode to 'context'
        if repeat_mode == 'off' or repeat_mode == 'context' or repeat_mode == 'track':
            pass
        else:
            repeat_mode = 'context'
        requests.put(self.auth.api_base_url + f'me/player/repeat?state={repeat_mode}', headers=self.auth.get_header())
        return f'Successfully set the repeat mode to {repeat_mode}!'

    def set_shuffle_mode(self, shuffle: bool):
        requests.put(self.auth.api_base_url + f'me/player/shuffle?state={shuffle}', headers=self.auth.get_header())
        return f'Successfully set the shuffle to {shuffle}!'
