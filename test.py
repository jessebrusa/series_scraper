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

    def download_video(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            page.on('request', self.handle_request)
            
            page.goto(self.url)
            
            # Wait for the iframe to be available and switch to it
            iframe_selector = '#frameNewcizgifilmuploads0'
            page.wait_for_selector(iframe_selector)
            iframe = None
            for frame in page.frames:
                if frame.url.startswith('https://embed.watchanimesub.net/inc/embed/video-js.php'):
                    iframe = frame
                    break
            
            # Ensure the iframe is found
            if iframe is None:
                print("Iframe not found")
                browser.close()
                return
            
            # Wait for the video element to be available within the iframe
            video_selector = 'video'
            iframe.wait_for_selector(video_selector)
            
            # Click the play button to generate the video URL using JavaScript within the iframe
            iframe.evaluate('document.querySelector(\'button[title="Play Video"]\').click()')
            
            # Wait for the network request to complete
            page.wait_for_timeout(10000)  # Adjust the timeout as needed
            
            # Download the video file
            self.download_video_file()
            
            browser.close()

if __name__ == "__main__":
    episode_url = 'https://www.wcostream.tv/naruto-shippuden-episode-1-english-dubbed'
    downloader = VideoDownloader(episode_url)
    downloader.download_video()