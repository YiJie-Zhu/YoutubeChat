class Comment:
    def __init__(
        self,
        id: str,
        video_id: str,
        author: str,
        text: str,
        time_in_seconds: int,
    ):
        self.id = id
        self.video_id = video_id
        self.author = author
        self.text = text
        self.time_in_seconds = time_in_seconds

