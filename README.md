# Spotify Playlist and Liked Songs Viewer

This Flask application allows users to authenticate with Spotify, view their playlists, and see their liked songs. The app uses the Spotipy library for Spotify API interactions and manages sensitive information with environment variables.

## Features

- Authenticate with Spotify
- View Spotify playlists
- View liked songs on Spotify

## Prerequisites

- Python 3.x
- Spotify Developer Account
- Spotify Client ID and Client Secret

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/potatoooo34/spotify-viewer.git
cd spotify-viewer
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory of the project with the following content:

```env
SPOTIPY_CLIENT_ID='your_client_id_here'
SPOTIPY_CLIENT_SECRET='your_client_secret_here'
SPOTIPY_REDIRECT_URI='http://127.0.0.1:5000/callback'
SPOTIPY_SCOPE='playlist-read-private user-read-email user-read-private user-library-read'
```

Replace `'your_client_id_here'`, `'your_client_secret_here'`, and other placeholder values with your actual Spotify Developer credentials.

### 5. Run the Application

```bash
flask run
```

Open your browser and go to `http://127.0.0.1:5000` to view the app.

## Usage

- Navigate to the home page to authenticate with Spotify.
- After authentication, you will be redirected to a page displaying your playlists.
- Click on "View Liked Songs" to see your liked songs on Spotify.

