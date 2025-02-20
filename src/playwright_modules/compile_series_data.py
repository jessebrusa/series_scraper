from .playwright_super import PlaywrightSuper
from .episode_data_processor import EpisodeDataProcessor

class CompileSeriesData(PlaywrightSuper):
    def __init__(self, data_manager, page):
        super().__init__()
        self.data_manager = data_manager
        self.page = page
        self.episode_titles = []

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
            if 'episode' in episode.text_content().strip().lower()
        ]
        self.episode_titles.reverse()

        self.data_manager.set_episode_titles(self.episode_titles)
        print(self.episode_titles)