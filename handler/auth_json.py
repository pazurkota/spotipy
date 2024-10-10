import userpaths, os, json

class AuthJson:
    @staticmethod
    def read_json():
        path = os.path.join(userpaths.get_my_documents(), "spotiplay_auth.json")
        with open(path, "r") as f:
            return json.load(f)
