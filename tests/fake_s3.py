"""Lokalny serwer zgodny z podzbiorem S3 — do testów kopii poza domem.

Obsługuje dokładnie to, czego używa :mod:`cleanvault.s3`: PUT, GET, HEAD,
DELETE i ListObjectsV2 z paginacją. Podpisu nie sprawdza kryptograficznie (to robi
osobny test na tle ``botocore``), ale pilnuje formy nagłówka ``Authorization``
i tego, że ``x-amz-content-sha256`` zgadza się z przesłaną treścią — pomyłka
w liczeniu skrótu treści to typowy powód odrzucenia żądań przez prawdziwe S3.
"""

from __future__ import annotations

import hashlib
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from xml.sax.saxutils import escape


class FakeS3:
    def __init__(self, bucket: str = "kubel", access_key: str = "AKIATEST", page_size: int = 1000) -> None:
        self.bucket = bucket
        self.access_key = access_key
        self.page_size = page_size
        self.objects: dict[str, tuple[bytes, float]] = {}
        self.requests: list[tuple[str, str]] = []
        self.fail_next = 0
        self.lock = threading.Lock()
        handler = self._handler()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    @property
    def endpoint(self) -> str:
        return f"http://127.0.0.1:{self.server.server_address[1]}"

    def __enter__(self) -> FakeS3:
        self.thread.start()
        return self

    def __exit__(self, *_exc) -> None:
        self.server.shutdown()
        self.server.server_close()

    def _handler(self):
        fake = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *_args) -> None:  # ciszej w testach
                pass

            def _reply(self, status: int, body: bytes = b"", content_type: str = "application/xml") -> None:
                self.send_response(status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                if self.command != "HEAD":
                    self.wfile.write(body)

            def _error(self, status: int, code: str, message: str) -> None:
                body = f"<Error><Code>{code}</Code><Message>{escape(message)}</Message></Error>".encode()
                self._reply(status, body)

            def _handle(self) -> None:
                length = int(self.headers.get("Content-Length") or 0)
                body = self.rfile.read(length) if length else b""
                parsed = urllib.parse.urlsplit(self.path)
                path = urllib.parse.unquote(parsed.path)
                with fake.lock:
                    fake.requests.append((self.command, path))
                    if fake.fail_next > 0:
                        fake.fail_next -= 1
                        self._error(503, "SlowDown", "Please reduce your request rate.")
                        return
                auth = self.headers.get("Authorization", "")
                if not auth.startswith(f"AWS4-HMAC-SHA256 Credential={fake.access_key}/"):
                    self._error(403, "InvalidAccessKeyId", "The AWS Access Key Id you provided does not exist.")
                    return
                if self.headers.get("x-amz-content-sha256") != hashlib.sha256(body).hexdigest():
                    self._error(400, "XAmzContentSHA256Mismatch", "The provided hash does not match.")
                    return
                prefix = f"/{fake.bucket}"
                if not path.startswith(prefix):
                    self._error(404, "NoSuchBucket", "The specified bucket does not exist.")
                    return
                key = path[len(prefix) :].lstrip("/")
                if not key and self.command == "GET":
                    self._list(urllib.parse.parse_qs(parsed.query))
                    return
                with fake.lock:
                    if self.command == "PUT":
                        fake.objects[key] = (body, time.time())
                        self._reply(200)
                    elif self.command in ("GET", "HEAD"):
                        if key not in fake.objects:
                            self._error(404, "NoSuchKey", "The specified key does not exist.")
                        else:
                            self._reply(200, fake.objects[key][0], "application/octet-stream")
                    elif self.command == "DELETE":
                        fake.objects.pop(key, None)
                        self._reply(204)
                    else:
                        self._error(405, "MethodNotAllowed", "Method not allowed.")

            def _list(self, query: dict[str, list[str]]) -> None:
                prefix = query.get("prefix", [""])[0]
                token = query.get("continuation-token", [""])[0]
                with fake.lock:
                    keys = sorted(k for k in fake.objects if k.startswith(prefix) and k > token)
                    page = keys[: fake.page_size]
                    truncated = len(keys) > len(page)
                    items = "".join(
                        "<Contents><Key>{}</Key><Size>{}</Size><LastModified>{}</LastModified></Contents>".format(
                            escape(k),
                            len(fake.objects[k][0]),
                            time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(fake.objects[k][1])),
                        )
                        for k in page
                    )
                next_token = f"<NextContinuationToken>{escape(page[-1])}</NextContinuationToken>" if truncated else ""
                body = (
                    '<?xml version="1.0" encoding="UTF-8"?>'
                    '<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">'
                    f"<IsTruncated>{'true' if truncated else 'false'}</IsTruncated>{items}{next_token}"
                    "</ListBucketResult>"
                ).encode()
                self._reply(200, body)

            do_GET = do_PUT = do_HEAD = do_DELETE = _handle

        return Handler
