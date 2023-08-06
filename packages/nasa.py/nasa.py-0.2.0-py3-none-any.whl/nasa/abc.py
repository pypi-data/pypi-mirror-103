

class Asset:
    def __init__(self, raw_url : str, media_type : str):
        self._raw_url = raw_url
        self._media_type = media_type

    def __repr__(self):
        return f"<Asset url={self.url} media_type={self.media_type}>"

    @property
    def url(self):
        return self._raw_url

    @property
    def media_type(self):
        return self._media_type


