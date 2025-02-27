from bs4 import BeautifulSoup
from .anime_episode_processor import AnimeEpisodeProcessor

class CompileEpisodeAnimeData:
    def __init__(self, page):
        self.page = page
        self.episodes = []

    def get_episodes(self):
        episode_selector = '#catlist-listview li a'
        self.wait_for_episodes(episode_selector)
        html_content = self.get_page_content()
        episode_element_list = self.parse_html_content(html_content, episode_selector)
        self.extract_episode_data(episode_element_list)
        return self.episodes

    def wait_for_episodes(self, selector):
        self.page.wait_for_selector(selector)

    def get_page_content(self):
        return self.page.content()

    def parse_html_content(self, html_content, selector):
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.select(selector)

    def extract_episode_data(self, episode_list):
        for episode in episode_list:
            episode_data = AnimeEpisodeProcessor(episode).process_episode()
            if episode_data['episode_title'] is not None:
                self.episodes.append(episode_data)
        self.episodes.reverse()
