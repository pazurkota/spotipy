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