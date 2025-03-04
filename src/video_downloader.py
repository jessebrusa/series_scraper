import yt_dlp
import concurrent.futures
import os
import time
import platform

class VideoDownloader:
    def __init__(self, file_manager, data_manager):
        self.data_manager = data_manager
        self.file_manager = file_manager
        self.episodes = self.data_manager.get_episodes()

    def download_videos(self):
        self.cleanup_old_files()

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for episode in self.episodes:
                futures.append(executor.submit(self.download_video, episode['video_src'], self.output_path(episode), episode['cookies']))
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"An error occurred: {e}")

    def download_video(self, video_url, output_file_name, cookies):
        if video_url:
            ydl_opts = {
                'outtmpl': output_file_name,
                'http_headers': self.get_headers(cookies)
            }
            attempts = 0
            while attempts < 5:  # Increase retry attempts
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])
                    print(f"Downloaded successfully: {output_file_name}")
                    break
                except yt_dlp.utils.DownloadError as e:
                    attempts += 1
                    print(f"DownloadError: {e}")
                    print(f"Attempt {attempts} failed for {output_file_name}. Retrying...")
                    time.sleep(5)  # Increase delay between retries
            else:
                print(f"Failed to download {output_file_name} after 5 attempts.")
        else:
            print(f"No video URL found for {output_file_name}")

    def get_platform(self):
        if platform.system() == 'Windows':
            self.sec_ch_ua_platform = '"Windows"'
            self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
        else:
            self.sec_ch_ua_platform = '"macOS"'
            self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'

    def get_headers(self, cookies):
        self.get_platform()
        return {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': cookies,
            'referer': 'https://embed.watchanimesub.net/inc/embed/video-js.php?file=Watch%20Dragon%20Ball%20Heroes%20Episode%201.flv&hd=1&pid=423566&h=fbdeffbb573d679d7258e6ab47fbb710&t=1740872269&embed=www',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': self.sec_ch_ua_platform,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-storage-access': 'active',
            'user-agent': self.user_agent,
            'x-requested-with': 'XMLHttpRequest'
        }

    def output_path(self, episode):
        return os.path.join(self.file_manager.get_season_directory(episode['season_number']), episode['output_file_name'])

    def cleanup_old_files(self):
        # Implement cleanup logic to delete files that do not end with .mp4
        for episode in self.episodes:
            season_directory = self.file_manager.get_season_directory(episode['season_number'])
            for filename in os.listdir(season_directory):
                if not filename.endswith('.mp4'):
                    file_path = os.path.join(season_directory, filename)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"Deleted old file: {file_path}")