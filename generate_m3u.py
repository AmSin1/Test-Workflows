import requests

def create_m3u():
    json_url = "https://github.com/StmpupCricket/extract/raw/main/stream-manifests.json"
    
    try:
        response = requests.get(json_url, headers={"User-Agent": "Mozilla/5.0"})
        data = response.json()
        
        with open("playlist.m3u", "w") as f:
            f.write("#EXTM3U\n")
            
            # Case 1: JSON is a Dict {"Channel Name": {"url": "...", "clearkey": {...}}}
            if isinstance(data, dict):
                for name, content in data.items():
                    if isinstance(content, dict):
                        write_entry(f, name, content)
            
            # Case 2: JSON is a List [{"name": "...", "url": "..."}]
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        name = item.get("name", "Unknown Stream")
                        write_entry(f, name, item)

        print("Playlist generated successfully.")
    except Exception as e:
        print(f"Python Error: {e}")
        exit(1)

def write_entry(f, name, content):
    url = content.get("url", "")
    keys = content.get("clearkey", {})
    
    if url:
        f.write(f'#EXTINF:-1 tvg-name="{name}",{name}\n')
        if isinstance(keys, dict) and keys:
            # Get the first KID and KEY
            kid = list(keys.keys())[0]
            key = keys[kid]
            f.write("#KODIPROP:inputstream.adaptive.license_type=clearkey\n")
            f.write(f"#KODIPROP:inputstream.adaptive.license_key={kid}:{key}\n")
        f.write(f"{url}\n")

if __name__ == "__main__":
    create_m3u()
