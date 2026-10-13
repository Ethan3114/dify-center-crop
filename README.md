# Center Crop v0.0.5

A Dify tool for autonomous Agents: receive the image URL returned by an image-generation tool, download it, and retain the central 85% of both width and height. No resizing or padding. A 1024×1024 input produces an 870×870 PNG.

## Install

In Dify choose **Integrations > Install > GitHub**, enter `https://github.com/Ethan3114/dify-center-crop`, select `v0.0.5` and `center_crop-0.0.5.difypkg`. Alternatively download the package from the release and use local-package installation. The package is unsigned and has not been reviewed by Dify Marketplace.

## Autonomous Agent setup

1. Add **Center Crop / center_crop** to the existing Agent's tools.
2. Allow the model to supply `image_url`; leave optional `images` empty.
3. Use numeric `ratio=0.85`.
4. After image generation succeeds, instruct the Agent to pass the exact generated HTTPS image URL to this tool and display its actual output PNG. No workflow or separate download tool is needed.

See the [Chinese Agent prompt](examples/hotspot-agent-prompt-zh.md) and [Chinese usage guide](readme/README_zh_Hans.md).

## Inputs and outputs

- `image_url`: optional public HTTPS image URL on port 443; takes precedence over uploaded files. Signed query parameters are preserved.
- `images`: optional list of 1–5 Dify image files, used when image_url is absent. Supply at least one input mode.
- `ratio`: retained width and height fraction, numeric 0.01–1, default 0.85.
- Output: cropped PNG file messages plus JSON metadata (`filename`, `width`, `height`, `ratio`, `operation`). Only use an output URL if Dify actually exposes it; never reuse the input URL as a cropped result.

Supports static PNG, JPEG and WebP, up to 20 MiB and 25 million pixels. EXIF orientation is applied before cropping; transparency is preserved. Whole-pixel rounding may cause opposite borders to differ by one pixel. This geometric crop does not guarantee removal of text or watermarks.

## Download and privacy

Public HTTPS targets are validated, including each redirect, and the TLS connection is pinned to a validated public IP while preserving hostname certificate verification. Download size is bounded. No API keys or cookies are sent by the tool. Processing happens in memory inside Dify's plugin runtime; no external image-processing service is used. See [PRIVACY.md](PRIVACY.md).

## Development and validation

Requires Python 3.12 and the official Dify Plugin CLI:

```sh
pip install -r requirements.txt
dify plugin package . -o center_crop-0.0.5.difypkg
```

Local SDK loading, mock URL transport, pixel-exact PNG output, legacy file input, public-address checks and download limits passed. Live cloud Agent invocation and file rendering remain unverified. The author identifier is `ethan3114`; repository owner is `Ethan3114`.
