import re

class AnimeEpisodeProcessor:
    def __init__(self, episode, assigned_episode_numbers):
        self.episode_title = episode.text.strip()
        self.href = episode.get('href')
        self.season_number = None
        self.episode_number = None
        self.output_file_name = None
        self.assigned_episode_numbers = assigned_episode_numbers

    def process_episode(self):
        self.get_season_number()
        self.get_episode_number()
        self.output_file_name = f's{self.season_number}e{self.episode_number}.mp4'
        return {
            'episode_title': self.episode_title,
            'href': self.href,
            'season_number': self.season_number,
            'episode_number': self.episode_number,
            'output_file_name': self.output_file_name
        }

    def get_season_number(self):
        match = re.search(r'Season (\d+)', self.episode_title, re.IGNORECASE)
        if match:
            self.season_number = f'{int(match.group(1)):02}'
        else:
            self.season_number = '01'

    def get_episode_number(self):
        match = re.search(r'Episode (\d+)', self.episode_title, re.IGNORECASE)
        if match:
            episode_number = int(match.group(1))
        else:
            episode_number = 1

        season_key = f'Season {self.season_number}'
        if season_key not in self.assigned_episode_numbers:
            self.assigned_episode_numbers[season_key] = set()

        while episode_number in self.assigned_episode_numbers[season_key]:
            episode_number += 1

        self.assigned_episode_numbers[season_key].add(episode_number)
        self.episode_number = f'{episode_number:02}'