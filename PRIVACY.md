# Privacy

Version 0.0.5 also accepts an Agent-provided public HTTPS image URL. It downloads the image from that URL's host, without sending API keys, cookies, or image contents to another processing service. Each redirect is validated against public network addresses, and the download is limited to 20 MiB. The source host can observe the request from Dify's infrastructure and receives the URL path and query parameters needed to download the image. URLs are not logged by this plugin.

This plugin reads image files provided to it by the Dify application. The SDK retrieves their bytes from Dify's configured file storage, and the plugin crops them in memory inside the Dify plugin runtime. It returns PNG bytes and dimensions to Dify. It does not send images to any external image-processing service, request an image-processing API key, log image bytes, or use persistent plugin storage.

On Dify Cloud, processing runs on Dify's infrastructure, not on the user's device. Input and output file retention are governed by Dify and the workspace's settings. This plugin does not alter those policies.
