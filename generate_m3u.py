import requests

def write_stream(f, name, url):
    """
    Handles writing the specific metadata and headers for each stream.
    """
    # Essential headers to bypass Akamai 403 Forbidden errors
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    referer = "https://www.icc-cricket.com"

    f.write(f'#EXTINF:-1 tvg-name="{name}",{name}\n')
    
    # 1. Headers for VLC and standard IPTV players
    f.write(f'#EXTVLCOPT:http-user-agent={user_agent}\n')
    f.write(f'#EXTVLCOPT:http-referrer={referer}\n')
    
    # 2. Headers for Kodi/ExoPlayer/Android based players
    f.write(f'#KODIPROP:inputstream.adaptive.license_type=clearkey\n')
    f.write(f'#KODIPROP:inputstream.adaptive.user_agent={user_agent}\n')
    
    # 3. The actual Stream URL
    f.write(f"{url}\n")

def create_m3u():
    json_url = "https://github.com/StmpupCricket/extract/raw/main/stream-manifests.json"
    
    try:
        # Fetching JSON with a User-Agent to avoid being blocked by GitHub's bot protection
        response = requests.get(json_url, headers={"User-Agent": "Mozilla/5.0"})
        data = response.json()
        
        count = 0
        with open("playlist.m3u", "w") as f:
            f.write("#EXTM3U\n")
            
            # Extracting HLS URLs
            hls_urls = data.get("hls", {}).get("urls", [])
            for i, url in enumerate(hls_urls):
                if isinstance(url, str) and url.startswith("http"):
                    write_stream(f, f"ICC_HLS_{i+1}", url)
                    count += 1
            
            # Extracting DASH URLs
            dash_urls = data.get("dash", {}).get("urls", [])
            for i, url in enumerate(dash_urls):
                if isinstance(url, str) and url.startswith("http"):
                    write_stream(f, f"ICC_DASH_{i+1}", url)
                    count += 1
                    
        print(f"Success: Added {count} channels to playlist.m3u with updated playback headers.")
        
    except Exception as e:
        print(f"Python Error: {e}")
        exit(1)

if __name__ == "__main__":
    create_m3u()
