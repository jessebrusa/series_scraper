from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup, Comment

class ExtractVideoUrl:
    def __init__(self, page):
        self.page = page

    def extract_video_url(self):
        try:
            self.page.wait_for_timeout(1250)
            self.page.wait_for_selector('iframe')
            iframe_element = self.page.query_selector('iframe')
            if not iframe_element:
                print("Iframe element not found")
                return None

            iframe = iframe_element.content_frame()
            if not iframe:
                print("Iframe content not found")
                return None
            
            iframe.wait_for_selector('video#video-js_html5_api, video#hls_html5_api')
            video_element = iframe.query_selector('video#video-js_html5_api, video#hls_html5_api')
            if not video_element:
                print("Video element not found")
                return None

            # Print the video element's outer HTML
            video_html = video_element.evaluate("element => element.outerHTML")
            print(video_html)

            video_src = video_element.get_attribute('src')
            if not video_src:
                print("Video source not found in video element")
                # Use BeautifulSoup to parse the HTML and extract the URL from the commented source tag
                soup = BeautifulSoup(video_html, 'html.parser')
                comment = soup.find(string=lambda text: isinstance(text, Comment))
                if comment:
                    source_soup = BeautifulSoup(comment, 'html.parser')
                    source_element = source_soup.find('source')
                    if source_element:
                        video_src = source_element.get('src')
                        print("Video source found in commented source element")
            print(f"Extracted video URL: {video_src}")
            return video_src
        except Exception as e:
            print(f"Error extracting video URL: {e}")
            return None

if __name__ == "__main__":
    episode_url = 'https://www.wcostream.tv/naruto-shippuden-episode-347-english-dubbed'
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.set_extra_http_headers({
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
        })
        
        page.goto(episode_url)
        
        extractor = ExtractVideoUrl(page)
        video_url = extractor.extract_video_url()
        
        if video_url:
            print(f"Extracted video URL: {video_url}")
        else:
            print("Failed to extract video URL")
        
        browser.close()