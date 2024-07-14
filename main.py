import os
from flask import Flask , session ,redirect, url_for , request, Response
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
scope = os.getenv('SPOTIPY_SCOPE')

cache_handler = FlaskSessionCacheHandler(session)

sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret= client_secret,
    redirect_uri= redirect_uri,
    scope = scope,
    cache_handler= cache_handler,
    show_dialog = True
)


sp = Spotify(auth_manager=sp_oauth)
@app.route('/')
def home():
    #invalid token means not logged in
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    return redirect(url_for('get_playlists'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_playlists'))


@app.route('/get_playlists')
def get_playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    playlists = sp.current_user_playlists()
    playlists_info = [(pl['name'] , pl['external_urls']['spotify']) for pl in playlists['items']]
    playlists_html = '<br>'.join([f'{name} :{url}' for name,url in playlists_info]) 
    playlists_html += '<br><a href="/get_liked_songs">View Liked Songs</a>'
    return playlists_html

@app.route('/get_liked_songs')
def get_liked_songs():
    
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    all_songs = []
    iter = 0
    while True:
        res_items = sp.current_user_saved_tracks(limit=50, offset=iter*50)['items']
        iter += 1
        all_songs += res_items
        if len(res_items) < 50:
            break
    
    liked_songs_info = [(item['track']['name'], item['track']['artists'][0]['name'], item['track']['external_urls']['spotify']) for item in all_songs]
    liked_songs_html = '<br>'.join([f'{name} by {artist}: {url}' for name, artist, url in liked_songs_info])
    liked_songs_html += '<br><a href="/download_liked_songs">Download Liked Songs as CSV</a>'
    return liked_songs_html

@app.route('/download_liked_songs')
def download_liked_songs():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    all_songs = []
    iter = 0
    while True:
        res_items = sp.current_user_saved_tracks(limit=50, offset=iter*50)['items']
        iter += 1
        all_songs += res_items
        if len(res_items) < 50:
            break
    
    liked_songs_info = [(item['track']['name'], item['track']['artists'][0]['name'], item['track']['external_urls']['spotify']) for item in all_songs]

    def generate_csv():
        output = []
        header = ['Song Name', 'Artist', 'URL']
        output.append(header)
        for song in liked_songs_info:
            output.append(song)
        for row in output:
            yield ','.join(row) + '\n'
    
    return Response(generate_csv(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=liked_songs.csv'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug = True)
