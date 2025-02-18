from .playwright_super import PlaywrightSuper

class Compile_Series_Data(PlaywrightSuper):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.series_titles = []
        self.episode_titles = []
        self.season_episode_list = []

    def search_for_series(self, title):
        def search_title(title):
            input_selector = '#searchbox'
            self.page.wait_for_selector(input_selector)
            self.type_input(input_selector, title)

            submit_button = '#konuara > div > input[type=submit]'
            self.page.wait_for_selector(submit_button)
            self.click(submit_button)

        def collect_series_titles():
            title_selector = '.aramadabaslik a'
            self.page.wait_for_selector(title_selector)
            title_selector_list = self.collect_selectors(title_selector)
            for title in title_selector_list:
                self.series_titles.append({
                    'title': title.text_content().strip(),
                    'href': title.get_attribute('href')
                })

        search_title(title)
        collect_series_titles()
        return self.series_titles

    def get_episode_titles(self):
        episode_selector = '#catlist-listview li a'
        self.page.wait_for_selector(episode_selector)
        episode_list = self.collect_selectors(episode_selector)
        for episode in episode_list:
            self.episode_titles.append({
                'title': episode.text_content().strip(),
                'href': episode.get_attribute('href')
            })
        self.episode_titles.reverse()

        return self.episode_titles
    
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

    def get_episode_data(self):
        for episode in self.episode_titles:
            title = episode['title'].lower()
            title_list = title.split(' ')
            season_number = self.get_season_number(title_list)
            episode_numbers = self.get_episode_number(title_list)

            if episode_numbers:
                if len(episode_numbers) == 2:
                    self.season_episode_list.append([season_number, self.format_episode_data(episode_numbers[0]), self.format_episode_data(episode_numbers[1])])
                else:
                    self.season_episode_list.append([season_number, self.format_episode_data(episode_numbers[0])])

        return self.season_episode_list