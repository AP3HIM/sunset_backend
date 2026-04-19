import re

def platform_penalty(caption, platform):
    score = 0.0
    length = len(caption)

    if platform == "youtube":
        if length > 90:
            score -= 0.7
        if "#" in caption:
            score -= 0.3

    if platform == "tiktok":
        if length > 70:
            score -= 0.5
        if caption.count("#") > 3:
            score -= 0.5

    return score

def repetition_penalty(caption):
    words = caption.lower().split()
    unique_ratio = len(set(words)) / max(len(words), 1)

    if unique_ratio < 0.65:
        return -0.4
    return 0.0
'''
def emoji_penalty(caption):
    if sum(caption.count(e) for e in ["🔥","🤯","👀","🏈"]) > 1:
        return -0.3
    return 0.0
'''
def intent_penalty(caption, prompt):
    prompt_words = set(
        w for w in re.findall(r"\b[a-z]{4,}\b", prompt.lower())
    )
    caption_words = set(
        w for w in re.findall(r"\b[a-z]{4,}\b", caption.lower())
    )

    overlap = len(prompt_words & caption_words)

    if overlap == 0:
        return -0.25
    if overlap == 1:
        return -0.05

    return 0.0

GENERIC_PATTERNS = [
    r"\bmoments?\b",
    r"\bhighlights?\b",
]

def generic_penalty(caption):
    caption = caption.lower()
    if any(re.search(p, caption) for p in GENERIC_PATTERNS):
        return -0.2
    return 0.0

CASUAL_TOKENS = [
    "bro", "nah", "actually", "lowkey", "wild",
    "this", "that", "wait", "so", "just", "crazy", 
    "genuinely", "fr"
]

def casualness_score(caption):
    score = 0.0
    words = caption.lower().split()

    if len(words) <= 10:
        score += 0.2

    if caption[0].islower():
        score += 0.15

    for t in CASUAL_TOKENS:
        if t in words:
            score += 0.1
            break

    return score

def length_score(caption, platform="tiktok"):
    length = len(caption)

    # sweet spots
    if platform == "tiktok":
        if 15 <= length <= 45:
            return 0.25
        if length < 10:
            return -0.1
        if length > 60:
            return -0.3

    if platform == "youtube":
        if 25 <= length <= 70:
            return 0.2
        if length > 90:
            return -0.4

    return 0.0

def specificity_score(caption):
    score = 0.0

    # numbers feel concrete
    if any(c.isdigit() for c in caption):
        score += 0.15

    # capitalized words (entities, names)
    caps = sum(1 for w in caption.split() if w[:1].isupper())
    if caps >= 2:
        score += 0.2

    return score

HOOK_FAMILIES = {
    "shock": [
        "no way",
        "what??",
        "that ending",
    ],
    "reaction": [
        "i wasn’t ready",
        "lowkey blew my mind",
        "genuinely crazy",
        "fr",
    ],
    "bait": [
        "bro thought",
        "this changed",
        "you won’t believe",
        "the truth",
    ]
}

def hook_pattern_score(caption):
    lower = caption.lower()
    score = 0.0

    for patterns in HOOK_FAMILIES.values():
        for p in patterns:
            if p in lower:
                score += 0.25
                break  # only once per family

    return min(score, 0.6)

def hook_template_penalty(caption):
    lower = caption.lower()
    matched_families = 0
    matched_phrases = 0

    for family, patterns in HOOK_FAMILIES.items():
        family_hit = False
        for p in patterns:
            if p in lower:
                matched_phrases += 1
                family_hit = True
        if family_hit:
            matched_families += 1

    penalty = 0.0

    # Too many hooks total
    if matched_phrases >= 2:
        penalty -= 0.25
    if matched_phrases >= 3:
        penalty -= 0.5

    # Too many hook TYPES
    if matched_families >= 2:
        penalty -= 0.2

    return penalty

def informational_density_score(caption):
    tokens = caption.split()
    nouns = sum(1 for t in tokens if len(t) > 5)
    return min(nouns * 0.15, 0.6)