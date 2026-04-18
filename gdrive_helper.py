"""Google Drive helper for the ingester.

Uses the Replit Google Drive integration (connection:conn_google-drive_...).
Calls the connectors proxy to fetch a fresh OAuth access token, then talks to
the Drive v3 REST API directly.
"""
import os
import json
import re
import time
import urllib.parse
import urllib.request
import urllib.error

_HOST = os.environ.get("REPLIT_CONNECTORS_HOSTNAME", "connectors.replit.com")
_TOKEN_CACHE = {"value": None, "expires_at": 0}

LESSON_KEY_RE = re.compile(r"^G(\d)-W(\d+)-Day([AB])$", re.IGNORECASE)


def _replit_token() -> str:
    ident = os.environ.get("REPL_IDENTITY") or os.environ.get("WEB_REPL_RENEWAL")
    if not ident:
        raise RuntimeError("No REPL_IDENTITY / WEB_REPL_RENEWAL available")
    prefix = "repl" if os.environ.get("REPL_IDENTITY") else "depl"
    return f"{prefix} {ident}"


def get_access_token(force: bool = False) -> str:
    now = time.time()
    if not force and _TOKEN_CACHE["value"] and _TOKEN_CACHE["expires_at"] - 60 > now:
        return _TOKEN_CACHE["value"]
    url = f"https://{_HOST}/api/v2/connection?include_secrets=true&connector_names=google-drive"
    req = urllib.request.Request(url, headers={"X_REPLIT_TOKEN": _replit_token()})
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = json.loads(resp.read())
    items = body.get("items") or []
    if not items:
        raise RuntimeError("Google Drive connection not found for this Repl.")
    creds = (items[0].get("settings") or {}).get("oauth", {}).get("credentials", {})
    at = creds.get("access_token")
    if not at:
        raise RuntimeError("Drive access token missing in connection settings.")
    _TOKEN_CACHE["value"] = at
    expires_in = creds.get("expires_in")
    try:
        ttl = float(expires_in) if expires_in is not None else 1800.0
    except (TypeError, ValueError):
        ttl = 1800.0
    _TOKEN_CACHE["expires_at"] = now + ttl
    return at


def _drive(path: str, params: dict | None = None, accept: str = "application/json"):
    if params:
        path = f"{path}?{urllib.parse.urlencode(params)}"
    url = f"https://www.googleapis.com{path}"
    for attempt in (1, 2):
        token = get_access_token(force=(attempt == 2))
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "Accept": accept})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code == 401 and attempt == 1:
                continue
            raise


def list_folder(folder_id: str, page_size: int = 1000) -> list[dict]:
    out: list[dict] = []
    page_token = None
    while True:
        params = {
            "q": f"'{folder_id}' in parents and trashed=false",
            "fields": "nextPageToken,files(id,name,mimeType,size,modifiedTime)",
            "pageSize": str(page_size),
            "orderBy": "folder,name",
            "supportsAllDrives": "true",
            "includeItemsFromAllDrives": "true",
        }
        if page_token:
            params["pageToken"] = page_token
        body = json.loads(_drive("/drive/v3/files", params))
        out.extend(body.get("files", []))
        page_token = body.get("nextPageToken")
        if not page_token:
            break
    return out


def get_file_bytes(file_id: str) -> bytes:
    return _drive(f"/drive/v3/files/{file_id}", {"alt": "media", "supportsAllDrives": "true"})


def get_file_json(file_id: str) -> dict:
    return json.loads(get_file_bytes(file_id).decode("utf-8"))


def get_file_meta(file_id: str) -> dict:
    return json.loads(_drive(
        f"/drive/v3/files/{file_id}",
        {"fields": "id,name,mimeType,size,modifiedTime,parents", "supportsAllDrives": "true"},
    ))


def parse_lesson_key(name: str):
    """Parse 'G3-W3-DayB' -> (3, 3, 'B'). Returns None if not matching."""
    m = LESSON_KEY_RE.match(name.strip())
    if not m:
        return None
    return int(m.group(1)), int(m.group(2)), m.group(3).upper()


def scan_for_sections(folder_id: str, max_depth: int = 3) -> list[dict]:
    """Walk a folder; for any subfolder named GX-WY-Day[AB] containing
    sections.json, return a candidate descriptor."""
    found: list[dict] = []

    def walk(fid: str, path: str, depth: int):
        if depth > max_depth:
            return
        for item in list_folder(fid):
            is_folder = item["mimeType"] == "application/vnd.google-apps.folder"
            sub_path = f"{path}/{item['name']}" if path else item["name"]
            if is_folder:
                key = parse_lesson_key(item["name"])
                if key:
                    children = list_folder(item["id"])
                    sec_file = next((c for c in children if c["name"] == "sections.json"), None)
                    if sec_file:
                        grade, week, day = key
                        found.append({
                            "lesson_key": item["name"],
                            "grade": grade,
                            "week": week,
                            "day": day,
                            "folder_id": item["id"],
                            "folder_path": sub_path,
                            "sections_file_id": sec_file["id"],
                            "sections_file_name": sec_file["name"],
                            "modified_time": sec_file.get("modifiedTime"),
                        })
                walk(item["id"], sub_path, depth + 1)

    walk(folder_id, "", 0)
    return found
