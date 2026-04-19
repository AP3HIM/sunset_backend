import re

STOPWORDS = {
    "this", "that", "actually", "happened", "thought",
    "ready", "changed", "crazy", "over", "what"
    }

HOOK_WORDS = {
    "bro", "fr", "lowkey", "no", "way", "ending"

}

GENRE_TAGS = {
    "sports": ["nfl", "football"],
    "gaming": ["gaming"],
    "education": ["explained"],
    "science_tech": ["ai", "tech"],
    "entertainment": ["viral"],
}

PLATFORM_TAGS = {
    "tiktok": ["fyp"],
    "youtube": ["shorts"],
}

def extract_keywords(caption, max_keywords=2):
    words = []
    for w in caption.lower().split():
        w = re.sub(r"[^\w]", "", w)
        if (
            len(w) >= 4
            and w.isalpha()
            and w not in STOPWORDS
            and w not in HOOK_WORDS
        ):
            words.append(w)

    # preserve order, unique
    return list(dict.fromkeys(words))[:max_keywords]

def generate_tags(caption, genre, platform="tiktok"):
    tags = []

    # Content-aware tags
    tags += extract_keywords(caption, max_keywords=2)

    # Genre anchor
    tags += GENRE_TAGS.get(genre, [])[:1]

    # Platform boost (1 only)
    tags += PLATFORM_TAGS.get(platform, [])[:1]

    # Final cleanup
    tags = list(dict.fromkeys(tags))  # unique
    return tags[:5]
