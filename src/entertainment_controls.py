import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build
import subprocess
import webbrowser
import os
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, YOUTUBE_API_KEY

# Spotify API credentials and scope
scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

# YouTube service
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Local Media Playback with Subprocess
def play_local_media(file_path):
    if os.path.isfile(file_path):
        subprocess.Popen(['start', file_path] , shell=True)
    else:
        print("File does not exist:", file_path)

def open_youtube_video(query):
    video_url = search_youtube_video(query)
    if video_url:
        webbrowser.open(video_url)
    else:
        print("Video not found.")

def search_youtube_video(query):
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=1
    )
    response = request.execute()
    if response["items"]:
        video_id = response["items"][0]["id"]["videoId"]
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        return None

# Spotify Controls
def play_spotify_track(track_name):
    results = sp.search(q=track_name, type="track", limit=1)
    if results["tracks"]["items"]:
        track_uri = results["tracks"]["items"][0]["uri"]
        sp.start_playback(uris=[track_uri])

def pause_spotify():
    sp.pause_playback()

def resume_spotify():
    sp.start_playback()

def skip_spotify_track():
    sp.next_track()

def previous_spotify_track():
    sp.previous_track()

# Example usage
if __name__ == "__main__":
    # Local Media Example
    play_local_media("C:/Users/Administrator/Music/My List/AFSANAY Song Mp3 Download Young Stunners.mp3")

    # # YouTube Example
    # open_youtube_video("Relaxing music")
    #
    # # Spotify Example
    # play_spotify_track("Shape of You")
