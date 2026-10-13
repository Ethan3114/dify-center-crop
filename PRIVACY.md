# Privacy

This plugin reads image files provided to it by the Dify application. The SDK retrieves their bytes from Dify's configured file storage, and the plugin crops them in memory inside the Dify plugin runtime. It returns PNG bytes and dimensions to Dify. It does not send images to any external image-processing service, request an image-processing API key, log image bytes, or use persistent plugin storage.

On Dify Cloud, processing runs on Dify's infrastructure, not on the user's device. Input and output file retention are governed by Dify and the workspace's settings. This plugin does not alter those policies.
