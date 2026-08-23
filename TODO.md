# Open questions — CCOS Meta API integration

Items that need a human decision or product knowledge before the generated
docs can be considered correct. Each one lists what was found, why it is
blocked, and where to look.

Background: setting tables are now generated from the
[Firmware Meta API](https://github.com/CharaChorder/CCOS-firmware#firmware-meta-api)
via `docs/_ext/ccos_meta.py`. See README.md for how the directive works.

---

## 1. Device slug → product names (decided)

**File:** `docs/_data/ccos/devices.json`

Every slug the Meta API exposes now has a decision. Recorded here so the ones
that are deliberately hidden do not get re-investigated. Slugs still marked
`"confirm": true` carry a guessed name and stay out of generated tables
(`"docs_default": false`) until CharaChorder announces the product.

**Decided:** `m4gr_s3` is the right half of one product, not a product of its
own. In 3.0.0 its 43 settings are byte-for-byte identical to `m4g_s3`, so a row
for it would only repeat the Master Forge row. Kept out of generated tables,
renamed to `Master Forge (right)` to match DeviceManager, `confirm` dropped.

**Decided:** `t4g_s2` and `ccb_s2` are **two separate products**, despite
DeviceManager aliasing both to `CCB`. Neither is described in the official docs
yet, so both stay out of generated tables (`docs_default: false`). Their names
here are still guesses — `confirm: true` is kept until CharaChorder publishes
the products. Revisit then. (Only `t4g_s2` appears in the 3.0.0 snapshot;
`ccb_s2` has no data yet.)

**Decided:** `zero_linux`, `zero_wasm` and `zero_win` are treated the same way:
CharaChorder Zero has not been announced and has no page in these docs, so all
three stay out of generated tables and keep `confirm: true` until it ships.
Whether the three platform builds deserve separate rows, or collapse into one
"CharaChorder Zero", is deferred to that point.

Confirmed from `DeviceManager/src/lib/serial/device.ts` (`DEVICE_ALIASES`):
`one_m0`→CC1, `two_s3`→CC2, `lite_s2`→Lite (S2), `lite_m0`→Lite (M0),
`x_s2`→CCX, `m4g_s3`→M4G.

**Decided:** `lite_m0` and `lite_s2` are two shipped generations of
"CharaChorder Lite", so the rule is per setting: `lite_s2` alone by default,
and `:devices:` spelled out to add a `lite_m0` row only where the two
generations actually differ.

Nothing needs that treatment today. In 3.0.0 the two are identical — 43
settings each, no key or value differences. And `lite_m0` published no build
between `2.0.0-beta` and `3.0.0`, so it has no metadata for the whole 2.1–2.2
range the version picker offers; adding it there would produce a column of em
dashes.

Re-check when a new CCOS release is cached: if a setting starts to differ, give
that one directive an explicit `:devices:` listing both. Note the option
*replaces* the default list rather than extending it, so all the other slugs
have to be repeated.

---

## 2. Settings that no longer exist in CCOS 3.0.0 (done)

Both were removed from the firmware, and `docs/Beta Releases.rst` turned out to
record why. The docs now describe what replaced them.

### 2a. `GTM > Mouse > Poll Rate` — removed

`Beta Releases.rst:215` (2.2.0-beta): "Replaced the mouse/keyboard poll rate
settings (which didn't actually change the poll rate) with a USB poll rate
setting under a new experimental category."

- The `Mouse > Poll Rate` section is gone from `GenerativeTextMenu.rst`, along
  with its hand-written table and the Hz-to-ms conversion dropdown.
- Confirmed on hardware that the GTM does not expose the `usb/*` settings, so
  `usb/poll rate` is documented in `Device Manager.rst` instead, under a new
  `USB` section, generated with `:columns: Device, Default` because it is an
  enum. The old `Mouse > Poll Rate` dropdown there was deleted.
- The mouse speed sections used to repeat a
  `Speed (px) x poll rate (Hz) = px/s` dropdown three times. Since the setting
  it depended on never worked, the formula was deleted rather than retargeted.
  Measuring the real cursor speed on hardware would let it come back.
- `mouse/scroll throttle` (new in 3.0.0, `0-255 ms`, default 16) had no
  documentation at all. Confirmed on hardware that it is not in the GTM either,
  despite being in the `mouse` group, so it is documented as a `Scroll
  Throttle` dropdown in the Device Manager's `Mouse` section.

**Worth knowing for the rest of this work:** an API group name does not tell
you whether a setting is reachable from the GTM. `usb/poll rate`,
`mouse/scroll throttle` and `chording/detection method` are all absent from the
GTM in 3.0.0, and each was guessed wrong from its group before being checked on
a device. The GTM page's section list has never been verified against 3.0.0 as
a whole — only the sections touched here. Anything written there with a
`Path: GTM > ...` line is an untested claim unless someone has looked.

### 2b. `GTM > Chording > Spurring` — folded into detection method

Spurring is not a setting of its own in any version that publishes metadata. It
survives as `chording/detection method` = `continuous`, whose API description
reads "Continuous (spurring)". No setting matching the hand-written spurring
timeout (240 s, range 0-250 s) exists in any version, so it was not renamed —
it is gone.

- The `Spurring` section in `GenerativeTextMenu.rst`, its `Spurring On/Off` and
  `Spurring Timeout` subsections and the hand-written table were deleted. The
  GTM does not offer `chording/detection method` either (confirmed on
  hardware), so nothing replaces them on that page; the Device Manager's
  `Detection method` dropdown already covers all three modes. The deletion also
  removed a stale path line reading
  `Path: GTM > Chording > Character Only Mode > Spurring Timeout`.
- `Device Manager.rst` described spurring twice: an old `Spurring` section and
  a current `Detection method` dropdown under `Chording`. Confirmed in the
  Device Manager that the spurring box no longer exists, so the old section was
  deleted. `assets/images/ManagerSettingsSpurring.png` is now unreferenced but
  was left in place.

---

## 3. LEDs section is scoped to the wrong devices (done)

`leds/*` exists on four slugs in 3.0.0 — `lite_m0`, `lite_s2`, `m4g_s3` and
`m4gr_s3` — with identical defaults on all of them, so both Lite generations
and both Master Forge halves have LEDs. The heading claiming otherwise, and a
note under it stating LED settings exist "not on any other CharaChorder
devices", were both wrong.

Checked on hardware while fixing this:

- The Lite's LEDs are not individually addressable; every LED takes one color.
- The Master Forge stores LED settings per half, so its two digitizers can be
  lit in different colors, but a half is still one color throughout.
- **Neither device exposes an LED color setting in the GTM.**
- The low-power warning is a Lite matter; nothing similar is recorded for the
  Master Forge, which has far fewer LEDs.

What changed:

- Heading `LEDs (CharaChorder Lite only)` → `LEDs`, and the one `:ref:` that
  used the old title (`CharaChorder_Lite.rst:159`) was retargeted. The intro
  now describes both devices' lighting, which is physically different: the Lite
  lights the keys from below, the Master Forge has downward facing clusters
  inside each digitizer.
- The `Color` subsection and its 11-color table (`W`/`R`/`O`/…) were deleted:
  the GTM has no color setting, and the API models color as `leds/hue`
  (`0-65280`) plus `leds/saturation`, not a list of names. Judged not worth
  keeping anywhere.
- Brightness prose said "any number between 0 and 50"; the API says `0-255`,
  default 255. Rather than restate the new numbers, the prose now points at the
  generated table so it cannot go stale again.
- The brightness table carries `:devices: lite_s2, m4g_s3`. Without it the
  table was six rows, four of them em dashes for devices with no LEDs. The
  cost is that a future LED device has to be added by hand.
- `Device Manager.rst`'s `RGB` section opened with "The RGB settings ONLY
  affect the CharaChorder Lite as of February of 2024", which is now wrong; it
  describes both devices instead.

---

## 4. Unit labels the API uses for LEDs (done)

`leds/brightness` had `unit: "B"`, `leds/hue` `"H"`, `leds/saturation` `"S"` —
HSB component letters, not units. Rendered faithfully they read "255 B", and
the setting name beside them already says which component it is.

**Decided:** suppress them. `UNIT_DISPLAY` maps `B`, `H` and `S` to nothing,
and lives in both `docs/_ext/ccos_meta.py` and `docs/_static/ccos-meta.js`,
because the extension renders the baked-in table and the script re-renders it
on a version switch. Documented in README.md so the next unit question knows
where to go.

| | before | after |
|---|---|---|
| `leds/brightness` | `Range 0 B to 255 B. Default 255 B.` | `Range 0 to 255. Default 255.` |
| `leds/hue` | `Range 0 H to 65280 H, in steps of 256 H.` | `Range 0 to 65280, in steps of 256.` |

`ms`, `s` and `px` are left alone — they are real units and they read fine.

**Still open: `pg`.** `mouse/scroll speed` has `unit: "pg"`, so its table reads
"2 pg" with nothing to explain it. Unlike the HSB letters this looks like a
genuine unit, probably "pages", but that is a guess and the prose that used to
surround the table said "pixels (px)", contradicting the API. Left verbatim
rather than expanded into a word nobody has verified. Resolving it means
watching what changing the setting actually does, or finding a label for it in
the Device Manager.

---

## 5. Enum values render in the API's lower case

`misc/operating system` renders as `windows`, `mac`, `linux`, `ios`,
`android`. The hand-written table said `Windows`.

**Question:** render enum values verbatim, or title-case them for display?
Verbatim matches what the device and Device Manager show; title-case matches
the old docs' prose style.

---

## 6. Operating system codes table — `docs/SerialAPI.rst`

The hand-written table maps `Windows`→0 … `Android`→4 **plus `Unknown`→255**.
The API enum only has the five real values; 255 is not represented.

**Question:** is `255` still a valid value to send? If yes the table cannot be
fully generated and should stay hand-written (or the generator needs a way to
add extra rows).

---

## 7. The version picker only lists one device's releases

**File:** `docs/_static/ccos-meta.js`

The dropdown is built from the first device in the table, but release history
differs a lot per device — stable counts: `one_m0` 9, `lite_s2` 12,
`engine_s2` 6, `two_s3` 6, `x_s2` 6, `m4g_s3` 3, `t4g_s2` 1.

Picking a version another device never shipped shows an em dash for it, which
is correct but can look like missing data.

**Question:** list the union of all devices' versions (more choices, more
em dashes), the intersection (fewer, always fully populated), or keep the
current behaviour?

Related: CCOS only publishes setting metadata from **2.1.0** onward. Older
builds answer HTTP 500 with no CORS header. The picker currently offers them
and explains the failure after the fact; it could hide them instead, but that
would require probing every version.

---

## 8. Prose that quotes stale numbers

Converting the tables fixed the tables, not the sentences around them. Known
mismatches to re-read:

- "You can set this setting to be as low as 0.0 seconds (s) or as high as
  25.0 seconds (s)" — API says max 25.5 s (`autocorrect/timeout`).
- Chord press/release tolerance prose implies a 0–150 ms range; the API says
  0–255 ms.
- `SerialAPI.rst` parameter code descriptions carry their own defaults
  ("default is 7ms on the One and 20ms on the Lite") that predate 2.x.

---

## 9. Tables in `SerialAPI.rst` that stayed hand-written

Of the 24 `csv-table` blocks, 2 are now generated. The rest were left alone:

- **17 protocol frame tables** (`"I/O","Index","Name","Type","Example","Notes"`)
  describe the serial wire format and have no counterpart in the Meta API.
- **Command / CML / VAR / RST subcommand lists** — protocol, not settings.
- **Keymap codes** (`Primary` A1, `Secondary` A2, `Tertiary` A3) — not exposed
  as settings.
- **Chord Construction** bit layout table.
- **Operating system codes** — see item 6 above.

**Question:** is any of the protocol data published somewhere machine-readable
(the way settings and actions are)? If not these stay hand-written, and it is
worth a note in the file saying so.

---

## 10. Upstream data quirks worth reporting to CharaChorder

Found while generating the tables. None of these are bugs in these docs, but
they show up in generated output:

- `settings.json` spells two setting names `fuzzy modifiers/press theshold`
  and `fuzzy modifiers/release theshold` — "theshold" is missing an `r`.
  The generated tables render the API's spelling verbatim.
- Three descriptions contain inline HTML (`<b>...</b>`), one with an
  unbalanced `<b/>`. The extension strips tags, so nothing leaks into the
  page, but the markup is presumably unintended in a JSON API.
- `actions.json` has inconsistent keys across entries: both `keyCode` and
  `KeyCode`, both `variantOf` and `variationOf`, and `sparator` alongside
  `separator`. The generator only reads `id`, `name`, `display` and `title`,
  so it is unaffected.
- Requests for versions older than 2.1.0 answer **HTTP 500 without CORS
  headers** rather than 404, which browsers can only report as a generic
  network failure.
- `fuzzy modifiers/enable` is an on/off setting with `range [0, 1]`, but it
  carries `unit: "ms"`. The other nine `[0, 1]` settings across the API have no
  unit, and its neighbours in the same group (`press theshold`, `release
  theshold`, `release guard threshold`) are genuinely in ms, so the unit looks
  copied. It renders as "Range 0 ms to 1 ms. Default 0 ms." The docs leave it
  verbatim rather than special-casing it, so a fix upstream will show up here.

**Question:** worth opening issues upstream on CCOS-firmware?

---

## 11. `Master Forge.rst` — nothing to generate (investigated, closed)

Recorded so it does not get re-investigated.

The file has exactly one `csv-table`, "Shifted Key Actions" under
*Shift Modifier*, mapping unshifted to shifted keys (`` ` ``→`~`, `1`→`!`, …).
It is **not** derivable from the Meta API:

- The page itself says the output "is currently controlled by the Operating
  System that your Forge is plugged into, and it is not possible to customize
  their outputs" — it describes host keyboard behaviour, not a CCOS setting.
- In `actions.json` the two halves live in different categories (`1` = code 49
  in *ASCII*, `!` = code 33 in *ASCII Macros*) and nothing links them:
  `variationOf` / `variantOf` are unset on every character in the table.

The rest of the file contains no defaults, ranges, or units — only prose,
images, notes and dropdowns. It should stay hand-written.

---

## 12. Pre-existing markup bugs in the RST sources

Unrelated to the Meta API work — found while checking the deployed site. Both
predate this branch (`git log -L` points at upstream commits by `duianto`,
2025-08). Both are easy to miss: 12a never warns anywhere, because it is valid
RST that simply does nothing, and 12b resolves silently on macOS, whose
filesystem is case-insensitive, so it only warns on the Linux CI runner.

### 12a. A whole section is commented out — `docs/Master Forge.rst:333`

```rst
.. Dropdown: Only use in Emergency
```

One colon, not two. `.. dropdown::` is a directive; `.. Dropdown:` is a
**comment**, so docutils swallows everything indented beneath it — lines
334–418, i.e. 62 non-blank lines and 9 images. The entire *"Only use in
Emergency"* manual firmware-update procedure is absent from the published
page. Confirmed: the deployed `Master Forge.html` contains no occurrence of
"auto-connected" or "Doing it manually".

**Question:** restore it as a real `.. dropdown:: Only use in Emergency`?
The block would then be parsed for the first time, so expect follow-on work:
its lines are indented with a mix of tabs and spaces at inconsistent depths,
and two of its images have the wrong case (12b).

### 12b. Image paths whose case does not match the file on disk

| Reference | File in git | Effect |
|---|---|---|
| `Device Manager.rst:403` → `ManagerSettingsAutocorrect.png` | `ManagerSettingsAutoCorrect.png` | **Image missing from the published page** |
| `Master Forge.rst:325` → `DM-apply-update-button-M4G.png` | `DM-apply-update-button-m4g.png` | **Image missing from the published page** |
| `Master Forge.rst:342` → `FW-connect-button.jpg` | `FW-connect-button.JPG` | Harmless today — inside the 12a comment |
| `Master Forge.rst:385` → `FW-connect-button.jpg` | `FW-connect-button.JPG` | Harmless today — inside the 12a comment |

The first two are the only `image file not readable` warnings the CI build
emits. Fixing them is a one-word edit each; the last two must be fixed as part
of 12a, or they will start failing the moment that block is uncommented.

Note `Master Forge.rst:241` and `:291` already spell the same file `.JPG`
correctly, so only the copies inside the commented block are wrong.

### 12c. `:ref:` targets that do not exist

Four cross-references point at section titles no section has. They predate this
branch — the same four are missing at the commit this branch started from — and
`sphinx.yml` does not pass `-W`, so they warn without failing the build.

| Reference | Target that does not exist |
|---|---|
| `Chords.rst:103` | `Chords:Impulse Chording` |
| `Device Manager.rst:618` | `Device Manager:Action Code Categories` |
| `Glossary.rst:35` | `Device Manager:Compound Timeout Setting` |
| `SerialAPI.rst:31` | `SerialAPI:ID` |

**Question:** same as 12b — fix in the fork, or send upstream?

**Question:** fix these in the fork, or send them upstream as a separate PR
(they are not fork-specific, so upstream seems the better home)?

---

## 13. The GTM page has never been checked against a real device

**File:** `docs/GenerativeTextMenu.rst`

Every section there carries a `Path: GTM > ...` line claiming the setting is
reachable from that menu. 26 such claims remain, and none has been verified
against CCOS 3.0.0:

| Menu | Claims |
|---|---|
| Keyboard | 7 |
| Chording | 7 |
| Display | 7 |
| Mouse | 4 |
| Resources | 1 |

This is not hypothetical. Three settings were placed on that page during the
item 2 work by reasoning from their API group, and all three turned out to be
absent from the GTM when someone opened it on a device:

| Setting | Group | Actually in the GTM |
|---|---|---|
| `usb/poll rate` | `usb` | no |
| `mouse/scroll throttle` | `mouse` | no |
| `chording/detection method` | `chording` | no |

So the API tells you a setting exists and what values it takes, but not where a
user reaches it. Only the device does. The settings whose sections survived
item 2 were inherited from the pre-3.0.0 docs and carry the same risk in the
other direction: a section may describe a menu entry that 3.0.0 moved or
dropped.

**What it would take:** open the GTM on a device running 3.0.0, walk
`>K<eyboard`, `>M<ouse`, `>C<hording`, `>D<isplay` and `>R<esources`, and write
down what each menu actually lists. Then reconcile: sections with no menu entry
move to `Device Manager.rst` (as `usb/poll rate` and `mouse/scroll throttle`
did) or go; menu entries with no section get written.

Worth doing before trusting any remaining `Path:` line, but it is a device-in-
hand job and does not block the other items.

---

## 14. Six LED settings have no documentation anywhere

**File:** `docs/Device Manager.rst`, `RGB` section

Item 3 fixed who the LED settings apply to, not how many are described. The API
exposes eight; the docs describe two.

| Setting | Default | Range / options | Documented |
|---|---|---|---|
| `leds/enable` | 1 | `0-1` | yes, GTM `On/Off` |
| `leds/brightness` | 255 | `0-255` | yes, GTM `Brightness` |
| `leds/hue` | 0 | `0-65280` | no |
| `leds/saturation` | 255 | `0-255` | no |
| `leds/effect` | `rainbow` | `static`, `rainbow` | no |
| `leds/effect cycle` | 25000 | `100-25500`, step 100, unit `s` | no |
| `leds/off delay` | 1000 | `0-2550 ms`, step 10 | no |
| `leds/on off transition` | 1000 | `0-2550 ms`, step 10 | no |

The `RGB` section is two sentences and a screenshot, so this is where they
belong — the same shape as the `USB` section added for item 2.

**Why it was not done with item 3:** the metadata alone does not say what these
mean, and guessing is how three settings ended up on the wrong page during item
2. Specifically:

- `leds/off delay` and `leds/on off transition` are both `0-2550 ms` and
  nothing in the API distinguishes them.
- `leds/hue` at `0-65280` in steps of 256 is presumably a 16-bit hue stored in
  the high byte, but whether the Device Manager shows a number or a color
  picker is unknown.
- `leds/effect` has two options, `static` and `rainbow`, and `leds/effect cycle`
  (`0.1-25.5 s`) presumably sets the rainbow's period — but that it applies
  only to `rainbow` is a guess.

**What it needs:** someone with a Lite or a Master Forge open in the Device
Manager to say which controls appear in the RGB box and what each does. Then
the six get dropdowns and `ccos-setting` tables like the rest.

