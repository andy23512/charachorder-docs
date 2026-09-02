#!/usr/bin/env python3
"""Refresh the cached CCOS changelog snapshot at docs/_data/ccos/changelog.json.

For every stable release of the docs_default devices, this pulls
changelog.json (features/fixes) and meta.json (git_date) from the Firmware
Meta API, then merges entries that read identically across devices so a
single "3.0.0" version only lists a fix once even if six devices shipped it.
The docs build never touches the network; it reads the JSON committed here.

    python3 scripts/update_ccos_changelog.py

Upstream API: https://github.com/CharaChorder/CCOS-firmware#firmware-meta-api
"""

import sys
import urllib.error
from datetime import datetime, timezone

from update_ccos_meta import (
    API_ROOT,
    DATA_DIR,
    fetch_json,
    is_stable,
    listing,
    version_key,
    write_snapshot,
)

CHANGELOG_FILE = DATA_DIR / "changelog.json"


def fetch_json_lenient(url):
    """Older firmware versions 500 rather than 404 when a file is missing."""
    try:
        return fetch_json(url)
    except urllib.error.HTTPError:
        return None


def target_devices():
    import json

    catalogue = json.loads((DATA_DIR / "devices.json").read_text())["devices"]
    return [slug for slug, info in catalogue.items() if info.get("docs_default")]


def merge_entries(entries_by_device):
    """Group entries by (summary, description) so identical text across
    devices collapses into one row tagged with every device that has it.
    """
    devices_by_key = {}
    order = []
    for device, entries in entries_by_device.items():
        for entry in entries:
            key = (entry.get("summary", ""), entry.get("description", ""))
            if key not in devices_by_key:
                devices_by_key[key] = []
                order.append(key)
            devices_by_key[key].append(device)
    return [
        {"summary": summary, "description": description, "devices": devices_by_key[(summary, description)]}
        for summary, description in order
    ]


def snapshot_version(devices, version):
    changelogs = {}
    dates = []
    for device in devices:
        changelog = fetch_json_lenient(f"{API_ROOT}/{device}/{version}/changelog.json")
        if changelog is None:
            continue
        changelogs[device] = changelog
        meta = fetch_json_lenient(f"{API_ROOT}/{device}/{version}/meta.json")
        if meta and meta.get("git_date"):
            dates.append(meta["git_date"])
    if not changelogs:
        return None
    return {
        "version": version,
        "date": min(dates) if dates else None,
        "devices": sorted(changelogs),
        "features": merge_entries({d: c.get("features", []) for d, c in changelogs.items()}),
        "fixes": merge_entries({d: c.get("fixes", []) for d, c in changelogs.items()}),
    }


def main():
    devices = target_devices()

    stable_versions_by_device = {}
    all_versions = set()
    for device in devices:
        stable = [v for v in listing(device) if is_stable(v)]
        stable_versions_by_device[device] = set(stable)
        all_versions.update(stable)

    results = []
    for version in sorted(all_versions, key=version_key, reverse=True):
        shipped_on = [d for d in devices if version in stable_versions_by_device[d]]
        snapshot = snapshot_version(shipped_on, version)
        if snapshot is None:
            print(f"  {version}: no changelog data on any device, skipped", file=sys.stderr)
            continue
        print(
            f"  {version}: {len(snapshot['devices'])} devices, "
            f"{len(snapshot['features'])} feature entries, {len(snapshot['fixes'])} fix entries"
        )
        results.append(snapshot)

    if not results:
        print("nothing fetched; leaving cache untouched", file=sys.stderr)
        return 1

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "devices": devices,
        "versions": results,
    }
    write_snapshot(CHANGELOG_FILE, payload)
    print(f"wrote {CHANGELOG_FILE.relative_to(DATA_DIR.parent.parent.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
