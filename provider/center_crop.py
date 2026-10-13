from typing import Any
from dify_plugin import ToolProvider


class CenterCropProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # All processing runs in the plugin; no third-party API key is needed.
        pass
