# YouTube scraper for Korble Coaching Exercise Library
# VidObjects.py: The data structures used to organize video data.
# By James N / Radded @ https://github.com/RaddedMC and https://linktr.ee/RaddedMC

class playlist:
    name = ""
    videos = []

    def __init__(self, name, videos):
        self.name = name
        self.videos = videos

class video:
    title = ""
    description = ""
    author = ""
    thumb_link = ""
    unlisted_link = ""

    def __init__(self, title, description, author, thumb_link, unlisted_link):
        self.title = title
        self.description = description
        self.author = author
        self.thumb_link = thumb_link
        self.unlisted_link = unlisted_link