from ..abc import Asset

class Video(Asset):
    def __init__(self, video_url : str) -> None:
        super().__init__(video_url, "video")

    def __repr__(self):
        return f"<Video url='{super().url}'>"




class Image(Asset):
    def __init__(self, raw_url: str, hd_url : str):
        super().__init__(raw_url, "image")
        self._hd_url = hd_url

    def __repr__(self):
        return f"<Image url='{super().url}' hd_url='{self._hd_url}'>"

    @property
    def hd_url(self):
        return self._hd_url

    
        
    
class Media:
    def __init__(self, video : Video = None, image : Image = None):
        self._video = video
        self._image = image

    def __repr__(self):
        return f"<Media image={self.image!r} video={self.video!r}>"

    @property
    def image(self):
        return self._image

    @property
    def video(self):
        return self._video