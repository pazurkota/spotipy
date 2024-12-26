# 🎼 spotiplay - simple Spotify CLI player!

---

### Quick Start:
##### Prerequisites:
The recommended version of Python is 3.10 or above

##### Installation:
1. Clone the repository:
```shell
git clone https://github.com/pazurkota/spotiplay.git
cd spotiplay
```

2. Create a virtual environment:
```shell
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install dependencies:
```shell
pip install flask
pip install requests
pip install userpaths
pip install urllib3
```

4. Set up the confiuration file:
    - Create a file named `spotiplay_auth.json` in your Documents directory with the following content:
    ```json
    {
      "client_id": "your_spotify_client_id",
      "client_secret": "your_spotify_client_secret"
    }
    ```
   
##### Running the Application:

1. Start the flask application:
```shell
python main.py
```

2. Access the application:
   - Open your web browser and go to `http://localhost:8080`

##### Usage
- Login with Spotify:  
   - Click on the "Login with Spotify" link on the homepage.
   - Authorize the application to access your Spotify account.
  
- View Playlists:
  - After logging in, you will be redirected to the playlists page where you can view your Spotify playlists.