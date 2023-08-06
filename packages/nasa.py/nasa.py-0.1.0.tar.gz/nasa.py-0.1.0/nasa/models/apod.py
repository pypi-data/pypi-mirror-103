from .meta import Video, Image, Media
from typing import Union




class APODResult:
    def __init__(self, payload : dict):
        self._payload = payload

    def __repr__(self):
        return f"<APODResult date={self.date} explanation={self.explanation} media={self.media!r} title={self.title}>"

    @property
    def date(self) -> str:
        return self._payload.get("date")

    @property
    def explanation(self) -> str:
        return self._payload.get("explanation")

    @property
    def media(self) -> Union[Image, Video]:
        media_type = self._payload.get("media_type")
        if media_type == "video":
            video = Video(self._payload.get("url"))
            return Media(image = None, video = video)
        elif media_type == "image":
            image = Image(self._payload.get("url"),  self._payload.get("hdurl"))
            return Media(image = image, video = None)
        else:
            raise TypeError("Invalid Media Type returned by NASA APOD API")

    @property
    def title(self) -> str:
        return self._payload.get("title")

    @property
    def raw_data(self) -> dict:
        return self._payload

    

        