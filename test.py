import yt_dlp
from playwright.sync_api import sync_playwright

class VideoDownloader:
    def __init__(self, url):
        self.url = url
        self.video_url = None
        self.headers = {}

    def handle_request(self, request):
        if 'getvid' in request.url:
            self.video_url = request.url
            self.headers = request.headers

    def download_video_file(self):
        if self.video_url:
            print(f"Video URL found: {self.video_url}")
            # Download the video using yt-dlp with headers
            ydl_opts = {
                'outtmpl': 'video.mp4',  # Specify the output file name
                'http_headers': self.headers,  # Pass the headers to yt-dlp
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.video_url])
            print("Video downloaded successfully")
        else:
            print("Video URL not found")

    def get_first_iframe(self, page):
        # Wait for the iframe to be available and switch to it
        iframe_selector = 'iframe'
        page.wait_for_selector(iframe_selector)
        iframe_element = page.query_selector(iframe_selector)
        
        # Ensure the iframe element is found
        if iframe_element is None:
            print("Iframe element not found")
            return None
        
        iframe = iframe_element.content_frame()
        
        # Ensure the iframe is found
        if iframe is None:
            print("Iframe not found")
            return None
        
        return iframe

    def download_video(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            page.on('request', self.handle_request)
            
            page.goto(self.url)
            
            # Get the first iframe
            iframe = self.get_first_iframe(page)
            if iframe is None:
                browser.close()
                return
            
            # Wait for the video element to be available within the iframe's body
            video_selector = '#video-js_html5_api'
            iframe.wait_for_selector(video_selector)
            
            # Wait for the src attribute to be set on the video element
            iframe.wait_for_function('document.querySelector("#video-js_html5_api").getAttribute("src") !== null')
            
            # Extract the video URL from the video element's src attribute
            self.video_url = iframe.evaluate('document.querySelector("#video-js_html5_api").getAttribute("src")')
            print(f"Video URL: {self.video_url}")
            
            # Download the video file
            self.download_video_file()
            
            browser.close()

if __name__ == "__main__":
    episode_url = 'https://www.wcostream.tv/naruto-shippuden-episode-1-english-dubbed'
    downloader = VideoDownloader(episode_url)
    downloader.download_video()