
import json
import os

from objects.comment_object import Comment
from flask_restful import Resource, reqparse
import googleapiclient.discovery

class VideoComments(Resource):
    api_service_name = "youtube"
    api_version = "v3"
    put_args = None

    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.put_args = reqparse.RequestParser()
        self.put_args.add_argument("text", type=str, help="raw text of comment")
        self.put_args.add_argument("author", type=str, help="Display name of commenter")
        self.put_args.add_argument("time_in_seconds", type=int, help="Time when comment is posted")


    def get(self, video_id):
        youtube = self._get_api_client()
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            order="relevance"
        )

        response = request.execute()

        comment_list = []

        # Repeats loop until all comments from given video is retreived
        while "nextPageToken" in response:
            next_page_token = response["nextPageToken"]
            for comment_raw in response["items"]:
                # Filter for comments that contains timestamp
                text_display =  comment_raw["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                if "href" in text_display and "t=" in text_display:
                    time_in_seconds, time_display = self._get_time_in_seconds(text_display)

                    id = comment_raw["id"]
                    video_id = comment_raw["snippet"]["videoId"]
                    text_original = comment_raw["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                    author = comment_raw["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]

                    comment = Comment(
                            id=id,
                            video_id=video_id,
                            author=author,
                            text=text_original,
                            time_in_seconds=time_in_seconds
                        )
                    
                    comment_list.append(json.dumps(comment.__dict__))

            request = youtube.commentThreads().list(
                part="snippet",
                videoId="5NxKNrfqUjs",
                order="relevance",
                pageToken=next_page_token
            )
            response = request.execute()
        return comment_list

    def post(self, video_id):
        args = self.put_args.parse_args()
        return {video_id: args}

    def _get_api_client(self):
        '''
        Creates YoutubeAPI client
        '''
        youtube = googleapiclient.discovery.build(
            self.api_service_name,
            self.api_version,
            developerKey=self.api_key
        ) 
        return youtube
    
    def _get_time_in_seconds(self, text_display:str):
        '''
        Parses through comment to return timestamp in seconds
        '''
        time_raw = text_display.split("t=")[1].split('"')[0]
        hour = 0
        time_display = ""
        if "h" in time_raw:
            hour = int(time_raw.split("h")[0])
            time_raw = time_raw.split("h")[1]
            time_display += str(hour) + ":"
        minute = int(time_raw.split("m")[0])
        second = int(time_raw.split("m")[1].rstrip("s"))
        time_in_seconds = 3600*hour + 60*minute + second
        time_display += str(minute) + ":" + str(second)
        return (time_in_seconds, time_display)