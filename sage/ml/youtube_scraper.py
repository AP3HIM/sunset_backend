from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import time
import os
import re

API_KEY = "AIzaSyBm_eMLOYrPqgJtLtZL2PiFtj8HIw-OfEs"

youtube = build("youtube", "v3", developerKey=API_KEY)

DATA_PATH = "sage/ml/data/captions.csv"

GENRE_KEYWORDS = {
    "sports": ["NFL highlights", "NBA shorts", "football crazy ending"],
    "gaming": ["fortnite shorts", "minecraft shorts", "valorant clips"],
    "education": ["did you know", "explained in 60 seconds", "science facts"],
    "entertainment": ["viral shorts", "funny clips", "prank shorts"],
    "science_tech": ["AI explained", "technology facts", "coding shorts"],
}

# --------- CLEANING ---------
def is_good_caption(title: str) -> bool:
    if len(title) < 6:
        return False
    if title.isupper():
        return False
    if re.search(r"(full video|episode \d+|official trailer)", title.lower()):
        return False
    return True


def fetch_by_search(genre, keywords, max_results=300):
    rows = []

    for keyword in keywords:
        next_page_token = None

        while len(rows) < max_results:
            request = youtube.search().list(
                part="snippet",
                q=keyword,
                type="video",
                maxResults=50,
                order="viewCount",
                pageToken=next_page_token,
            )

            response = request.execute()

            for item in response.get("items", []):
                title = item["snippet"]["title"]

                if not is_good_caption(title):
                    continue

                rows.append({
                    "caption": title,
                    "description": item["snippet"].get("description", ""),
                    "genre": genre,
                    "platform": "youtube",
                    "source": "search",
                })

                if len(rows) >= max_results:
                    break

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

            time.sleep(0.2)

    return rows


# --------- MAIN ---------
all_rows = []

for genre, keywords in GENRE_KEYWORDS.items():
    print(f"\nFetching {genre}...")
    try:
        rows = fetch_by_search(genre, keywords, max_results=300)
        print(f"  → got {len(rows)} new captions")
        all_rows.extend(rows)
    except HttpError as e:
        print(f"Failed for {genre}: {e}")

new_df = pd.DataFrame(all_rows)

# Load existing captions if present
if os.path.exists(DATA_PATH):
    old_df = pd.read_csv(DATA_PATH)
    df = pd.concat([old_df, new_df], ignore_index=True)
else:
    df = new_df

# Deduplicate
df = df.drop_duplicates(subset=["caption"]).reset_index(drop=True)

df.to_csv(DATA_PATH, index=False)

print(f"\nSaved {len(df)} total captions to {DATA_PATH}")
