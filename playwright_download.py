from playwright.sync_api import sync_playwright
import requests

def extract_video_url(page_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            extra_http_headers={
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
            }
        )
        page = context.new_page()
        
        # Go to the page URL
        page.goto(page_url)
        
        # Wait for the video element to be available
        video_selector = 'video source'
        try:
            page.wait_for_selector(video_selector, timeout=60000)  # Increase timeout to 60 seconds
        except Exception as e:
            print(f"Error waiting for selector: {e}")
            browser.close()
            return None
        
        # Ensure all network requests are completed
        page.wait_for_load_state('networkidle')
        
        # Get the video URL from the source element's src attribute
        video_url = page.evaluate('document.querySelector("video source").getAttribute("src")')
        
        # Debugging: Print the extracted video URL
        print(f"Extracted Video URL: {video_url}")
        
        browser.close()
        return video_url

def download_video_file(video_url, output_file='video.mp4'):
    headers = {
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
    
    # Debugging: Print the video URL
    print(f"Video URL: {video_url}")
    
    # Download the video file
    if video_url:
        response = requests.get(video_url, headers=headers, stream=True, allow_redirects=True)
        
        # Debugging: Print the response status code and headers
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Video downloaded successfully")
        else:
            print(f"Failed to download video. Status code: {response.status_code}")
    else:
        print("Video URL not found")

if __name__ == "__main__":
    page_url = 'https://t01.watchanimesub.net/getvid?evid=mvDpTdr2hjWnOq07jjZcwJpEcgVxj5X4LVQBvZATRvDU3Pz67_D90MKjOl-NC_XHibvlIXnR-87B85jGkHRZYqj32jTpv6j2sqJFnFdmol9H-ye-XCVCcW7HnYPuH-vhkNT-PRVH-NRFou4jl20Wy3N9SAbmnIKiq1do2zIA5Qj7E62DJXvfy-kKxAemVb8AZbIRgKiyMpJdojvz9IFDei0BnT-HJh69sp4sMNj5-u3BP6NNJK7ZmrPiZVQhW5jtAdwH2mJTk87bh68cjlb41gxhh6hQ79KjHqiOSDXo50-aNUfMlMzoLyV86bu0OIhthMXHx6bD8gqHzsN1u41r1hRZgL_QnFVCU-WRx15ar-t1ilAlrxQ83oNioo_5rmqaESTqRKUTCcy24_02Mx3BEqpp0rDf1VifcJqqc28DnRxpcQyQ_j6k-kvE8Z3bKDGmeaZ9KeQHKBHYG-yvG4oS2A'
    video_url = extract_video_url(page_url)
    download_video_file(video_url)