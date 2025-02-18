import yt_dlp
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

class VideoDownloader:
    def __init__(self, page):
        self.page = page
        self.video_url = None
        self.headers = {}
        print("VideoDownloader initialized")

    def handle_request(self, request):
        if 'getvid' in request.url:
            self.video_url = request.url
            self.headers = request.headers

    def download_video_file(self, output_file='video.mp4'):
        if self.video_url:
            # Download the video using yt-dlp with headers
            ydl_opts = {
                'outtmpl': output_file,  # Specify the output file name
                'http_headers': self.headers,  # Pass the headers to yt-dlp
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.video_url])
            print("Video downloaded successfully")
        else:
            print("Video URL not found")

    def get_first_iframe(self):
        # Wait for the iframe with the specific id to be available and switch to it
        iframe_selector = '#frameNewcizgifilmuploads0'
        self.page.wait_for_selector(iframe_selector)
        iframe_element = self.page.query_selector(iframe_selector)
        
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

    def download_video(self, output_file='video.mp4'):
        self.page.on('request', self.handle_request)
        
        # Get the first iframe
        iframe = self.get_first_iframe()
        if iframe is None:
            return
        
        # Get the HTML content of the iframe
        iframe_content = iframe.content()
        
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(iframe_content, 'html.parser')
        
        # Find the video tag with the specific id within the iframe
        video_tag = soup.find('video', id='video-js_html5_api')
        
        # Extract the video URL from the video element's src attribute
        if video_tag:
            self.video_url = video_tag.get('src')
            print(f"Video URL: {self.video_url}")
        
        # Download the video file
        self.download_video_file(output_file)

if __name__ == "__main__":
    episode_url = 'https://www.wcostream.tv/naruto-shippuden-episode-123-english-dubbed-2'
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(episode_url)
        
        downloader = VideoDownloader(page)
        downloader.download_video()
        
        browser.close()