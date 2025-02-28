import yt_dlp
import concurrent.futures
import os
import time

class VideoDownloader:
    def __init__(self, file_manager, data_manager):
        self.data_manager = data_manager
        self.file_manager = file_manager
        self.episodes = self.data_manager.get_episodes()[:3]

    def download_videos(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for episode in self.episodes:
                print(episode)
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
            while attempts < 3:
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])
                    print(f"Downloaded successfully: {output_file_name}")
                    break
                except yt_dlp.utils.DownloadError as e:
                    attempts += 1
                    print(f"DownloadError: {e}")
                    print(f"Attempt {attempts} failed for {output_file_name}. Retrying...")
                    time.sleep(2) 
            else:
                print(f"Failed to download {output_file_name} after 3 attempts.")
        else:
            print(f"No video URL found for {output_file_name}")

    def get_headers(self, cookies):
        return {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.8',
            'cookie': cookies,
            'referer': 'https://embed.watchanimesub.net/inc/embed/video-js.php?file=reload%2F%5BYameii%5D%20Solo%20Leveling%20-%20S01E01%20%5BEnglish%20Dub%5D%20%5BCR%20WEB-DL%201080p%5D%20%5B5A1D9152%5D.flv&fullhd=1&pid=904149&h=884c6a462f619e391c2a2351480973a5&t=1740768642&embed=neptun',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-storage-access': 'none',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

    def output_path(self, episode):
        return os.path.join(self.file_manager.get_season_directory(episode['season_number']), episode['output_file_name'])