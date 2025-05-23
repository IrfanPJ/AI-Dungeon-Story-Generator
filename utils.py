import os
from datetime import datetime

def save_story_to_file(story_text, folder="saved_stories", genre="story"):
    os.makedirs(folder, exist_ok=True)
    safe_genre = genre.replace(" ", "_").lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder, f"{safe_genre}_{timestamp}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(story_text)
    return filename
