from collections.abc import Generator
from io import BytesIO
import math
from pathlib import Path
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.file.file import File
from PIL import Image, UnidentifiedImageError

from crop_image import MAX_FILE_BYTES, crop_image
from download_image import download_image


class CenterCropTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        images = tool_parameters.get("images")
        image_url = tool_parameters.get("image_url")
        raw_ratio = tool_parameters.get("ratio")
        try:
            ratio = 0.85 if raw_ratio is None else float(raw_ratio)
        except (TypeError, ValueError) as exc:
            raise ValueError("ratio must be a number such as 0.85.") from exc
        if not math.isfinite(ratio) or not 0.01 <= ratio <= 1:
            raise ValueError("ratio must be between 0.01 and 1; use 0.85 for 85%.")

        inputs = []
        if image_url:
            # A generated URL takes precedence over previously configured upload files.
            try:
                inputs.append(download_image(image_url))
            except ValueError:
                raise
            except Exception as exc:
                raise ValueError("Unable to download image; check that its HTTPS URL is accessible and unexpired.") from exc
        else:
            if not isinstance(images, list) or not 1 <= len(images) <= 5:
                raise ValueError("Provide image_url or bind 1-5 image files.")
            for image_file in images:
                if not isinstance(image_file, File):
                    raise ValueError("images must contain Dify file objects.")
                if image_file.size and image_file.size > MAX_FILE_BYTES:
                    raise ValueError("Each image must be at most 20 MiB.")
                try:
                    inputs.append((image_file.blob, image_file.filename or "image"))
                except Exception as exc:
                    raise ValueError("Unable to read the input image. Re-upload it and bind the file variable.") from exc

        for data, source_name in inputs:
            try:
                result = crop_image(data, ratio)
            except (UnidentifiedImageError, OSError) as exc:
                raise ValueError("Input is not a readable PNG, JPEG or WebP image.") from exc
            with Image.open(BytesIO(result)) as cropped:
                width, height = cropped.size
            stem = Path(source_name).stem
            filename = f"{stem}_crop.png"
            yield self.create_json_message({
                "filename": filename,
                "width": width,
                "height": height,
                "ratio": ratio,
                "operation": "center_crop",
            })
            yield self.create_blob_message(result, meta={
                "mime_type": "image/png",
                "filename": filename,
            })
