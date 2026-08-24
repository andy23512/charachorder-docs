#!/usr/bin/env python3
"""Refresh the cached CCOS Firmware Meta API snapshots under docs/_data/ccos/.

The docs build never touches the network; it reads the JSON committed here.
Run this script (or the scheduled workflow that wraps it) to pull new data.

    python3 scripts/update_ccos_meta.py                # latest stable per device
    python3 scripts/update_ccos_meta.py --version 3.0.0
    python3 scripts/update_ccos_meta.py --pre-releases # include rc/beta builds

Upstream API: https://github.com/CharaChorder/CCOS-firmware#firmware-meta-api
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_ROOT = "https://charachorder.io/firmware"
DATA_DIR = Path(__file__).resolve().parent.parent / "docs" / "_data" / "ccos"
DEVICES_FILE = DATA_DIR / "devices.json"
INDEX_FILE = DATA_DIR / "index.json"
TIMEOUT = 30


def fetch_json(url):
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise


def listing(path):
    """The API returns nginx autoindex JSON; we only want directory names.

    The trailing slash is required -- without it the server answers 404.
    """
    url = f"{API_ROOT}/{path}/" if path else f"{API_ROOT}/"
    entries = fetch_json(url) or []
    return [e["name"] for e in entries if e.get("type") == "directory"]


def version_key(version):
    """Sort semver-ish strings so 3.0.0 > 3.0.0-rc.2 > 2.9.0, and rc.10 > rc.2."""
    core, _, pre = version.partition("-")
    numbers = []
    for part in core.split("."):
        numbers.append(int(part) if part.isdigit() else 0)
    while len(numbers) < 3:
        numbers.append(0)
    # A release outranks any of its own pre-releases.
    pre_parts = []
    if pre:
        for part in pre.replace(".", " ").split():
            pre_parts.append((0, int(part), "") if part.isdigit() else (1, 0, part))
    return (numbers, 0 if pre else 1, pre_parts)


def is_stable(version):
    return "-" not in version


def normalize(settings_meta, factory_settings):
    """Join a version's settings definitions with its factory default values.

    The Meta API keeps the two apart: settings.json describes each setting,
    factory_settings.json is a sparse array indexed by setting id. Merging them
    is what turns "id 34, range [0,255]" into a row a reader can act on.
    """
    defaults = factory_settings.get("settings") or []
    result = {}
    for group in settings_meta:
        group_name = group.get("name", "")
        for item in group.get("items", []):
            item_id = item["id"]
            raw_default = defaults[item_id] if item_id < len(defaults) else None
            result[f"{group_name}/{item.get('name', item_id)}"] = {
                "id": item_id,
                "group": group_name,
                "group_cmd": group.get("cmd"),
                "name": item.get("name"),
                "cmd": item.get("cmd"),
                "range": item.get("range"),
                "step": item.get("step"),
                "unit": item.get("unit"),
                "scale": item.get("scale"),
                "enum": item.get("enum"),
                "description": item.get("description"),
                "default": raw_default,
            }
    return result


def normalize_actions(categories):
    """Flatten actions.json into the fields the docs actually show.

    The raw file carries per-key rendering hints for Device Manager (icons,
    keyCode, variant) plus a few upstream typos (`sparator`, `variantOf`),
    none of which belong in a printed action code table.
    """
    result = []
    for category in categories:
        actions = []
        for code, action in category.get("actions", {}).items():
            actions.append(
                {
                    "code": int(code),
                    "id": action.get("id"),
                    "name": action.get("name"),
                    "display": action.get("display"),
                    "description": action.get("title") or action.get("description"),
                }
            )
        actions.sort(key=lambda a: a["code"])
        result.append(
            {
                "name": category.get("name"),
                "description": category.get("description") or None,
                "actions": actions,
            }
        )
    return result


def snapshot_device(device, version):
    base = f"{API_ROOT}/{device}/{version}"
    meta = fetch_json(f"{base}/meta.json")
    if meta is None:
        return None
    settings_file = meta.get("settings") or "settings.json"
    factory_file = (meta.get("factory_defaults") or {}).get("settings") or "factory_settings.json"
    settings_meta = fetch_json(f"{base}/{settings_file}")
    factory_settings = fetch_json(f"{base}/{factory_file}")
    if settings_meta is None or factory_settings is None:
        return None
    return {
        "git_commit": meta.get("git_commit"),
        "git_date": meta.get("git_date"),
        "settings": normalize(settings_meta, factory_settings),
        "actions_file": f"{base}/{meta.get('actions') or 'actions.json'}",
    }


def write_snapshot(path, payload, sort_keys=False):
    """Write payload, reusing the previous fetched_at when nothing else moved.

    A timestamp that is new on every run would make the scheduled job open a
    pull request every week whose only content is the clock. Keeping the old
    timestamp leaves the file byte-identical, so a pull request shows up only
    when CCOS actually changed something.
    """
    stripped = {k: v for k, v in payload.items() if k != "fetched_at"}
    if path.exists():
        try:
            previous = json.loads(path.read_text())
        except json.JSONDecodeError:
            previous = None
        if previous and {k: v for k, v in previous.items() if k != "fetched_at"} == stripped:
            payload = dict(payload, fetched_at=previous.get("fetched_at", payload["fetched_at"]))
    path.write_text(json.dumps(payload, indent=1, sort_keys=sort_keys) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", help="snapshot this exact version instead of the latest")
    parser.add_argument("--pre-releases", action="store_true", help="allow rc/beta versions")
    args = parser.parse_args()

    known = json.loads(DEVICES_FILE.read_text())["devices"]

    available = listing("")
    unknown = [d for d in available if d not in known]
    if unknown:
        print(f"warning: API lists devices missing from devices.json: {', '.join(unknown)}", file=sys.stderr)

    by_version = {}
    for device in available:
        if device not in known:
            continue
        versions = listing(device)
        if not args.pre_releases:
            versions = [v for v in versions if is_stable(v)]
        if args.version:
            versions = [v for v in versions if v == args.version]
        if not versions:
            print(f"  {device}: no matching version, skipped", file=sys.stderr)
            continue
        target = max(versions, key=version_key)
        data = snapshot_device(device, target)
        if data is None:
            print(f"  {device} {target}: metadata incomplete, skipped", file=sys.stderr)
            continue
        by_version.setdefault(target, {})[device] = data
        print(f"  {device} {target}: {len(data['settings'])} settings")

    if not by_version:
        print("nothing fetched; leaving cache untouched", file=sys.stderr)
        return 1

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for version, devices in by_version.items():
        # actions.json is identical across every device of a given release, so
        # it is fetched once per version rather than once per device.
        actions = []
        for url in [device.pop("actions_file") for device in devices.values()]:
            raw = fetch_json(url)
            if raw:
                actions = normalize_actions(raw)
                break
        print(f"  {version}: {sum(len(c['actions']) for c in actions)} action codes")

        payload = {
            "version": version,
            "fetched_at": fetched_at,
            "actions": actions,
            "devices": devices,
        }
        path = DATA_DIR / f"{version}.json"
        write_snapshot(path, payload, sort_keys=True)
        print(f"wrote {path.relative_to(DATA_DIR.parent.parent.parent)}")

    versions = sorted(
        {p.stem for p in DATA_DIR.glob("*.json") if p.name not in ("devices.json", "index.json")},
        key=version_key,
        reverse=True,
    )
    write_snapshot(
        INDEX_FILE,
        {"fetched_at": fetched_at, "default_version": versions[0], "versions": versions},
    )
    print(f"wrote {INDEX_FILE.relative_to(DATA_DIR.parent.parent.parent)} (default {versions[0]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
