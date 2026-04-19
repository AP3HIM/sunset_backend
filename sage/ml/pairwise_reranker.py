def rerank(prompt, captions, model):
    scores = {c["caption"]: 0 for c in captions}

    for i in range(len(captions)):
        for j in range(i+1, len(captions)):
            a = captions[i]["caption"]
            b = captions[j]["caption"]

            if model.prefers(prompt, a, b):
                scores[a] += 1
            else:
                scores[b] += 1

    return sorted(captions, key=lambda c: scores[c["caption"]], reverse=True)
