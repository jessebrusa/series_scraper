class EpisodeDataProcessor:
    def __init__(self, episode):
        self.title = episode['title']
        self.href = episode['href']
        self.title_to_list()
        self.season_number = None
        self.episode_number = None

    def title_to_list(self):
        self.title_list = self.title.lower().split(' ')
    
    def format_episode_data(self, data):
        data = int(data)
        if data < 10:
            return f'0{data}'
        return str(data)
    
    def get_season_number(self):
        if 'season' in self.title_list:
            self.season_number = self.format_episode_data(self.title_list[self.title_list.index('season') + 1])
        else:
            self.season_number = '01'
    
    def get_episode_number(self):
        if 'episode' in self.title_list:
            self.episode_number = self.title_list[self.title_list.index('episode') + 1]
            if '-' in self.episode_number:
                self.episode_number = self.episode_number.split('-')

    def format_output_file_name(self):
        if isinstance(self.episode_number, list):
            return [f's{self.season_number}e{episode}.mp4' for episode in self.episode_number]
        return f's{self.season_number}e{self.episode_number}.mp4'

    def process_episode(self):
        self.get_season_number()
        self.get_episode_number()

        if self.season_number is None and self.episode_number is None:
            print(f'MOVIE: {self.title}')

        if isinstance(self.episode_number, list):
            episodes = []
            formatted_file_names = self.format_output_file_name()
            for episode, file_name in zip(self.episode_number, formatted_file_names):
                episodes.append({
                    'title': self.title,
                    'href': self.href,
                    'season_number': self.season_number,
                    'episode_number': episode,
                    'output_file_name': file_name
                })
            return episodes

        return {
            'title': self.title,
            'href': self.href,
            'season_number': self.season_number,
            'episode_number': self.episode_number,
            'output_file_name': self.format_output_file_name()
        }