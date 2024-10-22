from flask import Flask
from api.authorization import Authorization
from api.player import SpotifyPlayer

app = Flask(__name__)
app.secret_key = 'spotiplay_key'

auth = Authorization(app)
player = SpotifyPlayer(auth, app)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
