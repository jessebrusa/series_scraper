import os
import re

class FileManager:
    def __init__(self, directory=None):
        if directory:
            self.directory = directory
        else:
            self.directory = "/Volumes/Plex Movies and Shows/Anime"
        self.series_path = None

    def sanitize_title(self, title):
        return re.sub(r'[<>:"/\\|?*]', '', title)

    def create_series_directory(self, series_title):
        sanitized_title = self.sanitize_title(series_title)
        self.series = sanitized_title
        self.series_path = os.path.join(self.directory, sanitized_title)
        try:
            os.makedirs(self.series_path, exist_ok=True)
        except PermissionError as e:
            print(f"PermissionError: {e}")
            print("Please check the permissions or change the directory path.")
            raise

    def get_series_directory(self):
        return self.series_path

    def create_seasons_directories(self, num_seasons):
        if not self.series_path:
            raise ValueError("Series path is not set. Call create_series_directory first.")
        season_int = int(num_seasons)
        for season in range(1, season_int + 1):
            season_path = os.path.join(self.series_path, f"Season {season:02}")
            os.makedirs(season_path, exist_ok=True)

    def get_season_directory(self, season_number):
        if not self.series_path:
            raise ValueError("Series path is not set. Call create_series_directory first.")
        return os.path.join(self.series_path, f"Season {season_number:02}")