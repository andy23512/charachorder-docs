# docs (Tangent's fork)

An unofficial fork of the [CharaChorder documentation](https://github.com/CharaChorder/docs), where setting tables are
generated from the Firmware Meta API instead of being written by hand.
The official documentation is at <https://docs.charachorder.com/>.

## Dependencies

Install `sphinx`, `sphinx_rtd_theme`, `sphinx-design`, `myst-parser`, and `sphinx_copybutton` using `pip` or your preferred package manager.

```sh
pip install sphinx sphinx_rtd_theme myst-parser sphinx-design sphinx_copybutton
```

### Nix/NixOS

With flakes enabled, run `nix develop` or use [nix-direnv](https://github.com/nix-community/nix-direnv) with `direnv allow`

## Development

For development, you should also install `sphinx-autobuild` and then start the dev server using

```sh
sphinx-autobuild docs _build
```

## Building

```sh
sphinx-build -a docs _build
```

Note, the -a flag will rebuild all files, regardless of if they have changed. This is useful so that warnings don't get cached.  All warnings are preferred to be fixed rather than left, although in some cases (docs don't exist yet) the warnings are fine to leave.

## Adding a new top level page

If you are adding or editing an under construction top level page, make sure to
add it to index.rst if you'd like to have it shown on the left side bar.

## Linking

If you'd like to link to another page (just the page) use something like this:
```
:doc:`chording<Chords>`
```

If you want to link to a specific header in another page or on the same page:

```
:ref:`startup<GenerativeTextMenu:Startup>`
```

If you want to link to a specific anchor:
```
:ref:`slow speed <Slow Speed>`
```

## Tables

```
.. csv-table::
:header: "Device", "Default", "Min. Value", "Max. Value", "Increments"

    "CharaChorder One", ""
    "CharaChorder Lite", ""
    "CharaChorder X", ""
    "CharaChorder Engine", ""
```

## Dropdown

```
.. dropdown:: Title of the Dropdown, visible with the DD closed.

    Text inside the dropdown should skip a line then indent once (4 spaces).
```

## Images

```
.. image:: /assets/images/PATH-TO-IMAGE.png
  :width: 1200
  :alt: Alt text for screen readers
```

## CCOS setting tables

Setting defaults and ranges are generated from the official
[Firmware Meta API](https://github.com/CharaChorder/CCOS-firmware#firmware-meta-api)
instead of being written by hand, so they stay correct per device and per CCOS
version. Instead of a `csv-table`, write:

```
.. ccos-setting:: mouse/slow speed
```

The argument is `<settings group>/<setting name>` spelled exactly as the Meta
API spells it (lower case). Options:

```
.. ccos-setting:: chording/detection method
   :devices: one_m0, two_s3
   :version: 3.0.0
   :columns: Device, Default, Setting ID
```

- `:devices:` — API device slugs; defaults to the devices marked
  `docs_default` in `docs/_data/ccos/devices.json`
- `:version:` — a cached CCOS version; defaults to the newest one cached
- `:columns:` — any of `Device`, `Default`, `Min. Value`, `Max. Value`,
  `Increments`, `Setting ID`

A device that does not have the setting gets an em dash, so hardware
differences show up on their own.

Values are rendered as the API sends them — scaled, with the unit appended —
with one exception. The LED settings use HSB component letters as their unit,
so `leds/brightness` would read "255 B". Those letters are suppressed by
`UNIT_DISPLAY`, which lives in **both** `docs/_ext/ccos_meta.py` and
`docs/_static/ccos-meta.js`: the extension renders the baked-in table and the
script re-renders it when a reader picks another version, so a unit dropped in
only one of them would come back on the first version switch.

### Other generated tables

`SerialAPI.rst` uses two more directives fed by the same cache:

```
.. ccos-parameter-codes::
```

Every setting id a device accepts, as the hexadecimal parameter code used by
`CMD_VAR_SET_PARAMETER`, with the accepted range and factory default. Takes
`:devices:` and `:version:`. Settings that only exist on some hardware are
marked in the description ("CharaChorder Lite, Master Forge only"). This table
is a union across devices rather than one row per device, so unlike
`ccos-setting` it is **not** re-rendered by the live version picker.

```
.. ccos-action-codes::
```

All CC action codes from `actions.json`, one table per category, with the
decimal value used inside chords and its hexadecimal equivalent. Takes
`:version:` and `:categories:` (comma separated, to render only some).
`actions.json` is identical across devices for a given release, so it is
cached once per version.

### Refreshing the data

The build never touches the network; it reads snapshots committed under
`docs/_data/ccos/`. To update them:

```sh
python3 scripts/update_ccos_meta.py                 # newest stable per device
python3 scripts/update_ccos_meta.py --version 3.0.0
python3 scripts/update_ccos_meta.py --pre-releases   # include rc/beta builds
```

`.github/workflows/update-ccos-meta.yml` runs this weekly and opens a pull
request, so firmware changes surface as a reviewable diff.

On top of the baked-in tables, `docs/_static/ccos-meta.js` adds a version
picker that queries the Meta API live, letting readers check any device and
CCOS version combination. With JavaScript off, the cached tables still render.

The picker offers every version any device on the page released, back to
2.1.0-rc.0 — older builds answer 500 rather than publishing setting metadata,
so `MIN_METADATA_VERSION` hides them. A version a device skipped shows em
dashes in that device's row.

### Finding setting names

To list what a version exposes:

```sh
curl -s https://charachorder.io/firmware/one_m0/3.0.0/settings.json | python3 -m json.tool
```
