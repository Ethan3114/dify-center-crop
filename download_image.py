"""Fetch public HTTPS images with bounded size and validated redirects."""
import http.client
import ipaddress
import socket
import ssl
from pathlib import PurePosixPath
from urllib.parse import unquote, urljoin, urlsplit

from crop_image import MAX_FILE_BYTES


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host: str, address: str):
        super().__init__(host, port=443, timeout=15, context=ssl.create_default_context())
        self._address = address

    def connect(self):
        sock = socket.create_connection((self._address, 443), timeout=self.timeout)
        try:
            self.sock = self._context.wrap_socket(sock, server_hostname=self.host)
        except Exception:
            sock.close()
            raise


def _public_target(url: str):
    if not isinstance(url, str) or len(url) > 16384 or any(ord(c) < 32 for c in url):
        raise ValueError("image_url must be a valid public HTTPS URL.")
    parts = urlsplit(url)
    if (parts.scheme != "https" or not parts.hostname or parts.username is not None
            or parts.password is not None or parts.port not in (None, 443)):
        raise ValueError("Only public HTTPS image URLs on port 443 are supported.")
    host = parts.hostname.encode("idna").decode("ascii")
    addresses = list(dict.fromkeys(
        item[4][0] for item in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    ))
    if not addresses or any(not ipaddress.ip_address(a).is_global for a in addresses):
        raise ValueError("Private, local and reserved network addresses are not allowed.")
    return parts, host, addresses[0]


def download_image(url: str) -> tuple[bytes, str]:
    for attempt in range(6):
        parts, host, address = _public_target(url)
        connection = _PinnedHTTPSConnection(host, address)
        try:
            target = parts.path or "/"
            if parts.query:
                target += "?" + parts.query
            connection.request("GET", target, headers={
                "Accept": "image/png,image/jpeg,image/webp",
                "User-Agent": "Dify-Center-Crop/0.0.5",
            })
            response = connection.getresponse()
            if response.status in (301, 302, 303, 307, 308):
                location = response.getheader("Location")
                if not location or attempt == 5:
                    raise ValueError("Image download exceeded the redirect limit.")
                url = urljoin(url, location)
                continue
            if not 200 <= response.status < 300:
                raise ValueError(f"Image download failed (HTTP {response.status}).")
            length = response.getheader("Content-Length")
            if length is not None and (int(length) < 0 or int(length) > MAX_FILE_BYTES):
                raise ValueError("Each image must be at most 20 MiB.")
            data = response.read(MAX_FILE_BYTES + 1)
            if not data or len(data) > MAX_FILE_BYTES:
                raise ValueError("Downloaded image is empty or exceeds 20 MiB.")
            name = PurePosixPath(unquote(parts.path)).name or "generated_image"
            return data, name
        finally:
            connection.close()
    raise ValueError("Unable to download image.")
