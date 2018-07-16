"""
at first run set the update flag to false as it will delete the table and insert all videos
after this set the update flag to True so u only update the table in db
"""

import time
from YoutubeAPI import YoutubeAPI
from DatabaseUtils import DatabaseUtils

playlist_url = "https://www.youtube.com/watch?v=vPszR0-vTqc&list=PLvFsG9gYFxY97JaF2PiBy5fjPy1zufrcF"
channel_url = 'https://www.youtube.com/user/AsapSCIENCE/videos'
playlist_id = 'PLvFsG9gYFxY97JaF2PiBy5fjPy1zufrcF'
channel_name = 'AsapSCIENCE'

#for the playlist format we use the playlist id, otherwise we use the channel name
format_type = "playlist"
update = False

youtube_api = YoutubeAPI()
db = DatabaseUtils()
old_videos_url = {}
new_videos_url = {}

if update:
    old_videos_url = db.retrieve_videos_urls()

if format_type == "channel":
    channel_uploads_id = youtube_api.get_uploads_id(channel_name)
    playlist_id = channel_uploads_id

while True:
    print("working...")
    videos_response = youtube_api.get_playlist_videos(playlist_id)
    videos = youtube_api.get_videos(videos_response)

    new_videos_url = {}
    for vid in videos:
        new_videos_url[vid['id']] = True

    if not update:
        db.insert_all_videos(videos)
        update = True
    else:
        db.update_videos(videos, new_videos_url, old_videos_url)

    old_videos_url = new_videos_url

    print("Waiting...")
    print
    time.sleep(60)

