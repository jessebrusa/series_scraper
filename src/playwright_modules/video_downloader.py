import yt_dlp

class VideoDownloader:
    def __init__(self, video_url):
        self.video_url = video_url
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

    def download_video(self, output_file='video.mp4'):
        # Debugging: Print the URL and headers
        print(f"Video URL: {self.video_url}")
        print(f"Headers: {self.headers}")
        
        if self.video_url:
            # Download the video using yt-dlp with headers
            ydl_opts = {
                'outtmpl': output_file,  # Specify the output file name
                'http_headers': self.headers,  # Pass the headers to yt-dlp
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.video_url])
                print("Video downloaded successfully")
            except yt_dlp.utils.DownloadError as e:
                print(f"Download error: {e}")
        else:
            print("Video URL not found")

if __name__ == "__main__":
    video_url = 'https://t01.watchanimesub.net//getvid?evid=mvDpTdr2hjWnOq07jjZcwJpEcgVxj5X4LVQBvZATRvDU3Pz67_D90MKjOl-NC_XHibvlIXnR-87B85jGkHRZYqj32jTpv6j2sqJFnFdmol9H-ye-XCVCcW7HnYPuH-vhkNT-PRVH-NRFou4jl20Wy3N9SAbmnIKiq1do2zIA5Qj7E62DJXvfy-kKxAemVb8AZbIRgKiyMpJdojvz9IFDei0BnT-HJh69sp4sMNj5-u3BP6NNJK7ZmrPiZVQhW5jtAdwH2mJTk87bh68cjlb41gxhh6hQ79KjHqiOSDXo50-aNUfMlMzoLyV86bu0OIhthMXHx6bD8gqHzsN1u41r1hRZgL_QnFVCU-WRx15ar-t1ilAlrxQ83oNioo_5rmqaESTqRKUTCcy24_02Mx3BEqpp0rDf1VifcJqqc28DnRxpcQyQ_j6k-kvE8Z3bKDGmeaZ9KeQHKBHYG-yvG4oS2A'
    downloader = VideoDownloader(video_url)
    downloader.download_video()