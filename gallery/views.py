from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from .utils import load_config, fetch_bytes, make_thumbnail
from urllib.parse import urlparse

cfg = load_config()

def index(request):
    # show allowed domains in template
    context = {"allowed_domains": cfg.get("allowed_domains", [])}

    if request.method == "POST":
        url = request.POST.get("url")
        if not url:
            return HttpResponseBadRequest("Missing url")

        host = urlparse(url).hostname or ""
        if host not in cfg.get("allowed_domains", []):
            return HttpResponseBadRequest("domain not allowed")

        try:
            b = fetch_bytes(url)
            thumb_buf = make_thumbnail(
                b,
                thumb_size=tuple(cfg["thumbnail"]["size"]),
                watermark_text=cfg["watermark"]["text"],
            )
            return HttpResponse(thumb_buf.getvalue(), content_type="image/jpeg")
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=500)

    return render(request, "gallery/index.html", context=context)

