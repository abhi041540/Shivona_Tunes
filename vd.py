import yt_dlp
import os
import tempfile

def getURL(youtube_url):
    cookies_txt = os.environ.get("YOUTUBE_COOKIES")
    cookie_path = None

    if cookies_txt:
        with tempfile.NamedTemporaryFile(delete=False, mode="w") as cookie_file:
            cookie_file.write(cookies_txt)
            cookie_path = cookie_file.name

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'format': 'bestvideo+bestaudio/best',
        'cookies': cookie_path if cookie_path else None
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            for f in info_dict.get("formats", []):
                if f.get("vcodec") != "none" and f.get("acodec") != "none":
                    return f.get("url")
            return "not"
    except :
        return "not"

if __name__ == "__main__":
    url = getURL("https://youtu.be/9pIXNy-jkbkpS10?feature=shared")
    print("Direct media URL:", url)