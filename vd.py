import yt_dlp
def getURL(youtube_url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'format': 'bestvideo+bestaudio/best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            # Select best format URL if available
            if 'url' in info_dict:
                return info_dict['url']
            elif 'formats' in info_dict and len(info_dict['formats']) > 0:
                for f in info_dict['formats']:
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        return f['url']
            else:
                return "not"

    except:
        return "not"

if __name__== "__main__":
  print(getURL("https://youtu.be/9pIXNy-pS10?feature=shared"))