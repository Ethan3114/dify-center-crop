# Center Crop v0.0.2

A Dify tool plugin for symmetric inward cropping. It retains 85% of both image width and height by default, without resizing or adding margins.

- Accepts image files from chat uploads or upstream image nodes.
- Returns PNG file messages and output dimensions.
- Supports static PNG, JPEG and WebP.
- Processes images in the Dify plugin runtime; no external image processing server or API key.
- Sets the plugin author to the repository owner's GitHub login, `Ethan3114`.

Validation: packaged with the official Dify CLI 0.6.11; configuration loading and real SDK invocation tested with Python 3.12.15, dify-plugin 0.10.2 and Pillow 12.3.0. The supplied 1024×1024 sample yields a pixel-exact 870×870 center crop.

Not yet validated: installation on the user's Dify Cloud workspace, file transfer from that workspace's storage, and image presentation in the selected Agent strategy. This release is unsigned and is not a Marketplace-reviewed release.
