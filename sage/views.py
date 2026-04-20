# sage/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from sage.ml.caption_generator import generate_caption_v03
from sage.ml.caption_ranker import suggest_captions

import traceback

@csrf_exempt
@require_POST
def generate_captions(request):
    try:
        body = json.loads(request.body)
        base_caption = body.get("base_caption", "").strip()
        platform = body.get("platform", "youtube")

        if not base_caption:
            return JsonResponse({"error": "base_caption is required"}, status=400)

        ranked = suggest_captions(base_caption, genre=None, top_k=5)
        results = generate_caption_v03(
            base_caption=base_caption,
            ranked_captions=ranked,
            genre=None,
            platform=platform,
            n=3
        )

        return JsonResponse({"captions": results})

    except Exception as e:
        tb = traceback.format_exc()
        print(tb)  # prints full traceback to Django terminal
        return JsonResponse({"error": str(e), "traceback": tb}, status=500)