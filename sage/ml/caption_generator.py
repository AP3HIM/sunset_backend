import re
import random

from sage.ml.caption_scorer import score_caption
from sage.ml.tag_generator import generate_tags

from sage.ml.platform_rules import platform_penalty
from sage.ml.platform_rules import repetition_penalty
# from sage.ml.platform_rules import emoji_penalty
from sage.ml.platform_rules import intent_penalty
from sage.ml.platform_rules import generic_penalty
from sage.ml.platform_rules import casualness_score
from sage.ml.platform_rules import length_score
from sage.ml.platform_rules import specificity_score
from sage.ml.platform_rules import hook_pattern_score
from sage.ml.platform_rules import informational_density_score
from sage.ml.platform_rules import hook_template_penalty

from sage.ml.feedback_scorer import feedback_score
from sage.ml.similarity import similarity_penalty

from sage.ml.pairwise_ranker import pairwise_score
from sage.ml.caption_mutator import mutate_caption

from sage.ml.gb.gb_ranker import gb_score

EMOJIS = ["🔥", "🤯", "👀", "🏈"]

def clean_caption(text):
    text = re.sub(r"#\w+", "", text)
    return re.sub(r"\s+", " ", text).strip()

def extract_core_phrase(prompt):
    """
    Returns a clean, literal phrase that MUST appear in the caption.
    """
    prompt = prompt.lower()
    words = re.findall(r"\b[a-z]{3,}\b", prompt)

    # keep last meaningful chunk
    if len(words) >= 3:
        return " ".join(words[-3:])
    return prompt

def keyword_overlap(prompt, caption, min_overlap=1):
    prompt_words = set(
        re.findall(r"\b[a-zA-Z]{4,}\b", prompt.lower())
    )
    caption_words = set(
        re.findall(r"\b[a-zA-Z]{4,}\b", caption.lower())
    )
    return len(prompt_words & caption_words) >= min_overlap


def rewrite_caption(base_caption, template):
    core = extract_core_phrase(base_caption)

    template_clean = clean_caption(template)

    # If core already appears, just return cleaned version
    if core.lower() in template_clean.lower():
        return template_clean

    # Remove trailing punctuation
    core = core.rstrip(".!?")

    # Replace vague noun phrases only
    rewritten = re.sub(
        r"(?i)\b(this|that|these|those|moment|ending|play|game)\b",
        core,
        template_clean,
        count=1
    )

    return rewritten

def generate_caption_v03(
    base_caption,
    ranked_captions,
    genre,
    platform="youtube",
    n=5
):
    candidates = []
    seen = set()

    for row in ranked_captions:
        variants = [row["caption"]]

        # Mutation is OPTIONAL, not mandatory
        if random.random() < 0.6:
            variants += mutate_caption(base_caption, row["caption"])

        for variant in variants:
            final = variant

            if not keyword_overlap(base_caption, final):
                final = rewrite_caption(base_caption, final)

            score = score_caption(final)
            score += platform_penalty(final, platform)
            score += repetition_penalty(final)
            score += generic_penalty(final)
            score += intent_penalty(final, base_caption) *0.6

            sim = similarity_penalty(base_caption, final)
            score += sim * 0.5

            score += casualness_score(final) *1.3
            score += length_score(final, platform)
            score += specificity_score(final)*1.4
            score += hook_template_penalty(final)
            score += informational_density_score(final) * 1.2

            score += feedback_score(base_caption, final) * 2
            score += 0.5 * pairwise_score(base_caption, final)

            hook_score = hook_pattern_score(final)
            score += hook_score

            heuristic = score

            gb = gb_score(base_caption, final, platform)

            score = 0.35 * heuristic + 0.65 * gb

            norm = re.sub(r"\W+", "", final.lower())
            if norm in seen:
                continue
            seen.add(norm)

            if sim < -0.65:
                continue

            candidates.append({
                "caption": final,
                "tags": generate_tags(final, genre),
                "score": score
            })

    candidates.sort(key=lambda x: x["score"], reverse=True)

    finals = []
    for cand in candidates:
        if len(finals) >= n:
            break

        overlap = 0.0
        for f in finals:
            overlap += max(
                0,
                similarity_penalty(cand["caption"], f["caption"]) * -1
            )

        # reject if too similar to already-picked captions
        if overlap > 0.6:
            continue

        finals.append(cand)

    return finals
