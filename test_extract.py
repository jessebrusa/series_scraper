import re
from playwright.sync_api import sync_playwright

class ExtractVideoUrl:
    def __init__(self, page):
        self.page = page
        self.results = []

    def log_response(self, response):
        try:
            # Check if the response body is available
            if response.status == 200 and response.body():
                # Try to get the response body as text
                body = response.text()
                # Use a regular expression to find the URL containing 'cizgifilmlerizle.com'
                match = re.search(r'https:\\/\\/[^"]*cizgifilmlerizle\.com\\/getvid\?evid=[^"]+', body)
                if match:
                    target_url = match.group(0).replace('\\/', '/')
                    if 'cizgifilmlerizle.com' in target_url:
                        self.results.append(target_url)
                        print(self.results)
        except Exception:
            pass

    def extract(self):
        self.page.on('response', self.log_response)
        
        self.page.wait_for_load_state('networkidle')

        return self.results[-1]

if __name__ == "__main__":
    episode_url = 'https://www.wcostream.tv/naruto-shippuden-episode-122-english-dubbed-2'
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(episode_url)
        
        extractor = ExtractVideoUrl(page)
        extractor.extract()
        
        browser.close()