import requests

def write_stream(f, name, url):
    """
    Applies the Pipe syntax to the URL to force headers in IPTV players.
    """
    # Essential headers for ICC Akamai streams
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ref = "https://www.icc-cricket.com"

    # Formatting the URL with the Pipe (|) character
    # Many players use this to identify headers for the specific stream
    url_with_headers = f"{url}|User-Agent={ua}&Referer={ref}"

    f.write(f'#EXTINF:-1 tvg-name="{name}",{name}\n')
    
    # Redundant KODIPROP tags for Android-based players (ExoPlayer)
    f.write(f'#KODIPROP:inputstream.adaptive.license_type=clearkey\n')
    f.write(f'#KODIPROP:inputstream.adaptive.user_agent={ua}\n')
    
    # The URL including the forced headers
    f.write(f"{url_with_headers}\n")

def create_m3u():
    # Using the direct raw link for 2026 ICC manifests
    json_url = "https://github.com/StmpupCricket/extract/raw/main/stream-manifests.json"
    
    try:
        response = requests.get(json_url, headers={"User-Agent": "Mozilla/5.0"})
        data = response.json()
        
        count = 0
        with open("playlist.m3u", "w") as f:
            f.write("#EXTM3U\n")
            
            # Extract HLS (.m3u8) links
            hls_urls = data.get("hls", {}).get("urls", [])
            for i, url in enumerate(hls_urls):
                if isinstance(url, str) and url.startswith("http"):
                    write_stream(f, f"ICC_HLS_{i+1}", url)
                    count += 1
            
            # Extract DASH (.mpd) links
            dash_urls = data.get("dash", {}).get("urls", [])
            for i, url in enumerate(dash_urls):
                if isinstance(url, str) and url.startswith("http"):
                    write_stream(f, f"ICC_DASH_{i+1}", url)
                    count += 1
                    
        print(f"Success: Generated playlist.m3u with {count} streams using Pipe-Header syntax.")
        
    except Exception as e:
        print(f"Python Error: {e}")
        exit(1)

if __name__ == "__main__":
    create_m3u()
