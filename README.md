# Center Crop

A Dify tool that crops inward from all four edges, retaining 85% of both image width and height by default. It preserves retained pixels without resizing or adding borders. A 1024 x 1024 input produces an 870 x 870 PNG, removing 77 pixels from each edge.

Source: https://github.com/Ethan3114/dify-center-crop

Contact: ethangeng01@gmail.com

## Setup and connection requirements

No API key, provider credentials, external image-processing server, or model is required for the tool itself. Processing runs inside the Dify plugin runtime. The Dify SDK retrieves bound image files from the file URL supplied by Dify; network access to that file storage must work. No third-party image-processing service is contacted.

Install version 0.0.4 from its GitHub release or upload the `.difypkg` through **Integrations > Install > Local package**. After Marketplace approval, it will also be available through Marketplace installation. Submission does not imply approval.

## Usage

In a Workflow or Chatflow, add the **Center Crop** tool and bind `images` to an uploaded file variable (`sys.files` or a custom array of files) or an upstream node's image files. Set `ratio` to `0.85`, not `85`.

For an Agent node, add this tool to its tool list, bind `images` explicitly, and set `ratio` manually or let the Agent infer a retained fraction. The Agent needs its own tool-capable model and strategy. Configure the output node to return the actual tool file output; never rely on the model to invent a download URL.

Inputs:

- `images`: 1-5 static PNG, JPEG, or WebP files. Each image must be at most 20 MiB and 25 million pixels.
- `ratio`: retained width and height fraction from 0.01 to 1; default 0.85. Whole-pixel rounding can introduce a one-pixel difference between opposite edges.

Outputs:

- PNG file messages, with transparency retained when present.
- JSON metadata: `filename`, `width`, `height`, `ratio`, and `operation`.

Animated images and unsupported formats are rejected. EXIF orientation is applied before cropping. The tool performs no content recognition and does not guarantee removal of text or watermarks.

## Privacy

Uploaded images, names, dimensions, and crop ratios are processed in memory inside Dify. The plugin does not persist or log image content, request credentials, or send it to an external processing service. Dify controls input and output retention. See [PRIVACY.md](PRIVACY.md).

## Validation

Python 3.12 SDK loading, file message output, and pixel-exact crop checks are verified locally. Cloud testing and Marketplace review status are recorded in the submission PR. Community Edition compatibility has not yet been tested.

Chinese usage documentation: [readme/README_zh_Hans.md](readme/README_zh_Hans.md).
