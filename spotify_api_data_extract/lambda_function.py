import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3
from datetime import datetime

def lambda_handler(event, context):
    
    # Spotify API authentication
    client_id = os.environ.get("client_id")     # use environment variables
    client_secret = os.environ.get("client_secret")
    
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    
    playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF"
    playlist_URI = playlist_link.split("/")[-1]
    
    spotify_data = sp.playlist_tracks(playlist_URI)
    client = boto3.client("s3")
    
    filename = f"spotify_raw_{str(datetime.now())}.json"
    
    client.put_object(
        Bucket="spotify-etl-project-demo",
        Key=f"raw_data/to_processed/{filename}",
        Body=json.dumps(spotify_data)
        )
    