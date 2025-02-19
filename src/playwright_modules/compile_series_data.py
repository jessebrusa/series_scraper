from .playwright_super import PlaywrightSuper
from .episode_data_processor import EpisodeDataProcessor

class CompileSeriesData(PlaywrightSuper):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.series_titles = []
        self.episode_titles = []
        self.episode_data_processor = EpisodeDataProcessor()

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
        
        self.episode_titles = [
            {
                'title': episode.text_content().strip(),
                'href': episode.get_attribute('href')
            }
            for episode in episode_list
            if 'episode' in episode.text_content().strip().lower()  # Filter out movies
        ]
        
        self.episode_titles.reverse()
        
        for i, episode in enumerate(self.episode_titles):
            print(f"Episode {i+1}: {episode['title']}")
        
        return self.episode_titles
    
    def get_episode_data(self):
        episode_data = self.episode_data_processor.process_episode_data(self.episode_titles)
        
        # Debug print to check processed episode data
        for i, data in enumerate(episode_data):
            print(f"Episode Data {i}: {data}")
        
        return episode_data

    def get_episode_data(self):
        return self.episode_data_processor.process_episode_data(self.episode_titles)