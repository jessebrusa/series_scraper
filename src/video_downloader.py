import yt_dlp
import concurrent.futures
import os

class VideoDownloader:
    def __init__(self, file_manager, data_manager, max_workers=5):
        self.data_manager = data_manager
        self.file_manager = file_manager
        self.episode_finished_data = self.data_manager.get_processed_episodes()
        self.max_workers = max_workers
        self.set_headers()
        self.video_list = self.set_video_list()

    def set_headers(self):
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

    def set_video_list(self):
        video_list = []
        for episode in self.episode_finished_data:
            if 'video_url' in episode and 'output_file_name' in episode:
                video_list.append({
                    'video_url': episode['video_url'],
                    'output_file': episode['output_file_name'],
                    'season_number': episode['season_number']
                })
        return video_list
    
    def output_path(self, episode):
        return os.path.join(self.file_manager.get_season_directory(episode['season_number']), episode['output_file'])

    def download_videos(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for episode in self.video_list:
                futures.append(executor.submit(self.download_video, episode['video_url'], self.output_path(episode)))
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error occurred: {e}")

    def download_video(self, video_url, output_file='video.mp4'):
        if video_url:
            ydl_opts = {
                'outtmpl': output_file,
                'http_headers': self.headers,
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                print(f"Video downloaded successfully: {output_file}")
            except yt_dlp.utils.DownloadError as e:
                print(f"Download error for {output_file}: {e}")
        else:
            print("Video URL not found")