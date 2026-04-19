# backend/sage/ml/gb/features.py

from sage.ml.platform_rules import (
    platform_penalty,
    repetition_penalty,
    intent_penalty,
    generic_penalty,
    casualness_score,
    length_score,
    specificity_score,
    hook_pattern_score,
    informational_density_score,
    hook_template_penalty,
)
from sage.ml.similarity import similarity_penalty


def extract_features(base, caption, platform):
    words = caption.split()

    return {
        # structure
        "num_words": len(words),
        "avg_word_len": sum(len(w) for w in words) / max(len(words), 1),

        # semantic / intent
        "similarity": similarity_penalty(base, caption),
        "intent": intent_penalty(caption, base),

        # content quality
        "specificity": specificity_score(caption),
        "informational_density": informational_density_score(caption),

        # tone
        "casualness": casualness_score(caption),
        "hook_score": hook_pattern_score(caption),
        "hook_template_penalty": hook_template_penalty(caption),

        # penalties
        "generic_penalty": generic_penalty(caption),
        "repetition_penalty": repetition_penalty(caption),
        "platform_penalty": platform_penalty(caption, platform),

        # length alignment
        "length_score": length_score(caption, platform),
    }
