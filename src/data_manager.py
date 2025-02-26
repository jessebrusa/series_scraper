class DataManager:
    def __init__(self):
        self.media_type = None
        self.searched_titles = []
        self.series_title = None
        self.series_episodes = []

    def set_media_type(self, media_type):
        self.media_type = media_type

    def get_media_type(self):
        return self.media_type
    
    def get_media_type_url(self):
        if self.get_media_type() == 'Anime':
            return 'https://www.wcostream.tv/'
        else:
            return 'https://example.com/'
        
    def set_searched_titles(self, titles):
        self.searched_titles = titles