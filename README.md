# Center Crop

A Dify tool plugin that retains the central portion of an image. By default it retains 85% of both width and height. It crops existing pixels without resampling, adding a canvas, or calling an external image processing API.

For a 1024×1024 image, the result is 870×870 with 77 pixels removed from each edge. It supports static PNG, JPEG and WebP, up to 20 MiB and 25 million pixels per image, with up to five input files per call. Width and height are rounded to whole pixels.

## Installation and Agent setup

In Dify choose Plugins → Install Plugin → From GitHub, enter `https://github.com/Ethan3114/dify-center-crop`, select release `v0.0.2` and the `center_crop-0.0.2.difypkg` asset. Source code alone is not an installable release. See [Dify's GitHub publishing guide](https://docs.dify.ai/en/develop-plugin/publishing/marketplace-listing/release-to-individual-github-repo).

1. Install from GitHub as above, or download `center_crop-0.0.2.difypkg` from the release and upload it via local-file installation.
2. In a Chatflow, enable image uploads and add an Agent node.
3. Add **Center Crop** to the Agent's tools. Bind `images` to `sys.files` or to image files returned by an upstream node. This parameter is explicitly configured, rather than inferred by the LLM.
4. Set `ratio` manually to `0.85`, or let the Agent infer it from the user's instruction. Do not enter `85`.
5. Instruct the Agent to call Center Crop for inward cropping requests and return the resulting PNG file. Use the Agent node's file outputs in the Answer node's image/file output configuration.
6. Upload the example image and verify a 870×870 result with no added margins. Consult the Chinese guide for details.

The package is unsigned and has not been reviewed by the Dify Marketplace. Acceptance depends on the workspace's installation policy. If upload reports a signature or policy error, remote debugging can be used for temporary testing if available; a reviewed Marketplace release is the permanent distribution path when private installation is disallowed. Do not change self-hosted environment variables on Dify Cloud. A remote debug process must remain running and is not a permanent cloud deployment.

## Development

Requires Python 3.12 and the official Dify Plugin CLI.

```sh
pip install -r requirements.txt
dify plugin package . -o center_crop-0.0.2.difypkg
```

For optional remote debugging, copy `.env.example` to `.env`, fill in the address and key from Dify's plugin debug dialog, and run `python -m main`. Never include `.env` in a package or send debug keys in a prompt.

The author is `Ethan3114`. If publishing under another account, update it consistently in the manifest, provider and tool YAML files, then rebuild.

Local validation covers Python 3.12, SDK configuration loading and tool invocation. A live cloud installation and Agent invocation are still required before claiming end-to-end compatibility.

## References

- [Tool plugins](https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/tool-plugin)
- [File outputs](https://docs.dify.ai/en/develop-plugin/features-and-specs/plugin-types/tool)
- [Distribution methods](https://docs.dify.ai/en/develop-plugin/publishing/marketplace-listing/release-overview)
