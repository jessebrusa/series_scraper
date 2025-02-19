import yt_dlp
import concurrent.futures

class VideoDownloader:
    def __init__(self, video_list, max_workers=5):
        self.video_list = video_list
        self.max_workers = max_workers
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

    def download_videos(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            try:
                for item in self.video_list:
                    if isinstance(item, (list, tuple)) and len(item) == 2:
                        output_file, video_url = item
                        futures.append(executor.submit(self.download_video, video_url, output_file))
                    else:
                        print(f"Invalid item format: {item}")
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        print(f"Error occurred: {e}")
            except KeyboardInterrupt:
                print("Download process interrupted. Shutting down...")
                executor.shutdown(wait=False)
                raise

if __name__ == "__main__":
    video_list = [
        ['s01e01.mp4', 'https://t01.watchanimesub.net//getvid?evid=mvDpTdr2hjWnOq07jjZcwJpEcgVxj5X4LVQBvZATRvDU3Pz67_D90MKjOl-NC_XHibvlIXnR-87B85jGkHRZYqj32jTpv6j2sqJFnFdmol9H-ye-XCVCcW7HnYPuH-vhkNT-PRVH-NRFou4jl20Wy3N9SAbmnIKiq1do2zIA5Qj7E62DJXvfy-kKxAemVb8AZbIRgKiyMpJdojvz9IFDei0BnT-HJh69sp4sMNj5-u3BP6NNJK7ZmrPiZVQhW5jtAdwH2mJTk87bh68cjlb41gxhh6hQ79KjHqiOSDXo50-aNUfMlMzoLyV86bu0OIhthMXHx6bD8gqHzsN1u41r1hRZgL_QnFVCU-WRx15ar-t1ilAlrxQ83oNioo_5rmqaESTqRKUTCcy24_02Mx3BEqpp0rDf1VifcJqqc28DnRxpcQyQ_j6k-kvE8Z3bKDGmeaZ9KeQHKBHYG-yvG4oS2A'],
        # Add more [output_file_name, video_url] pairs here
    ]
    downloader = VideoDownloader(video_list, max_workers=5)
    try:
        downloader.download_videos()
    except KeyboardInterrupt:
        print("Main process interrupted. Exiting...")