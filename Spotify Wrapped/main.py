import requests
import urllib.parse

from datetime import datetime, timedelta
from flask import Flask, redirect, jsonify, request, session, render_template

app = Flask(__name__)
app.secret_key = 'fcfcfcm'

CLIENT_ID = '08cc6e9e0dd14ea6808a28ff1958599d'

CLIENT_SECRET = '7d48d19cd2d04d4aba5dac8b1589648c'

REDIRECT_URI = 'http://localhost:5000/callback'


AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email user-top-read'

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session['access_token'] =  token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        return redirect('/wrapped')
    
@app.route('/wrapped')
def get_wrapped():
    if 'access_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = {}

    response["profile"] = (requests.get(API_BASE_URL + 'me', headers=headers)).json()

    response["topTracks"] = (requests.get(API_BASE_URL + 'me/top/tracks?limit=6&time_range=long_term', headers=headers)).json()

    response["topArtists"] = (requests.get(API_BASE_URL + 'me/top/artists?limit=6&time_range=long_term', headers=headers)).json()

    return render_template('homepage.html')
    

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect ('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = request.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()

        session['access_token'] = new_token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

        return redirect('/wrapped')
    
# @app.route('/yourwrapped')
# def yourwrapped():
#     return render_template('homepage.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

