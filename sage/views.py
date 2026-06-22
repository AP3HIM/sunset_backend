# sage/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from sage.ml.caption_generator import generate_caption_v03
#from sage.ml.caption_ranker import suggest_captions
from sage.ml.tfidf_ranker import suggest_captions

import traceback
import time

@csrf_exempt
@require_POST
def generate_captions(request):
    start = time.time()

    try:
        print("Request received")

        body = json.loads(request.body)

        base_caption = body.get("base_caption", "").strip()
        platform = body.get("platform", "youtube")

        print("Starting suggest")
        t1 = time.time()

        ranked = suggest_captions(
            base_caption,
            genre=None,
            top_k=15
        )

        print("Suggest:", time.time() - t1)

        print("Starting generation")
        t2 = time.time()

        results = generate_caption_v03(
            base_caption=base_caption,
            ranked_captions=ranked,
            genre=None,
            platform=platform,
            n=3
        )

        print("Generate:", time.time() - t2)

        print("Total:", time.time() - start)

        return JsonResponse({"captions": results})

    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        return JsonResponse(
            {
                "error": str(e),
                "traceback": tb
            },
            status=500
        )