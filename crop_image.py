"""Retain the central portion of an image without resizing or padding."""
from io import BytesIO
import math

from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = 25_000_000
MAX_FILE_BYTES = 20 * 1024 * 1024


def crop_image(data: bytes, ratio: float = 0.85) -> bytes:
    if not math.isfinite(ratio) or not 0 < ratio <= 1:
        raise ValueError("ratio must be greater than 0 and at most 1; use 0.85 for 85%.")
    if not data or len(data) > MAX_FILE_BYTES:
        raise ValueError("The image must be nonempty and at most 20 MiB.")
    with Image.open(BytesIO(data)) as source:
        if source.format not in {"PNG", "JPEG", "WEBP"}:
            raise ValueError("Only static PNG, JPEG, and WebP images are supported.")
        if getattr(source, "is_animated", False):
            raise ValueError("Please upload a static image.")
        image = ImageOps.exif_transpose(source)
        width, height = image.size
        if width * height > Image.MAX_IMAGE_PIXELS:
            raise ValueError("The image must contain at most 25 million pixels.")
        # Round each retained dimension to the nearest whole pixel.
        size = (max(1, int(width * ratio + 0.5)), max(1, int(height * ratio + 0.5)))
        # Opposite edges can differ by one pixel for an odd crop difference.
        left = (width - size[0]) // 2
        top = (height - size[1]) // 2
        mode = "RGBA" if "A" in image.getbands() or "transparency" in image.info else "RGB"
        cropped = image.convert(mode).crop((left, top, left + size[0], top + size[1]))
        output = BytesIO()
        cropped.save(output, format="PNG")
        return output.getvalue()

