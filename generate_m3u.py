python
import requests
import json

# Your source JSON
JSON_URL = "https://github.com/StmpupCricket/extract/raw/main/stream-manifests.json"

def create_m3u():
    response = requests.get(JSON_URL)
    data = response.json()
    
    with open("playlist.m3u", "w") as f:
        f.write("#EXTM3U\n")
        for item in data:
            name = item.get("name", "Stream")
            url = item.get("url")
            # Extract keys from the clearKeys object
            drm = item.get("clearKeys", {})
            
            f.write(f'#EXTINF:-1, {name}\n')
            if drm:
                # Format: KID:KEY
                for kid, key in drm.items():
                    f.write("#KODIPROP:inputstream.adaptive.license_type=clearkey\n")
                    f.write(f"#KODIPROP:inputstream.adaptive.license_key={kid}:{key}\n")
            f.write(f"{url}\n")

if __name__ == "__main__":
    create_m3u()
