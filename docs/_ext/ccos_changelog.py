"""Render the CCOS Releases page from the cached Firmware Meta API changelog.

Usage in an .rst file::

    .. ccos-releases::

Data comes from docs/_data/ccos/changelog.json, refreshed by
scripts/update_ccos_changelog.py -- the build itself never hits the network.
"""

import json
import re
from pathlib import Path

from docutils import nodes
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

__version__ = "0.1.0"


def plain_text(value):
    """Flatten an API description into plain text.

    Mirrors ccos_meta.plain_text: a few descriptions carry inline HTML
    (`<b>`, `<kbd>`, and at least one unbalanced `<b/>`), which docutils
    would otherwise render as literal angle brackets. Tags are replaced with
    a space, not dropped outright, so adjacent tags like
    `<kbd>CTRL</kbd><kbd>RIGHT</kbd>` don't fuse into "CTRLRIGHT".
    """
    return " ".join(re.sub(r"<[^>]*>", " ", value or "").split())

logger = logging.getLogger(__name__)


def data_dir(env):
    return Path(env.srcdir) / env.config.ccos_data_dir


def load_changelog(env):
    path = data_dir(env) / "changelog.json"
    env.note_dependency(str(path))
    if not path.is_file():
        return None
    return json.loads(path.read_text())


def device_names(env):
    path = data_dir(env) / "devices.json"
    env.note_dependency(str(path))
    return json.loads(path.read_text())["devices"]


def device_label(catalogue, slugs, all_slugs):
    if set(slugs) == set(all_slugs):
        return None
    names = [catalogue.get(s, {}).get("name", s) for s in slugs]
    return ", ".join(names)


def entry_nodes(entry, catalogue, version_devices):
    """Build the nodes for one changelog entry.

    Uses a rubric rather than a nested section: the same fix summary can
    legitimately recur across versions (e.g. a regression fixed twice), which
    would otherwise collide as duplicate autosectionlabel targets. Rubrics
    also keep the page's "on this page" outline to version-level headings
    instead of one entry per feature/fix.
    """
    summary = plain_text(entry["summary"]) or "Untitled"
    result = [nodes.rubric(text=summary)]
    label = device_label(catalogue, entry["devices"], version_devices)
    if label:
        result.append(
            nodes.paragraph(text=f"Applies to: {label}.", classes=["ccos-changelog-scope"])
        )
    description = (entry.get("description") or "").strip()
    if description:
        for paragraph in description.split("\n\n"):
            text = plain_text(paragraph)
            if text:
                result.append(nodes.paragraph(text=text))
    return result


class CcosReleasesDirective(SphinxDirective):
    """Emit one section per cached stable CCOS release."""

    def run(self):
        env = self.env
        changelog = load_changelog(env)
        if changelog is None:
            logger.warning(
                "ccos-releases: docs/_data/ccos/changelog.json is missing; "
                "run scripts/update_ccos_changelog.py",
                location=self.get_location(),
            )
            return []

        catalogue = device_names(env)
        result = []
        for version in changelog["versions"]:
            version_devices = version["devices"]
            names = [catalogue.get(s, {}).get("name", s) for s in version_devices]
            section = nodes.section(ids=[nodes.make_id(f"ccos-release-{version['version']}")])
            section += nodes.title(text=version["version"])
            date = (version.get("date") or "").split("T")[0]
            subtitle = ", ".join(names)
            if date:
                subtitle = f"{date} — {subtitle}"
            section += nodes.paragraph(text=subtitle, classes=["ccos-changelog-devices"])

            if version["features"]:
                section += nodes.rubric(text="Features", classes=["ccos-changelog-group"])
                for entry in version["features"]:
                    section += entry_nodes(entry, catalogue, version_devices)
            if version["fixes"]:
                section += nodes.rubric(text="Fixes", classes=["ccos-changelog-group"])
                for entry in version["fixes"]:
                    section += entry_nodes(entry, catalogue, version_devices)
            result.append(section)
        return result


def setup(app):
    app.add_directive("ccos-releases", CcosReleasesDirective)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
