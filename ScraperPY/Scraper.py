# YouTube scraper for Korble Coaching Exercise Library
# Scraper.py: The driver for the scraper program.
# By James N / Radded @ https://github.com/RaddedMC and https://linktr.ee/RaddedMC

# --- GLOBALS ---
scope = "youtube.readonly"
playlist_file = "playlists.txt" # Change this to change the location of the playlists file
key_file = "apikey.txt"

# --- IMPORTS ---
from libs.SiteBuilder import *
from libs.VideoGrabber import *
from libs.VidObjects import *

# Youtube's API needs me to have the *unlisted links* in order to grab data from *unlisted playlists*.
### Please update the links in playlists.txt in order for the YouTube scraper to grab videos from those playlists. ###

# Primary driver method.
def main():
    global playlist_file
    global key_file

    print("--- KorbleScraper ---")

    ### GET VIDEOS ###
    print("Grabbing video data...")
    playlistids = get_playlist_ids(playlist_file, key_file)
    playlists = []
    for id in playlistids:
        print("Getting videos from playlist " + id)
        playlists.append(get_playlist_videos(id))

        print()
        print("Finished playlist " + playlists[-1].name)

        print()
        print()
    
    ### PARSE SITE ###
    print("------------------------")
    print("Generating video page...")

    build_site(playlists)


if __name__ == "__main__":
    main()