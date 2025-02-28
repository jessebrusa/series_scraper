import re
import json

class DataManager:
    def __init__(self):
        self.media_type = None
        self.base_url = None
        self.searched_titles = []
        self.series_title = None
        self.series_url = None
        self.series_episodes = []

    def get_data(self):
        return {
            'media_type': self.media_type,
            'base_url': self.base_url,
            'searched_titles': self.searched_titles,
            'series_title': self.series_title,
            'series_url': self.series_url,
            'series_episodes': self.series_episodes
        }

    def set_media_type(self, media_type):
        self.media_type = media_type.lower()
        self.get_media_type_url()

    def get_media_type(self):
        return self.media_type
    
    def get_media_type_url(self):
        if self.get_media_type() == 'anime':
            self.base_url = 'https://www.wcostream.tv'
            return self.base_url
        else:
            return 'https://example.com'
        
    def set_searched_titles(self, titles):
        self.searched_titles = titles

    def get_searched_titles(self):
        return self.searched_titles
    
    def set_series_title(self, title):
        self.series_title = title
    
    def get_series_title(self):
        return self.series_title
    
    def set_series_url(self, url):
        self.series_url = f'{self.base_url}{url}'

    def get_series_url(self):
        return self.series_url
    
    def set_episodes(self, episodes):
        self.series_episodes = episodes

    def get_episodes(self):
        return self.series_episodes
    
    def get_num_seasons(self):
        season_num = 1
        for episode in self.series_episodes:
            season_num = max(season_num, int(episode['season_number']))
        return season_num
    
    def add_video_src(self, index, video_src):
        self.series_episodes[index]['video_src'] = video_src

    def add_cookies(self, index, cookies):
        self.series_episodes[index]['cookies'] = cookies

    def get_sanitized_series_title(self):
        return re.sub(r'[\\/*?:"<>|]', "", self.series_title)

    def write_data(self):
        data = self.get_data()
        with open(f"./data/anime/{self.get_sanitized_series_title()}.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self, file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            self.media_type = data['media_type']
            self.base_url = data['base_url']
            self.searched_titles = data['searched_titles']
            self.series_title = data['series_title']
            self.series_url = data['series_url']
            self.series_episodes = data['series_episodes']