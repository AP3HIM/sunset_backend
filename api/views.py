from django.shortcuts import render

# Create your views here.
# backend/api/views.py
import os, boto3, mimetypes, time
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  # or use proper auth
from django.utils.crypto import get_random_string

session = boto3.session.Session(
    aws_access_key_id=os.getenv("R2_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("R2_SECRET_ACCESS_KEY"),
    region_name="auto",  # R2
)
s3 = session.client("s3", endpoint_url=os.getenv("R2_ENDPOINT_URL"))
BUCKET = os.getenv("R2_BUCKET_NAME")

@csrf_exempt
@require_POST
def create_upload_url(request):
    # expected JSON: {"filename": "myvideo.mp4", "content_type": "video/mp4"}
    data = request.json if hasattr(request, "json") else None
    if data is None:
        import json; data = json.loads(request.body or "{}")

    filename = data.get("filename") or data.get("file_name") or f"upload-{int(time.time())}-{get_random_string(6)}"
    content_type = data.get("content_type") or mimetypes.guess_type(filename)[0] or "application/octet-stream"
    key = f"uploads/{filename}"

    url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={"Bucket": BUCKET, "Key": key, "ContentType": content_type},
        ExpiresIn=900,  # 15 min
    )
    # Optional: a future public URL (if bucket is public/served via R2 public URL or Worker)
    public_url = f"{os.getenv('R2_PUBLIC_BASE')}/{key}"
    return JsonResponse({"upload_url": url, "key": key, "public_url": public_url})
