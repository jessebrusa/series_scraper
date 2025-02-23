import yt_dlp

def download_video(url, output_path):
    ydl_opts = {
        'outtmpl': output_path
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    url = 'https://mcloud.vvid30c.site/watch/?v21#QngvRDVlNGYwbnhjQ1pFZGRPZlFuNHprYjcwYjlROTFKcnZPb0xQSlFZSk01U2VIUFhZQWpHTy9tWGFCTThaOXYrZz0'
    output_path = './tools/wolverine.mp4'
    download_video(url, output_path)