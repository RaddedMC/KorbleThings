# YouTube scraper for Korble Coaching Exercise Library
# SiteBuilder.py: Takes the parsed data and turns it into the video page on korblecoaching.com!
# By James N / Radded @ https://github.com/RaddedMC and https://linktr.ee/RaddedMC

from libs.VidObjects import *

video_template = ""
navitem_template = ""
page_template = ""

def import_resources():
    global video_template
    video_template = open("siteCode/Resources/video-template.html").read()
    print("Video template loaded!")

    global navitem_template
    navitem_template = open("siteCode/Resources/navitem-template.html").read()
    print("NavBar item template loaded!")

    global page_template
    page_template = open("siteCode/Resources/page-blank.html").read()
    print("NavBar item template loaded!")

def build_site(data):
    # Resources

    print("Loading resources...")
    import_resources()
    global video_template
    global navitem_template
    global page_template


    # Variables

    playlist_counter = 0


    # FOR EACH PLAYLIST:
    for playlist in data:
        print("Creating page for playlist " + playlist.name)

        # Create navbar items
        navbar_items = []
        nav_playlist_counter = 0
        for playlist_bar in data:
            navbar_items.append(navitem_template.format(category_name = playlist_bar.name, is_active = "active" if playlist_bar.name == playlist.name else "", navitem_link="main.html" if nav_playlist_counter == 0 else (playlist_bar.name + ".html")))
            nav_playlist_counter += 1
        
        # Create videos
        videos = []
        for video in playlist.videos:
            videos.append(video_template.format(video_link = video.unlisted_link, thumbnail_link = video.thumb_link['url'], video_title = video.title, author = video.author, description = video.description))

        # Create page
        navbar_items_string = ""
        for item in navbar_items:
            navbar_items_string += (item + "\n")
        videos_string = ""
        for item in videos:
            videos_string += (item + "\n")

        page = page_template.format(navitems = navbar_items_string, videos = videos_string)
        pagename = "main.html" if playlist_counter == 0 else playlist.name + ".html"

        with open("siteCode/"+pagename, "w") as pagefile:
            pagefile.write(page)
        print("Page completed!")


        playlist_counter += 1