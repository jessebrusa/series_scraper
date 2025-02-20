class DataManager:
    def __init__(self):
        self.base_url = 'https://www.wcostream.tv'
        self.series_title = None

    def set_series_title(self, series_title):
        self.series_title = series_title

    def get_series_title_href(self):
        return  f'{self.base_url}{self.series_title['href']}'

    def set_series_title_options(self, series_title_options):
        self.series_title_options = series_title_options

    def get_series_title_options(self):
        return self.series_title_options
    
    def set_episode_titles(self, episode_titles):
        self.episode_titles = episode_titles