from bs4 import BeautifulSoup
from .playwright_super import PlaywrightSuper

class CompileEpisodeTitles(PlaywrightSuper):
    def __init__(self, data_manager, page):
        super().__init__()
        self.data_manager = data_manager
        self.page = page
        self.episode_titles = []

    def get_episode_titles(self):
        episode_selector = '#catlist-listview li a'
        self._wait_for_episodes(episode_selector)
        html_content = self._get_page_content()
        episode_list = self._parse_html_content(html_content, episode_selector)
        self.episode_titles = self._extract_episode_titles(episode_list)
        self._store_episode_titles()

    def _wait_for_episodes(self, selector):
        self.page.wait_for_selector(selector)

    def _get_page_content(self):
        return self.page.content()

    def _parse_html_content(self, html_content, selector):
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.select(selector)

    def _extract_episode_titles(self, episode_list):
        episode_titles = [
            {
                'title': episode.text.strip(),
                'href': episode.get('href')
            }
            for episode in episode_list
            if 'episode' in episode.text.strip().lower()
        ]
        episode_titles.reverse()
        return episode_titles

    def _store_episode_titles(self):
        self.data_manager.set_episode_titles(self.episode_titles)