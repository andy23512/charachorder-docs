# Open questions — CCOS Meta API integration

Items that need a human decision or product knowledge before the generated
docs can be considered correct. Each one lists what was found, why it is
blocked, and where to look.

Background: setting tables are now generated from the
[Firmware Meta API](https://github.com/CharaChorder/CCOS-firmware#firmware-meta-api)
via `docs/_ext/ccos_meta.py`. See README.md for how the directive works.

---

## 1. Confirm device slug → product names

**File:** `docs/_data/ccos/devices.json`

Slugs marked `"confirm": true` are guesses and are currently excluded from
generated tables (`"docs_default": false`).

| Slug | Current name | Status |
|---|---|---|
| `m4gr_s3` | Master Forge (right half) | DeviceManager calls it `M4G (right)` — is it a separate documented product? |
| `t4g_s2` | CCB (T4G S2) | DeviceManager maps **both** `t4g_s2` and `ccb_s2` to `CCB` |
| `ccb_s2` | CCB (S2) | Same alias as above — are these one product or two? |
| `zero_linux` | CharaChorder Zero (Linux) | Software build, not hardware — should it appear in device tables at all? |
| `zero_wasm` | CharaChorder Zero (WASM) | Same |
| `zero_win` | CharaChorder Zero (Windows) | Same; has no stable release yet |

Confirmed from `DeviceManager/src/lib/serial/device.ts` (`DEVICE_ALIASES`):
`one_m0`→CC1, `two_s3`→CC2, `lite_s2`→Lite (S2), `lite_m0`→Lite (M0),
`x_s2`→CCX, `m4g_s3`→M4G.

**Also decide:** `lite_m0` and `lite_s2` are two hardware generations of
"CharaChorder Lite". Docs currently show only `lite_s2` as "CharaChorder
Lite". Should both appear as separate rows?

---

## 2. Settings that no longer exist in CCOS 3.0.0

These sections still have hand-written tables because the setting is gone from
the API and the surrounding prose describes behaviour that may no longer exist.
Converting them would need someone who knows what replaced the feature.

### 2a. `GTM > Mouse > Poll Rate` — `docs/GenerativeTextMenu.rst`

- Not present in CCOS 3.0.0 at all.
- In 2.1.x it existed as `mouse/poll rate`, `range [0, 1000]`, `step 5`,
  unit **Hz**. The hand-written table says "20 ms / 0 ms / 100 ms / 1 ms (Hz)",
  so it was already inconsistent with the firmware back then.
- 3.0.0 gained `usb/poll rate` (enum: `1000Hz`, `500Hz`, `250Hz`, `125Hz`) and
  `mouse/scroll throttle` (`range [0, 255]`, unit ms).

**Question:** does the GTM still expose a mouse poll rate? Should this section
be rewritten around `usb/poll rate`, split, or deleted?

### 2b. `GTM > Chording > Spurring > Spurring Timeout` — `docs/GenerativeTextMenu.rst`

- No matching setting in **any** version that publishes metadata (2.1.0+).
- Spurring itself survives as `chording/detection method` = `continuous`,
  whose API description reads "Continuous (spurring)".
- The hand-written table says default 240 s, range 0–250 s. No setting with
  that shape exists; the nearest candidate `chording/compound timeout` is
  `range [0, 2550]`, `step 10`, unit **ms**.

**Question:** was the spurring timeout removed, or renamed to something not
obviously related? If removed, this subsection should probably go.

---

## 3. LEDs section is scoped to the wrong devices

**File:** `docs/GenerativeTextMenu.rst`, heading
`LEDs (CharaChorder Lite only)`

In CCOS 3.0.0 the `leds/*` settings exist on **`lite_s2` and `m4g_s3`**, so
the generated brightness table shows values for CharaChorder Lite *and* Master
Forge while the heading still says "CharaChorder Lite only".

**Question:** rename the heading (e.g. drop the parenthetical), and does the
surrounding prose about LED behaviour hold for Master Forge?

Note the hand-written table said brightness `0–50, default 5`; the API says
`0–255, default 255`.

---

## 4. Unit labels the API uses for LEDs

`leds/brightness` has `unit: "B"`, `leds/hue` has `"H"`, `leds/saturation` has
`"S"` — HSB component letters. Rendered faithfully this reads "255 B", which
is not obvious to a reader.

**Question:** leave as-is (faithful to the API), or add a display-name
override map in the extension (e.g. `B` → nothing, or → "brightness")?

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
