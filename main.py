from src.playwright_manager import PlaywrightManager
from src.video_downloader import VideoDownloader

class Main:
    def __init__(self):
        self.playwright_manager = PlaywrightManager()

    def run(self):
        self.playwright_manager.start_browser(headless=False)
        self.page = self.playwright_manager.get_page()

        self.page.goto('https://www.wcostream.tv/')

        self.playwright_manager.compile_series_data()
        name_video = self.playwright_manager.extract_video_urls()
        with open('name_video.txt', 'w') as file:
            for name in name_video:
                file.write(f'{name}\n')

        self.playwright_manager.close_browser()

        with open('name_video.txt', 'r') as file:
            lines = file.readlines()
            name_video = [[lines[i].strip(), lines[i+1].strip()] for i in range(0, len(lines), 2)]

        if name_video:
            downloader = VideoDownloader(name_video, max_workers=10)
            try:
                downloader.download_videos()
            except KeyboardInterrupt:
                print("Main process interrupted. Exiting...")

if __name__ == "__main__":
    main = Main()
    try:
        main.run()
    except KeyboardInterrupt:
        print("Main process interrupted. Exiting...")