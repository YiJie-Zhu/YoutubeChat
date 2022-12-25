import googleapiclient.discovery
import os
import json
import re

from dotenv import load_dotenv
from objects.comment_object import Comment

load_dotenv()

api_serivce_name = "youtube"
api_version = "v3"
key = os.getenv("API_KEY")

# API Client
youtube = googleapiclient.discovery.build(
    api_serivce_name,
    api_version,
    developerKey=key
)

request = youtube.commentThreads().list(
    part="snippet",
    videoId="u9-FIgI_V4s",
    order="relevance"
)

response = request.execute()
comment_list = []

while "nextPageToken" in response:
    next_page_token = response["nextPageToken"]
    for comment_raw in response["items"]:
        #filter comment
        text_display =  comment_raw["snippet"]["topLevelComment"]["snippet"]["textDisplay"]

        if "href" in text_display and "t=" in text_display:
            print(comment_raw)
            time_raw = text_display.split("t=")[1].split('"')[0]
            hour = 0
            if "h" in time_raw:
                hour = int(time_raw.split("h")[0])
                time_raw = time_raw.split("h")[1]
            minute = int(time_raw.split("m")[0])
            second = int(time_raw.split("m")[1].rstrip("s"))
            time_seconds = 3600*hour + 60*minute + second
            id = comment_raw["id"]
            video_id = comment_raw["snippet"]["videoId"]
            text_original = comment_raw["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            author = comment_raw["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]

            comment = Comment(
                    id=id,
                    video_id=video_id,
                    author=author,
                    text_display=text_display,
                    text_original=text_original,
                    time_seconds=time_seconds
                )
            
            comment_list.append(json.dumps(comment.__dict__))

    request = youtube.commentThreads().list(
        part="snippet",
        videoId="5NxKNrfqUjs",
        order="relevance",
        pageToken=next_page_token
    )
    response = request.execute()
