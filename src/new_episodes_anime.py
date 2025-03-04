import os

class NewEpisodeAnime:
    def __init__(self, data_manager, file_manager):
        self.data_manager = data_manager
        self.file_manager = file_manager
        self.series_path = self.file_manager.get_series_directory()

    def get_missing_episodes(self):
        missing_episodes = []
        episodes = self.data_manager.get_episodes()

        for episode in episodes:
            season_directory = self.file_manager.get_season_directory(episode['season_number'])
            episode_file_name = episode['output_file_name']
            episode_file_path = os.path.join(season_directory, episode_file_name)

            if not os.path.exists(episode_file_path):
                missing_episodes.append(episode)

        self.data_manager.set_episodes(missing_episodes)
