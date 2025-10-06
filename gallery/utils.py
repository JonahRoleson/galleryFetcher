import io
import urllib3
import yaml
from PIL import Image, ImageDraw, ImageFont

# load YAML config (demo uses FullLoader - unsafe for untrusted content)
def load_config(path="config.yaml"):
    with open(path, "r") as f:
        # Use FullLoader if available (>=5.1), otherwise fall back to yaml.Loader (5.0)
        loader = getattr(yaml, "FullLoader", yaml.Loader)
        return yaml.load(f, Loader=loader)

# fetch bytes via urllib3
def fetch_bytes(url, timeout=10.0):
    http = urllib3.PoolManager()
    r = http.request("GET", url, preload_content=True, timeout=timeout)
    if r.status != 200:
        raise ValueError(f"bad status {r.status}")
    return r.data

# create thumbnail + watermark
def make_thumbnail(image_bytes, thumb_size=(200, 200), watermark_text="GalleryFetcher"):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    img.thumbnail(thumb_size)

    # watermark layer
    txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    w, h = draw.textsize(watermark_text, font=font)
    pos = (max(0, img.size[0] - w - 8), max(0, img.size[1] - h - 8))
    draw.text(pos, watermark_text, fill=(255, 255, 255, 128), font=font)
    out = Image.alpha_composite(img, txt)

    buf = io.BytesIO()
    out.convert("RGB").save(buf, format="JPEG")
    buf.seek(0)
    return buf


def make_thumbnail(image_bytes, thumb_size=(200, 200), watermark_text="GalleryFetcher"):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    img.thumbnail(thumb_size)

    txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    # Pillow 10+: use textbbox (textsize was removed)
    try:
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        # Older Pillow fallback
        w, h = draw.textsize(watermark_text, font=font)

    pos = (max(0, img.size[0] - w - 8), max(0, img.size[1] - h - 8))
    draw.text(pos, watermark_text, fill=(255, 255, 255, 128), font=font)

    out = Image.alpha_composite(img, txt)
    buf = io.BytesIO()
    out.convert("RGB").save(buf, format="JPEG")
    buf.seek(0)
    return buf

