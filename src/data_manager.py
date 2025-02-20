class DataManager:
    def __init__(self, base_url):
        self.base_url = base_url
        self.series_title = None

    def set_series_title(self, series_title):
        self.series_title = series_title

    def get_series_title_href(self):
        series_page = f'{self.base_url}{self.series_title['href'][1:]}'
        return series_page

    def set_series_title_options(self, series_title_options):
        self.series_title_options = series_title_options

    def get_series_title_options(self):
        return self.series_title_options