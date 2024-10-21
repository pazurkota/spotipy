from flask import Flask
from api.authorization import Authorization

app = Flask(__name__)
app.secret_key = 'spotiplay_key'

auth = Authorization(app)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
