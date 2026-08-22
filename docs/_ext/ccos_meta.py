"""Render CCOS setting tables from cached Firmware Meta API data.

Usage in an .rst file::

    .. ccos-setting:: mouse/slow speed

    .. ccos-setting:: chording/detection method
       :devices: one_m0, two_s3
       :version: 3.0.0

The argument is ``<settings group>/<setting name>`` exactly as the Meta API
spells it. Data comes from docs/_data/ccos/, refreshed by
scripts/update_ccos_meta.py -- the build itself never hits the network.

Tables are emitted as ordinary docutils nodes so every builder (html, latex,
epub) keeps working. On HTML they are additionally wrapped in a div carrying
the setting key, which _static/ccos-meta.js uses to swap in other firmware
versions live.
"""

import json
import re
from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

__version__ = "0.1.0"

logger = logging.getLogger(__name__)

DEFAULT_COLUMNS = ("Device", "Default", "Min. Value", "Max. Value", "Increments")
MISSING = "—"  # em dash: this device/version does not have the setting


class ccos_table(nodes.General, nodes.Element):
    """Wrapper that carries the setting key through to the HTML writer."""


def visit_ccos_table_html(self, node):
    self.body.append(
        self.starttag(
            node,
            "div",
            CLASS="ccos-table",
            **{
                "data-setting": node["setting"],
                "data-version": node["version"],
                "data-devices": ",".join(node["devices"]),
            },
        )
    )


def depart_ccos_table_html(self, node):
    self.body.append("</div>\n")


def visit_ccos_table_passthrough(self, node):
    pass


def depart_ccos_table_passthrough(self, node):
    pass


def data_dir(env):
    return Path(env.srcdir) / env.config.ccos_data_dir


def load_json(env, name):
    path = data_dir(env) / name
    env.note_dependency(str(path))
    if not path.is_file():
        return None
    return json.loads(path.read_text())


def format_number(value):
    """8.0 -> '8', 0.1 -> '0.1'. Keeps scaled values from growing a ragged tail."""
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return f"{value:.6f}".rstrip("0").rstrip(".")
    return str(value)


def format_value(value, setting, is_step=False):
    """Turn a raw firmware value into what a reader sees in the table.

    Three things can happen to a raw number: an ``enum`` setting stores an
    index into its option list, a ``scale`` setting stores a fixed-point
    integer, and a ``unit`` setting wants its unit appended.
    """
    if value is None:
        return MISSING
    options = setting.get("enum")
    if options and not is_step:
        if isinstance(value, int) and 0 <= value < len(options):
            return options[value]
        return str(value)
    scale = setting.get("scale")
    if scale:
        value = value * scale
    text = format_number(value)
    unit = setting.get("unit")
    return f"{text} {unit}" if unit else text


def setting_row(setting, columns):
    """One table row's worth of cells, keyed by the column headers in use."""
    if setting is None:
        return {c: MISSING for c in columns if c != "Device"}
    value_range = setting.get("range") or [None, None]
    step = setting.get("step")
    if step is None and not setting.get("enum") and value_range[0] is not None:
        step = 1
    return {
        "Default": format_value(setting.get("default"), setting),
        "Min. Value": format_value(value_range[0], setting, is_step=True),
        "Max. Value": format_value(value_range[1], setting, is_step=True),
        "Increments": format_value(step, setting, is_step=True),
        "Setting ID": str(setting["id"]),
    }


def build_table(columns, rows):
    table = nodes.table(classes=["colwidths-auto"])
    group = nodes.tgroup(cols=len(columns))
    table += group
    # HTML ignores these (colwidths-auto), but text/latex lay out badly without
    # them, and device names are far longer than the numbers beside them.
    for index, column in enumerate(columns):
        widest = max([len(str(column))] + [len(str(row[index])) for row in rows])
        group += nodes.colspec(colwidth=widest)

    head = nodes.thead()
    group += head
    head += table_row(columns)

    body = nodes.tbody()
    group += body
    for row in rows:
        body += table_row(row)
    return table


def table_row(cells):
    row = nodes.row()
    for cell in cells:
        entry = nodes.entry()
        entry += nodes.paragraph(text=str(cell))
        row += entry
    return row


class CcosSettingDirective(SphinxDirective):
    """Emit the per-device table for one CCOS setting."""

    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "devices": directives.unchanged,
        "version": directives.unchanged,
        "columns": directives.unchanged,
    }

    def warn(self, message):
        logger.warning(message, location=self.get_location())
        return [nodes.system_message(message, level=2, type="WARNING", source=self.env.docname)]

    def run(self):
        key = self.arguments[0].strip()
        env = self.env

        index = load_json(env, "index.json")
        if index is None:
            return self.warn(
                "ccos-setting: docs/_data/ccos/index.json is missing; "
                "run scripts/update_ccos_meta.py"
            )
        version = self.options.get("version", index["default_version"])
        snapshot = load_json(env, f"{version}.json")
        if snapshot is None:
            return self.warn(f"ccos-setting: no cached data for CCOS {version}")

        catalogue = json.loads((data_dir(env) / "devices.json").read_text())["devices"]
        if "devices" in self.options:
            slugs = [s.strip() for s in self.options["devices"].split(",") if s.strip()]
        else:
            slugs = [s for s, d in catalogue.items() if d.get("docs_default")]
        slugs = [s for s in slugs if s in snapshot["devices"]]
        if not slugs:
            return self.warn(f"ccos-setting: no devices with data for CCOS {version}")

        columns = list(DEFAULT_COLUMNS)
        if "columns" in self.options:
            columns = [c.strip() for c in self.options["columns"].split(",") if c.strip()]

        rows = []
        found = None
        options_list = None
        for slug in slugs:
            setting = snapshot["devices"][slug]["settings"].get(key)
            if setting is not None:
                found = setting
                options_list = options_list or setting.get("enum")
            values = setting_row(setting, columns)
            label = catalogue.get(slug, {}).get("name", slug)
            rows.append([label if c == "Device" else values.get(c, MISSING) for c in columns])

        if found is None:
            return self.warn(
                f"ccos-setting: '{key}' is not present on any selected device in CCOS {version}"
            )

        container = ccos_table()
        container["setting"] = key
        container["version"] = version
        container["devices"] = slugs
        container += build_table(columns, rows)

        if options_list:
            container += nodes.paragraph(
                text="Available options: " + ", ".join(options_list),
                classes=["ccos-enum-options"],
            )
        return [container]


def plain_text(value):
    """Flatten an API description into a single line of plain text.

    A few descriptions carry inline HTML (`<b>`, and at least one unbalanced
    `<b/>`), which docutils would otherwise render as literal angle brackets.
    """
    return " ".join(re.sub(r"<[^>]*>", "", value or "").split())


def describe_setting(setting):
    """Compose the prose the SerialAPI parameter table shows for one setting.

    The API splits what a reader needs across several fields, so the sentence
    is assembled here rather than stored: prose first, then what values are
    accepted, then the factory default.
    """
    parts = []
    description = plain_text(setting.get("description"))
    if description:
        parts.append(description if description[-1] in ".!?" else description + ".")
    if setting.get("enum"):
        parts.append("One of: " + ", ".join(setting["enum"]) + ".")
    else:
        bounds = setting.get("range")
        if bounds:
            low = format_value(bounds[0], setting, is_step=True)
            high = format_value(bounds[1], setting, is_step=True)
            sentence = f"Range {low} to {high}"
            step = setting.get("step")
            if step and step != 1:
                sentence += f", in steps of {format_value(step, setting, is_step=True)}"
            parts.append(sentence + ".")
    if setting.get("default") is not None:
        parts.append("Default " + format_value(setting["default"], setting) + ".")
    return " ".join(parts)


class CcosParameterCodesDirective(SphinxDirective):
    """Emit the VAR parameter code table: every setting id a device accepts."""

    option_spec = {"devices": directives.unchanged, "version": directives.unchanged}

    def run(self):
        env = self.env
        index = load_json(env, "index.json")
        if index is None:
            logger.warning(
                "ccos-parameter-codes: docs/_data/ccos/index.json is missing; "
                "run scripts/update_ccos_meta.py",
                location=self.get_location(),
            )
            return []
        version = self.options.get("version", index["default_version"])
        snapshot = load_json(env, f"{version}.json")
        if snapshot is None:
            logger.warning(
                f"ccos-parameter-codes: no cached data for CCOS {version}",
                location=self.get_location(),
            )
            return []

        catalogue = json.loads((data_dir(env) / "devices.json").read_text())["devices"]
        if "devices" in self.options:
            slugs = [s.strip() for s in self.options["devices"].split(",") if s.strip()]
        else:
            slugs = [s for s, d in catalogue.items() if d.get("docs_default")]
        slugs = [s for s in slugs if s in snapshot["devices"]]

        # Parameter codes are per setting id, and a setting may exist on only
        # some hardware, so build the union and remember who has what.
        by_id = {}
        for slug in slugs:
            for key, setting in snapshot["devices"][slug]["settings"].items():
                entry = by_id.setdefault(setting["id"], {"key": key, "setting": setting, "on": []})
                entry["on"].append(slug)

        rows = []
        for setting_id in sorted(by_id):
            entry = by_id[setting_id]
            description = describe_setting(entry["setting"])
            if len(entry["on"]) < len(slugs):
                names = ", ".join(catalogue.get(s, {}).get("name", s) for s in entry["on"])
                description = (description + f" {names} only.").strip()
            rows.append([entry["key"], f"0x{setting_id:02X}", description])

        if not rows:
            logger.warning(
                f"ccos-parameter-codes: no settings found for CCOS {version}",
                location=self.get_location(),
            )
            return []

        return [build_table(["Parameter", "Hexadecimal Code", "Description"], rows)]


class CcosActionCodesDirective(SphinxDirective):
    """Emit the CC action code tables, one per category, from actions.json."""

    option_spec = {"version": directives.unchanged, "categories": directives.unchanged}

    def run(self):
        env = self.env
        index = load_json(env, "index.json")
        if index is None:
            logger.warning(
                "ccos-action-codes: docs/_data/ccos/index.json is missing; "
                "run scripts/update_ccos_meta.py",
                location=self.get_location(),
            )
            return []
        version = self.options.get("version", index["default_version"])
        snapshot = load_json(env, f"{version}.json")
        if snapshot is None or not snapshot.get("actions"):
            logger.warning(
                f"ccos-action-codes: no cached action codes for CCOS {version}",
                location=self.get_location(),
            )
            return []

        wanted = None
        if "categories" in self.options:
            wanted = [c.strip().lower() for c in self.options["categories"].split(",") if c.strip()]

        result = []
        for category in snapshot["actions"]:
            name = category.get("name") or ""
            if wanted is not None and name.lower() not in wanted:
                continue
            result.append(nodes.rubric(text=name))
            blurb = plain_text(category.get("description"))
            if blurb:
                result.append(nodes.paragraph(text=blurb))
            rows = [
                [
                    action["code"],
                    f"0x{action['code']:X}",
                    action.get("id") or MISSING,
                    plain_text(action.get("description")) or action.get("name") or MISSING,
                ]
                for action in category["actions"]
            ]
            result.append(build_table(["Code", "Hex", "ID", "Description"], rows))

        if not result:
            logger.warning(
                "ccos-action-codes: no categories matched", location=self.get_location()
            )
        return result


def setup(app):
    app.add_config_value("ccos_data_dir", "_data/ccos", "env")
    app.add_node(
        ccos_table,
        html=(visit_ccos_table_html, depart_ccos_table_html),
        latex=(visit_ccos_table_passthrough, depart_ccos_table_passthrough),
        text=(visit_ccos_table_passthrough, depart_ccos_table_passthrough),
        man=(visit_ccos_table_passthrough, depart_ccos_table_passthrough),
        texinfo=(visit_ccos_table_passthrough, depart_ccos_table_passthrough),
    )
    app.add_directive("ccos-setting", CcosSettingDirective)
    app.add_directive("ccos-parameter-codes", CcosParameterCodesDirective)
    app.add_directive("ccos-action-codes", CcosActionCodesDirective)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
