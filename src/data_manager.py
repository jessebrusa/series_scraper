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
        return self.series_title['title']

    def get_series_title_href(self):
        return f'{self.base_url}{self.series_title["href"]}'

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
            data = EpisodeDataProcessor(episode).process_episode()
            if isinstance(data, list):
                for episode in data:
                    processed_episodes.append(episode)
            else:
                processed_episodes.append(data)
        self.processed_episodes = processed_episodes
    
    def get_processed_episodes(self):
        return self.processed_episodes

    def num_seasons(self):
        season_num = 1
        for episode in self.processed_episodes:
            if episode['season_number'] is not None:
                if int(episode['season_number']) > season_num:
                    season_num = int(episode['season_number'])
        return season_num

    def add_video_url(self, title, url):
        for episode in self.processed_episodes:
            if episode['title'] == title:
                episode['video_url'] = url

    def write_episodes(self):
        with open('./test_data/episodes.json', 'w') as json_file:
            json.dump(self.episode_titles, json_file, indent=4)

    def read_episodes(self):
        with open('./test_data/episodes.json', 'r') as json_file:
            self.episode_titles = json.load(json_file)

    def write_processed_episodes(self):
        with open('./test_data/processed_episodes.json', 'w') as json_file:
            json.dump(self.processed_episodes, json_file, indent=4)

    def read_processed_episodes(self):
        with open('./test_data/processed_episodes.json', 'r') as json_file:
            self.processed_episodes = json.load(json_file)

    def write_finished_episodes(self):
        with open('./test_data/finished_episodes.json', 'w') as json_file:
            json.dump(self.processed_episodes, json_file, indent=4)

    def read_finished_episodes(self):
        with open('./test_data/finished_episodes.json', 'r') as json_file:
            self.processed_episodes = json.load(json_file)