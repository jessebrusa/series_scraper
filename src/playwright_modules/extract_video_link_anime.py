from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup, Comment

class ExtractVideoLinkAnime:
    def __init__(self, page):
        self.page = page
        self.iframe_element = None
        self.video_element = None
        self.video_html = None
        self.video_src = None

    def extract_video_link(self):
        self.set_iframe()
        self.get_video_element()
        self.get_video_src()
        if self.video_src:
            return self.video_src
        return None

    def set_iframe(self):
        iframe_selector = 'iframe'
        try:
            self.page.wait_for_timeout(1250)
            self.page.wait_for_selector(iframe_selector)
            self.iframe_element = self.page.query_selector(iframe_selector)
            if not self.iframe_element:
                print('No iframe element found.')
                return None
            iframe_html = self.iframe_element.content_frame().content()
            self.soup = BeautifulSoup(iframe_html, 'html.parser')
        except Exception as e:
            print(e)

    def get_video_element(self):
        video_selector = 'video#video-js_html5_api, video#hls_html5_api'
        video_element = self.soup.select_one(video_selector)
        if video_element:
            self.video_html = str(video_element)
            self.video_element = video_element
        else:
            print('No video element found.')

    def get_video_src(self):
        if self.video_element:
            self.video_src = self.video_element.get('src')
            if self.video_src:
                return
            comment = self.soup.find(string=lambda text: isinstance(text, Comment))
            if comment:
                source_soup = BeautifulSoup(comment, 'html.parser')
                source_element = source_soup.find('source')
                if source_element:
                    self.video_src = source_element.get('src')