import os
import requests
import urllib.request
import json
import time


def download_bird_audio(bird_name, output_dir="dataset"):
    api_url = f"https://www.xeno-canto.org/api/2/recordings?query={bird_name.replace(' ', '%20')}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()

        data = json.loads(response.content)

        if len(data['recordings']) == 0:
            print(f"No recordings found for {bird_name}.")
            return

        # Create a directory for this bird species (class)
        bird_dir = os.path.join(output_dir, bird_name)
        if not os.path.exists(bird_dir):
            os.makedirs(bird_dir)

        for recording in data['recordings']:
            file_url = recording['file']
            

            if not file_url.startswith("https://"):
                file_url = f"https://www.xeno-canto.org{file_url}"
            
            file_name = os.path.join(bird_dir, f"{recording['id']}.mp3")

            print(f"Downloading {file_name} from {file_url}...")
            try:
                urllib.request.urlretrieve(file_url, file_name)
            except Exception as e:
                print(f"Failed to download {file_name}: {e}")

        print(f"Downloaded all recordings for {bird_name}!")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {bird_name}: {e}")

# List of bird species (classes)
bird_classes = [
    "White-throated Bushchat", "Long-tailed Duck", "Swamp Francolin", "Jerdon's Babbler", 
    "Grey-sided Thrush", "Egyptian Vulture", "Grey-crowned Prinia", "Black Kite", 
    "Slender-billed Babbler", "Spotted Dove", "Himalayan Monal", "Large-billed Crow", 
    "Grey Treepie", "Red-billed Blue Magpie", "Cheer Pheasant", "Spiny Babbler", 
    "House Sparrow", "Great Slaty Woodpecker", "Common Cuckoo", "Rufous-necked Hornbill", 
    "Wood Snipe", "Pallas's Fish Eagle", "Bristled Grassbird", "Common Wood Pigeon", 
    "House Crow", "Rufous Treepie", "Asian Koel", "Black-necked Crane", "Indian Spotted Eagle", 
    "Sarus Crane", "Greater Spotted Eagle", "Rustic Bunting", "Eastern Imperial Eagle", 
    "Rose-ringed Parakeet", "Black-breasted Parrotbill", "Steppe Eagle", 
    "Kashmir Flycatcher", "Common Pochard", "Swamp Grass-babbler", "Saker Falcon", 
    "Satyr Tragopan", "White-throated Bush Chat", "Swamp Grass Babbler"
]


# Download audio for each bird class in the list
for bird in bird_classes:
    download_bird_audio(bird)
    time.sleep(2)
