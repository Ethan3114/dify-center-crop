"""从四边向内裁切，保留中央宽高各 85% 的画面。"""
from io import BytesIO
import math
from pathlib import Path

from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = 25_000_000
MAX_FILE_BYTES = 20 * 1024 * 1024


def crop_image(data: bytes, ratio: float = 0.85) -> bytes:
    if not math.isfinite(ratio) or not 0 < ratio <= 1:
        raise ValueError("ratio 必须大于 0 且不超过 1；保留 85% 请传 0.85")
    if not data or len(data) > MAX_FILE_BYTES:
        raise ValueError("图片不能为空，且不能超过 20 MiB")
    with Image.open(BytesIO(data)) as source:
        if source.format not in {"PNG", "JPEG", "WEBP"}:
            raise ValueError("仅支持 PNG、JPEG、WebP 静态图片")
        if getattr(source, "is_animated", False):
            raise ValueError("请上传静态图片")
        image = ImageOps.exif_transpose(source)
        width, height = image.size
        if width * height > Image.MAX_IMAGE_PIXELS:
            raise ValueError("图片像素不能超过 2500 万")
        # 像素必须是整数；四舍五入到最接近的尺寸。
        size = (max(1, int(width * ratio + 0.5)), max(1, int(height * ratio + 0.5)))
        # 奇数裁切差值时，左右或上下最多相差 1 像素。
        left = (width - size[0]) // 2
        top = (height - size[1]) // 2
        mode = "RGBA" if "A" in image.getbands() or "transparency" in image.info else "RGB"
        cropped = image.convert(mode).crop((left, top, left + size[0], top + size[1]))
        output = BytesIO()
        cropped.save(output, format="PNG")
        return output.getvalue()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--ratio", type=float, default=0.85)
    args = parser.parse_args()
    args.output.write_bytes(crop_image(args.input.read_bytes(), args.ratio))
    print(f"已保存：{args.output}")
