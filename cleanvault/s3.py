"""Minimalny klient S3 (AWS S3, Backblaze B2, MinIO i inne zgodne usługi).

Świadomie własny, a nie ``boto3``: potrzebujemy pięciu operacji (zapis, odczyt,
sprawdzenie, lista, usunięcie), a ``boto3`` z ``botocore`` ważą kilkadziesiąt MB
w pakiecie Sklepu. Podpis żądań to AWS Signature Version 4 — test porównuje go
z podpisem liczonym przez oficjalną bibliotekę AWS (``botocore``) dla tych
samych żądań.

Połączenia są utrzymywane osobno dla każdego wątku (keep-alive): przy setkach
tysięcy małych obiektów zestawianie TLS od nowa dla każdego pliku kosztowałoby
więcej niż samo przesłanie danych.
"""

from __future__ import annotations

import hashlib
import hmac
import http.client
import ssl
import threading
import time
import urllib.parse
import xml.etree.ElementTree as ET
from collections.abc import Iterator
from dataclasses import dataclass

from .i18n import tr
from .log import get_logger

log = get_logger("s3")

EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
_RETRIES = 4
_TIMEOUT = 60


class S3Error(Exception):
    """Błąd usługi S3 albo połączenia."""

    def __init__(self, message: str, status: int = 0, code: str = "") -> None:
        super().__init__(message)
        self.status = status
        self.code = code


class NotFound(S3Error):
    pass


@dataclass
class S3Target:
    """Gdzie trzymamy kopię poza domem. Klucza tajnego tu nie ma — leży w magazynie systemowym."""

    endpoint: str  # np. https://s3.eu-central-003.backblazeb2.com
    region: str  # np. eu-central-003
    bucket: str
    access_key: str
    prefix: str = ""  # „folder” w kubełku, np. "komputer-domowy"
    virtual_host: bool = False  # adres w stylu bucket.host zamiast host/bucket

    def to_dict(self) -> dict:
        return {
            "endpoint": self.endpoint,
            "region": self.region,
            "bucket": self.bucket,
            "access_key": self.access_key,
            "prefix": self.prefix,
            "virtual_host": self.virtual_host,
        }

    @classmethod
    def from_dict(cls, raw: dict) -> S3Target:
        return cls(
            endpoint=str(raw.get("endpoint", "")),
            region=str(raw.get("region", "")),
            bucket=str(raw.get("bucket", "")),
            access_key=str(raw.get("access_key", "")),
            prefix=str(raw.get("prefix", "")).strip("/"),
            virtual_host=bool(raw.get("virtual_host", False)),
        )


# ------------------------------------------------------------------ podpis


def _quote(text: str, safe: str = "") -> str:
    """Kodowanie URI według RFC 3986 — tak, jak wymaga SigV4."""
    return urllib.parse.quote(text, safe=safe + "-_.~")


def _hmac(key: bytes, text: str) -> bytes:
    return hmac.new(key, text.encode("utf-8"), hashlib.sha256).digest()


def sign(
    method: str,
    host: str,
    path: str,
    query: dict[str, str],
    headers: dict[str, str],
    payload_hash: str,
    access_key: str,
    secret_key: str,
    region: str,
    amz_date: str,
    service: str = "s3",
) -> str:
    """Nagłówek ``Authorization`` dla żądania (AWS Signature Version 4)."""
    date = amz_date[:8]
    signed = {"host": host, **{k.lower(): v for k, v in headers.items()}}
    names = sorted(signed)
    canonical_headers = "".join(f"{name}:{' '.join(str(signed[name]).split())}\n" for name in names)
    signed_headers = ";".join(names)
    canonical_query = "&".join(
        f"{_quote(k)}={_quote(v)}" for k, v in sorted((str(k), str(v)) for k, v in query.items())
    )
    canonical_request = "\n".join(
        [method, _quote(path, safe="/"), canonical_query, canonical_headers, signed_headers, payload_hash]
    )
    scope = f"{date}/{region}/{service}/aws4_request"
    string_to_sign = "\n".join(
        ["AWS4-HMAC-SHA256", amz_date, scope, hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()]
    )
    key = _hmac(_hmac(_hmac(_hmac(("AWS4" + secret_key).encode("utf-8"), date), region), service), "aws4_request")
    signature = hmac.new(key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    return (
        f"AWS4-HMAC-SHA256 Credential={access_key}/{scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )


def _parse_time(text: str) -> float:
    """``2026-09-27T10:15:00.000Z`` → sekundy od 1970 (UTC); zapis nieznany → teraz."""
    import calendar

    try:
        return float(calendar.timegm(time.strptime(text[:19], "%Y-%m-%dT%H:%M:%S")))
    except ValueError:
        return time.time()


# ------------------------------------------------------------------ klient


class S3Client:
    def __init__(
        self, target: S3Target, secret_key: str, timeout: float = _TIMEOUT, retries: int = _RETRIES
    ) -> None:
        if not target.endpoint or not target.bucket or not target.access_key or not secret_key:
            raise S3Error(tr("Uzupełnij adres usługi, nazwę kubełka i klucze dostępu."))
        parsed = urllib.parse.urlsplit(target.endpoint if "://" in target.endpoint else "https://" + target.endpoint)
        self.target = target
        self.secret_key = secret_key
        self.secure = parsed.scheme != "http"
        base_host = parsed.netloc
        self.host = f"{target.bucket}.{base_host}" if target.virtual_host else base_host
        self._path_prefix = "" if target.virtual_host else f"/{target.bucket}"
        self._local = threading.local()
        # okno programu sprawdza połączenie krócej niż kopia w tle, która może czekać
        self.timeout = timeout
        self.retries = max(1, retries)

    # --------------------------------------------------------- połączenie

    def _connection(self) -> http.client.HTTPConnection:
        conn = getattr(self._local, "conn", None)
        if conn is None:
            if self.secure:
                conn = http.client.HTTPSConnection(self.host, timeout=self.timeout, context=ssl.create_default_context())
            else:
                conn = http.client.HTTPConnection(self.host, timeout=self.timeout)
            self._local.conn = conn
        return conn

    def _drop_connection(self) -> None:
        conn = getattr(self._local, "conn", None)
        if conn is not None:
            conn.close()
        self._local.conn = None

    def object_key(self, name: str) -> str:
        return f"{self.target.prefix}/{name}" if self.target.prefix else name

    def _request(
        self,
        method: str,
        key: str = "",
        query: dict[str, str] | None = None,
        body: bytes = b"",
        extra_headers: dict[str, str] | None = None,
    ) -> tuple[int, bytes, dict[str, str]]:
        query = query or {}
        path = self._path_prefix + ("/" + key if key else ("/" if not self._path_prefix else ""))
        payload_hash = hashlib.sha256(body).hexdigest() if body else EMPTY_SHA256
        last_error: Exception | None = None
        for attempt in range(self.retries):
            amz_date = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
            headers = {"x-amz-content-sha256": payload_hash, "x-amz-date": amz_date, **(extra_headers or {})}
            headers["Authorization"] = sign(
                method, self.host, path, query, headers, payload_hash,
                self.target.access_key, self.secret_key, self.target.region, amz_date,
            )
            url = _quote(path, safe="/")
            if query:
                url += "?" + "&".join(f"{_quote(k)}={_quote(v)}" for k, v in sorted(query.items()))
            try:
                conn = self._connection()
                conn.request(method, url, body=body or None, headers={**headers, "Host": self.host})
                response = conn.getresponse()
                data = response.read()
                status = response.status
                response_headers = {k.lower(): v for k, v in response.getheaders()}
            except (OSError, http.client.HTTPException) as exc:
                self._drop_connection()
                last_error = exc
                log.info("S3 %s %s — próba %d nieudana: %s", method, key, attempt + 1, exc)
                time.sleep(min(8.0, 0.5 * 2**attempt))
                continue
            if status >= 500 or status == 429:
                last_error = S3Error(tr("Usługa chwilowo niedostępna ({status}).").format(status=status), status)
                time.sleep(min(8.0, 0.5 * 2**attempt))
                continue
            return status, data, response_headers
        raise S3Error(
            tr("Nie udało się połączyć z usługą przechowywania: {error}").format(error=last_error)
        ) from last_error

    @staticmethod
    def _error(status: int, data: bytes) -> S3Error:
        code = message = ""
        try:
            root = ET.fromstring(data)
            code = root.findtext("Code") or ""
            message = root.findtext("Message") or ""
        except ET.ParseError:
            pass
        text = tr("Usługa odrzuciła żądanie ({status} {code}): {message}").format(
            status=status, code=code, message=message
        )
        cls = NotFound if status == 404 else S3Error
        return cls(text, status, code)

    # --------------------------------------------------------- operacje

    def put(self, name: str, data: bytes) -> None:
        status, body, _ = self._request(
            "PUT", self.object_key(name), body=data, extra_headers={"content-type": "application/octet-stream"}
        )
        if status not in (200, 201, 204):
            raise self._error(status, body)

    def get(self, name: str) -> bytes:
        status, body, _ = self._request("GET", self.object_key(name))
        if status != 200:
            raise self._error(status, body)
        return body

    def exists(self, name: str) -> bool:
        status, body, _ = self._request("HEAD", self.object_key(name))
        if status == 200:
            return True
        if status == 404:
            return False
        raise self._error(status, body)

    def delete(self, name: str) -> None:
        status, body, _ = self._request("DELETE", self.object_key(name))
        if status not in (200, 204, 404):
            raise self._error(status, body)

    def list(self, prefix: str = "") -> Iterator[tuple[str, int]]:
        """(nazwa bez prefiksu celu, rozmiar) wszystkich obiektów z danym początkiem nazwy."""
        for name, size, _modified in self.list_detailed(prefix):
            yield name, size

    def list_detailed(self, prefix: str = "") -> Iterator[tuple[str, int, float]]:
        """Jak :meth:`list`, plus czas ostatniej modyfikacji obiektu (sekundy od 1970, UTC)."""
        full_prefix = self.object_key(prefix)
        strip = len(self.object_key("")) if self.target.prefix else 0
        token = ""
        while True:
            query = {"list-type": "2", "prefix": full_prefix, "max-keys": "1000"}
            if token:
                query["continuation-token"] = token
            status, body, _ = self._request("GET", "", query=query)
            if status != 200:
                raise self._error(status, body)
            root = ET.fromstring(body)
            ns = root.tag.split("}")[0] + "}" if root.tag.startswith("{") else ""
            for item in root.findall(f"{ns}Contents"):
                key = item.findtext(f"{ns}Key") or ""
                modified = _parse_time(item.findtext(f"{ns}LastModified") or "")
                yield key[strip:], int(item.findtext(f"{ns}Size") or 0), modified
            if (root.findtext(f"{ns}IsTruncated") or "false").lower() != "true":
                return
            token = root.findtext(f"{ns}NextContinuationToken") or ""
            if not token:
                return

    def check(self) -> None:
        """Sprawdza dostęp: zapis, odczyt i usunięcie małego obiektu próbnego."""
        probe = f"tvb-proba-{int(time.time() * 1000)}"
        self.put(probe, b"Sigelith Backup")
        try:
            if self.get(probe) != b"Sigelith Backup":
                raise S3Error(tr("Usługa zwróciła inną treść niż zapisana."))
        finally:
            self.delete(probe)
