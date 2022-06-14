# YouTube scraper for Korble Coaching Exercise Library
# VideoGrabber.py: The functions needed to grab video data from the YouTube API.
# By James N / Radded @ https://github.com/RaddedMC and https://linktr.ee/RaddedMC

# --- IMPORTS ---
import urllib.request
import json
from xmlrpc.client import MAXINT
from libs.VidObjects import *

# --- GLOBALS ---
API_KEY = ""

# Opens the playlists.txt file and reads the playlist ids from it.
def get_playlist_ids(playlist_filelocation, api_key_filelocaton):
    playlists = []

    ### GET KEY FROM FILE ###
    global API_KEY

    with open(api_key_filelocaton) as file:
        API_KEY = file.readline().strip()

    
    ### GET PLAYLIST IDS ###
    with open(playlist_filelocation) as file:
        for listlink in file:
            # The find() method strips out everything before the '=' sign in the URL. All we need is the playlist ID!
            playlists.append(listlink[listlink.find("=")+1:].rstrip())

    return playlists


# This method will run once per playlist -- it grabs the name of that playlist!
def get_playlist_name(playlistid):
    global API_KEY

    # This URL will be populated with your API key and the playlist that the scraper is searching.
    url = "https://www.googleapis.com/youtube/v3/playlists?"\
          "id={playlistId}&"\
          "key={key}&"\
          "part=snippet".format(
        playlistId=playlistid,
        key=API_KEY
    )

    data = json.load(urllib.request.urlopen(url))
    name = data["items"][0]["snippet"]["title"]
    return name


# This method will run once per playlist -- grabs the video IDs of videos within that playlist from YouTube Data PlaylistItems
def get_playlist_videos(playlistid):
    global API_KEY

    # This URL will be populated with your API key and the playlist that the scraper is searching.
    url = "https://www.googleapis.com/youtube/v3/playlistItems?"\
          "playlistId={playlistId}&"\
          "key={key}&"\
          "part=contentDetails".format(
        playlistId=playlistid,
        key=API_KEY
    )

    # Gets the data from the YouTube playlist!
    data = json.load(urllib.request.urlopen(url))
    
    ### Now we need to drill down into the HTTP response to get the data for each video!
    playlistItems = data["items"]

    video_ids = []
    for item in playlistItems:
        video_ids.append(item["contentDetails"]["videoId"])

    videos_data = []
    for video_id in video_ids:
        print()
        print("Getting data from video " + video_id)
        videos_data.append(get_rich_video_data(video_id))

    return playlist(get_playlist_name(playlistid), videos_data)


# Runs multiple times per playlist -- grabs metadata of a video from its ID with YouTube Data Videos
def get_rich_video_data(video_id):
    global API_KEY

    # This URL will be populated with your API key and the video that the scraper is searching for.
    url = "https://www.googleapis.com/youtube/v3/videos?"\
          "part=snippet&"\
          "id={id}&"\
          "key={key}".format(
        id=video_id,
        key=API_KEY
    )

    # Gets the data from the YouTube video!
    data = json.load(urllib.request.urlopen(url))
    video_data = data["items"][0]

    ### PARSE DESCRIPTION / AUTHOR INFO ###
    return parse_video(video_data)


# This method runs once per video in a playlist. Parses the description and author text from that video.
def parse_video(video_data):

    descriptionString = video_data["snippet"]["description"]
    parseFailed = False
    description = ""
    author = ""

    try:
        desc_index = descriptionString.lower().index("video description: ") + 19
    except:
        # Handle later
        pass

    # AUTHOR
    try:
        auth_index = descriptionString.lower().index("author: ") + 8
    except:
        # Handle later
        parseFailed = True

        # TODO: spelling error

        print("Error! Unable to parse description/author data in video " + video_data["snippet"]["title"] + ". Was it formatted correctly? Got:" + descriptionString[0:50])
        description = "We weren't able to find the description for this one. Please <a href=\"about:blank\">let us know!</a>"
        author = "We weren't able to find the author for this one. Please <a href=\"about:blank\">let us know!</a>"
        pass
    
    # TIMESTAMP
    if not parseFailed:
        timestamp_index = MAXINT
        try:
            timestamp_index = descriptionString.lower().index("timestamps:")
        except:
            print("No timestamps detected for this video.")
            pass

        description = descriptionString[desc_index:(auth_index-8)]
        author = descriptionString[auth_index:timestamp_index]
        

    try:
        scraped_video = video(title=video_data["snippet"]["title"],
            description=description,
            author=author,
            thumb_link=video_data["snippet"]["thumbnails"]["maxres"],
            unlisted_link="https://youtu.be/"+video_data["id"])
    except:
        print("Detected a Short!")
        scraped_video = video(title=video_data["snippet"]["title"],
            description=description,
            author=author,
            thumb_link=video_data["snippet"]["thumbnails"]["high"],
            unlisted_link="https://youtu.be/"+video_data["id"])
    
    return scraped_video


