from playwright.sync_api import sync_playwright
from .playwright_modules.playwright_super import PlaywrightSuper
from .playwright_modules.compile_series_data import CompileSeriesData
from .extract_video_url import ExtractVideoUrl
import random

class PlaywrightManager(PlaywrightSuper):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager    
        self.playwright = sync_playwright().start()
        self.browser = None
        self.page = None
        self.headers = {
            'authority': 'lb.watchanimesub.net',
            'method': 'GET',
            'path': '/getvid?evid=2thBDdoDHeFGvmCBSouLs1bCrtku-akOqzoQcWahpjlyoXm7i4Jk_ummZjE9gfNc5c0S27nkI3cC2MiMc9Xb9or52kpMHqj4ZnPtClAMh99eNbEuwOAtuRcTYtgSN7Zmo-av1N-EV6JbwaAKGUyiBmTT9XzYgG9cPMzBtSBMvt8CHgAnnPFcyLBSzI-pv1YmlRGHIdmbH1mbURbJUT0EIJ8CF63TuyVkJBn4d3uw8FzzJokjbqPiXl22CMeSa9Wbb_mb5AtI1oIM72oGTbbDdkVJILQC1Pu6L0EglQO-djJLLFhjy1i5qMcYpHnnfNnr3IkutY2ueJpaViWGTye0O_6nH7F9LvQrtqgrFizTaCefXJ9U1S-2CC4s862TP8M2qRh2EmtJuDYmNXsaLAjbtgib1uiYvjZv9A_KyYRS6e7xaS2Aua9bwMqFKkTOjs2P1wF4p_q_LWFrLeeacfOGMw&json',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://embed.watchanimesub.net',
            'referer': 'https://embed.watchanimesub.net/',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
        }
        self.name_url = []

    def start_browser(self, headless=True):
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page(extra_http_headers=self.headers)

    def search_for_series(self, title):
        input_selector = '#searchbox'
        self.page.wait_for_selector(input_selector)
        self.type_input(input_selector, title)

        submit_button = '#konuara > div > input[type=submit]'
        self.page.wait_for_selector(submit_button)
        self.click(submit_button)

    def collect_episode_titles(self):
        CompileSeriesData(self.data_manager, self.page).get_episode_titles()

    def collect_series_titles(self):
        title_selector = '.aramadabaslik a'
        self.page.wait_for_selector(title_selector)

        title_selector_list = self.collect_selectors(title_selector)

        series_titles_options = []
        for title in title_selector_list:
            series_titles_options.append({
                'title': title.text_content().strip(),
                'href': title.get_attribute('href')
            })

        self.data_manager.set_series_title_options(series_titles_options)

    def compile_series(self):
        def choose_series(series_list):
            result = 1  
            selected_series = series_list[result]
            return selected_series
        
        compile_series_data = CompileSeriesData(self.page)
        test_title = 'Naruto'
        series_list = compile_series_data.search_for_series(test_title)
        selected_series = choose_series(series_list)
        self.go_to(f'https://www.wcostream.tv{selected_series["href"]}')
        self.episodes = compile_series_data.get_episode_titles()
        self.episode_data = compile_series_data.get_episode_data()

    def extract_video_urls(self):   
        random_episode = random.randint(1, 350)
        for i in range(random_episode, random_episode+15):  
            episode_index = i - 1  
            self.page = self.browser.new_page(extra_http_headers=self.headers)
            self.go_to(self.episodes[episode_index]['href'])
            if self.episode_data[episode_index][0] is None:
                season_number = '01'
            else:
                season_number = self.episode_data[episode_index][0]
            if self.episode_data[episode_index][1] is None:
                continue
            else:
                episode_number = self.episode_data[episode_index][1]
            
            output_file_name = f's{season_number}e{episode_number}.mp4'
    
            extractor = ExtractVideoUrl(self.page)
            video_url = extractor.extract_video_url()

            if video_url and output_file_name:
                self.name_url.append([output_file_name, video_url])

            self.page.close()

        return self.name_url