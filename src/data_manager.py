class DataManager:
    def __init__(self):
        self.data = {
            "series_name": "",
            "series_seasons": {}
        }

    def get_data(self):
        return self.data

    def set_series_name(self, series_name):
        self.data["series_name"] = series_name
    
    def set_series_seasons(self, series_seasons):
        self.data["series_seasons"] = series_seasons    