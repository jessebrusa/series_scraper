class EpisodeDataProcessor:
    def __init__(self):
        self.season_episode_list = []

    def format_episode_data(self, data):
        data = int(data)
        if data < 10:
            return f'0{data}'
        return str(data)

    def get_season_number(self, title_list):
        if 'season' in title_list:
            return self.format_episode_data(title_list[title_list.index('season') + 1])
        return None

    def get_episode_number(self, title_list):
        if 'episode' in title_list:
            episode_number = title_list[title_list.index('episode') + 1]
            if '-' in episode_number:
                return episode_number.split('-')
            return [episode_number]
        return None

    def process_episode_data(self, episode_titles):
        for episode in episode_titles:
            title = episode['title'].lower()
            title_list = title.split(' ')
            season_number = self.get_season_number(title_list)
            episode_numbers = self.get_episode_number(title_list)

            if episode_numbers:
                if len(episode_numbers) == 2:
                    self.season_episode_list.append([season_number, self.format_episode_data(episode_numbers[0]), self.format_episode_data(episode_numbers[1])])
                else:
                    self.season_episode_list.append([season_number, self.format_episode_data(episode_numbers[0])])
            else:
                # Skip entries without episode numbers
                continue

        return self.season_episode_list