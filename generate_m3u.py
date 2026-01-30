import requests

def create_m3u():
    json_url = "https://github.com/StmpupCricket/extract/raw/main/stream-manifests.json"
    
    try:
        response = requests.get(json_url)
        data = response.json()
        
        with open("playlist.m3u", "w") as f:
            f.write("#EXTM3U\n")
            
            for name, content in data.items():
                url = content.get("url", "")
                keys = content.get("clearkey", {})
                
                f.write(f'#EXTINF:-1 tvg-name="{name}",{name}\n')
                
                if keys:
                    # Safely get the first key-value pair
                    kid = list(keys.keys())[0]
                    key = keys[kid]
                    f.write("#KODIPROP:inputstream.adaptive.license_type=clearkey\n")
                    f.write(f"#KODIPROP:inputstream.adaptive.license_key={kid}:{key}\n")
                
                f.write(f"{url}\n")
        print("Done: playlist.m3u saved locally")
    except Exception as e:
        print(f"Python Error: {e}")
        exit(1) # Forces the GitHub Action to stop if script fails

if __name__ == "__main__":
    create_m3u()
