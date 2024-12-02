import userpaths, os, json

class AuthJson:
    @staticmethod
    def read_json():
        path = os.path.join(userpaths.get_my_documents(), "spotiplay_auth.json")
        with open(path, "r") as f:
            return json.load(f)

    @staticmethod
    def get_client_id():
        auth = AuthJson
        return auth.read_json()['client_id']

    @staticmethod
    def get_client_secret():
        auth = AuthJson
        return auth.read_json()['client_secret']

    @staticmethod
    def save_auth_tokens(access_token: str, refresh_token: str, expires_in: int):
        tokens = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': expires_in
        }

        with open(os.path.join(userpaths.get_my_documents(), "spotiplay_auth_tokens.json"), "w") as f:
            json.dump(tokens, f)

    @staticmethod
    def read_auth_tokens():
        with open(os.path.join(userpaths.get_my_documents(), "spotiplay_auth_tokens.json"), "r") as f:
            return json.load(f)