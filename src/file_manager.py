import os

class FileManager:
    def __init__(self):
        self.mount_point = "/Volumes/Plex Movies and Shows/Anime"

    def create_series_directory(self, series_title):
        self.series_path = os.path.join(self.mount_point, series_title)
        os.makedirs(self.series_path, exist_ok=True)

    def create_seasons_directory(self, num_seasons):
        season_int = int(num_seasons)
        for season in range(1, season_int + 1):
            season_path = os.path.join(self.mount_point, f"{self.series_path}/Season {season:02}")
            os.makedirs(season_path, exist_ok=True)

    def write_file(self, file_path, data):
        full_path = os.path.join(self.mount_point, file_path)
        with open(full_path, 'wb') as file:
            file.write(data)

# Example usage
if __name__ == "__main__":
    file_manager = FileManager()

    # Create series directory
    file_manager.create_series_directory("Example Series")

    # Create seasons directory
    file_manager.create_seasons_directory("3")
