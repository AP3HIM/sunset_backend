def mutate_caption(base, template):
    core = base.lower()
    variants = []

    # Keep original
    variants.append(template)

    # Short punchy
    variants.append(core.capitalize())
    variants.append(core.capitalize() + ".")

    # Social tone
    variants.append(f"bro thought this was over 💀")
    variants.append(f"This actually happened…")

    # Curiosity (light)
    variants.append(f"You won’t believe how {core}")
    variants.append(f"This changed how I see {core}")
    variants.append(f"This is genuinely crazy: {core}")
    variants.append(f"Lowkey blew my mind: {core}")
    variants.append(f"ts is overly crazy: {core}")

    # Ultra-short fragments
    variants.append("that ending.")
    variants.append("no way this happened.")
    variants.append("what??")

    # POV / reaction
    variants.append("I still can’t believe this fr")
    variants.append("I wasn’t ready for this at ALL")

    # Anti-hook (flat but strong)
    variants.append(core.replace("ending", "finish"))

    variants.append(f"{core} but watch the last second")
    variants.append(f"{core} explained simply")
    variants.append(f"{core} in under 30 seconds")

    return list(set(variants))
