from .data_manager_modules.episode_data_processor import EpisodeDataProcessor
import json

class DataManager:
    def __init__(self):
        self.base_url = 'https://www.wcostream.tv'
        self.series_title = None
        self.episode_titles = None
        self.processed_episodes = None

    def set_series_title(self, series_title):
        self.series_title = series_title

    def get_series_title(self):
        if self.series_title:
            return self.series_title['title']
        return None

    def get_series_title_href(self):
        if self.series_title:
            return f'{self.base_url}{self.series_title["href"]}'
        return None

    def set_series_title_options(self, series_title_options):
        self.series_title_options = series_title_options

    def get_series_title_options(self):
        return self.series_title_options
    
    def set_episode_titles(self, episode_titles):
        self.episode_titles = episode_titles

    def get_episode_titles(self):
        return self.episode_titles

    def filter_episodes(self):
        processed_episodes = []
        for episode in self.episode_titles:
            try:
                data = EpisodeDataProcessor(episode).process_episode()
                processed_episodes.append(data)
            except ValueError as e:
                print(f"Skipping episode due to error: {e}")
        self.processed_episodes = processed_episodes
    
    def get_processed_episodes(self):
        return self.processed_episodes

    def add_video_url(self, episode_number, video_url):
        for episode in self.processed_episodes:
            if episode['episode_number'] == episode_number:
                episode['video_url'] = video_url
                return

    def num_seasons(self):
        season_num = 1
        for episode in self.processed_episodes:
            season_num = max(season_num, int(episode['season_number']))
        return season_num
    
    def write_series_title(self):
        with open('./test_data/series_title.json', 'w') as f:
            json.dump(self.series_title, f)

    def write_episodes(self):
        with open('./test_data/episodes.json', 'w') as f:
            json.dump(self.episode_titles, f)   

    def write_processed_episodes(self):
        with open('./test_data/processed_episodes.json', 'w') as f:
            json.dump(self.processed_episodes, f)

    def read_series_title(self):
        with open('./test_data/series_title.json', 'r') as f:
            self.series_title = json.load(f)

    def write_finished_episodes(self):
        with open('./test_data/finished_episodes.json', 'w') as f:
            json.dump(self.processed_episodes, f)