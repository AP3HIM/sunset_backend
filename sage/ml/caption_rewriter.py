import random
import re

def rewrite_caption(caption):
    caption = re.sub(r"#\w+", "", caption)
    caption = caption.strip()

    rules = [
        lambda c: c.replace("This", "").strip(),
        lambda c: c.replace("You won’t believe", "").strip(),
        lambda c: c.rstrip("."),
    ]

    for rule in rules:
        if random.random() < 0.4:
            caption = rule(caption)

    return caption
