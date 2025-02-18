import yt_dlp

def download_video_file(output_file='video.mp4'):
    video_url = 'https://t02.cizgifilmlerizle.com/getvid?evid=3PLPg1TqArjwjsX4ztjiAtN3APE1qRhb-n0fNRus2UgupnYGrjvnhdILyd6JgNaPxKBlfSt6yUgsLTUhC75NcwnT4HUtJ8zsfWnXJLixBEgL8Ukol_975W6GbUDrX0K9xU4EnNR8WBQoAeyAdoi5T2dUZJyvil3m0j9Nl3TgNXYEf16eJAktbzTodCSq5PSRWrr9pSLfUqminQl22uppuaeDT9F-Z7eI-HJzep-I4YLxSTV2jPKFdmPWdoGlKN0qOwi6rY_qPuv3-ZGpo5ZRsmN-UpJO_MxBs5VcB_-CT6nJLELMU5AjOeF3cL7Luxi0d7qlnM9z_7vIOq4vi78dA72X8Mag8BnPOzKdooiSkbpcdk_Diax7gxDDtaj46aPhauek77BDyLpyZZUNCoHzrlNpLlMfeBkNmlXzLkDD0VI&json'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
    }
    if video_url:
        # Download the video using yt-dlp with headers
        ydl_opts = {
            'outtmpl': output_file,  # Specify the output file name
            'http_headers': headers,  # Pass the headers to yt-dlp
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("Video downloaded successfully")
    else:
        print("Video URL not found")

if __name__ == "__main__":
    download_video_file()