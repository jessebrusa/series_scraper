class DataManager:
    def __init__(self):
        self.media_type = None
        self.series_title = None
        self.series_episodes = []

    def set_media_type(self, media_type):
        self.media_type = media_type

    def get_media_type(self):
        return self.media_type