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
- **Missed at the time:** that sentence says "mouse/keyboard poll rate
  settings", plural. `keyboard/poll rate` (`0x14`) is what the GTM page called
  `Scan Rate`, and it went in the same release. Item 8f deleted it.
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
- **Addendum from the item 13 walk:** on a CharaChorder Two (CCOS 3.0.0), the
  `Chording` menu still lists a `Spurring` entry — selecting it does nothing.
  The setting behind it is gone, as above; the GTM just never cleaned up the
  now-dead menu label. Worth knowing so nobody mistakes the leftover text for
  evidence that spurring survived.
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
rather than expanded into a word nobody has verified.

**Both routes to resolving it turned out to be dead ends or impractical:**

- **No label in the Device Manager.** Its own hardcoded
  `src/lib/assets/settings.yml` carries the same bare `unit: pg` with no
  `description`, and the settings page
  (`src/routes/(app)/config/settings/+page.svelte`) renders any non-H/S/B unit
  by concatenating it straight after the number input -- so the shipping app
  shows the same unexplained "255pg" a reader would see here. There is no
  hidden label to go find.
- **Behavioural testing is confounded by the OS.** Any test that scrolls
  something and measures the result -- a paged terminal reader, a browser's
  `wheel` event `deltaY` -- passes through the OS's own scroll-speed
  multiplier first (macOS: System Settings > Mouse > Scroll speed). That
  multiplier sits between the firmware's HID wheel report and anything an app
  can observe, so no app-level measurement can isolate what `mouse/scroll
  speed` alone contributes.
  Reading the raw HID report before the OS touches it would route around
  that, but `hidutil monitor` -- the obvious tool -- does not exist on
  current macOS (checked on 26.5.1: `hidutil` only has `dump`, `property` and
  `list`, and `dump` is a state snapshot, not a live stream). A USB-level
  capture (Wireshark against the CharaChorder's USB bus, or a tool like
  Karabiner-EventViewer) would still work but has not been tried.

**Leading hypothesis, not yet confirmed: `pg` is a typo for `px`.** This
matches the pre-generation prose, which described this exact setting in
pixels. No new evidence for or against it was found beyond that prose already
being here before the tables were generated.

**Decided: leave the table rendering `pg` verbatim rather than silently
correct it to `px`.** Same reasoning as item 5 and item 6 -- an unverified
guess written as fact would be worse than the honest gap, because a reader
who trusted "px" and then measured actual pixel movement would be misled with
more confidence than the current bare "pg" ever claims. Revisit if a USB
capture or an upstream answer settles it.

**Changelog cross-check (2026-08), for reference.** Searched every
`changelog.json` `one_m0` publishes -- the 39 live versions from
`2.1.0-rc.0` up -- for "scroll". Two feature entries turned up, neither
explaining `pg`:

- **Spin Scroll**, first at `2.1.0-rc.0`: "This feature allows you to
  dedicate a stick to scrolling, and scroll by spinning it like a scroll
  wheel instead of holding down a key." (Typo "scolling" through `rc.3`,
  fixed at `rc.4`.)
- **High resolution scrolling** -- title only, no description -- first at
  `2.2.0-beta.20`, still listed as of `3.0.0`/`3.0.0-rc.0`. Absent from
  `beta.0` through `beta.8`.

Neither names `mouse/scroll speed` or `mouse/scroll throttle`, and neither
settles the unit. Flagged, not chased further: "High resolution scrolling"
landing in the same era as this setting raises the possibility that `pg` is
some resolution-related quantity rather than "pages" or a `px` typo, if it
changed what a single wheel HID report represents. That is speculation with
nothing behind it -- recorded so it is not reinvented, not as a lead anyone
should act on yet.

---

## 5. Enum values render in the API's lower case (decided)

Eight settings carry an `enum`, 29 values between them. They show up in three
places: the `Default` column, the generated "Available options:" line under the
table, and the `One of: ...` sentence in the Serial API parameter table.

**Decided: render them verbatim.** No code change.

A blanket title-case does not work. `ios` becomes `Ios`, which is wrong, while
`usb/poll rate` already ships `1000Hz`, `500Hz` and so on — the API sometimes
cases values deliberately, so a rule would overwrite that. A hand-written
display map like `UNIT_DISPLAY` was rejected for a different reason: that one
has three entries and no reason to grow, whereas this would be 29 values across
eight settings that upstream adds to, and a value added without a map entry
would be the only lower-case one on the page.

The deciding argument is that these are not display strings. They are the
values a reader sends over the Serial API, and they match what the device and
the Device Manager show.

Consequence handled here: `GenerativeTextMenu.rst` said "Currently, on CCOS,
you can select between Windows, Mac, Linux, iOS, or Android" immediately above
a generated table saying `windows`. The sentence was deleted rather than
re-cased — "Currently" plus a hand-written list is exactly the shape that goes
stale, and the generated "Available options:" line below it says the same thing
from the API.

---

## 6. Operating system codes table — `docs/SerialAPI.rst` (done)

The hand-written table maps `Windows`→0 … `Android`→4 **plus `Unknown`→255**.
Codes 0-4 are exactly the positions of the values in the `misc/operating
system` enum, but 255 is not in the enum, so the table cannot be generated
whole.

Nothing found supports 255: it is absent from the Meta API, all eleven devices
ship factory default `0`, and `Beta Releases.rst` never mentions the setting.
Nothing found contradicts it either — it has been in this page since the serial
API was first documented (`d1c9eba`).

**Decided (superseded below): the table stays hand-written, with a note saying
what is and is not known.** The generator was not extended to bolt extra rows
onto an enum — that would put an unverified value inside the generated
pipeline, for one table, with no second use case in sight. The section also
stays its own table rather than folding into the generated `Parameter codes`
above it: they are different lookups, the generated one read by parameter
name, this one by code number, which is what someone implementing the
protocol has in hand. Both of those calls still stand.

**Tested on hardware (2026-08): 255 does not round-trip.** Sent `255` to
parameter `0x91` with `CMD_VAR_SET_PARAMETER`, then read it back with
`CMD_VAR_GET_PARAMETER`. The device returned `5`, not `255` — one past the
last valid enum index (`android` = 4), not the value that was written and not
a clamp to the valid range either. Whatever this is, it settles the question
this item opened with: the firmware does not store `255` for this setting, so
`Unknown` → `255` was not a value a reader could ever rely on. Removed from
`docs/SerialAPI.rst`; the note there now records the test instead of the open
question.

**Not chased further: why `5`.** One plausible read is an off-by-one clamp —
firmware rejecting an out-of-range write by pinning it to `count` (5) instead
of `count - 1` (4, the actual last index) — but that takes more than one data
point to confirm (does `6` also read back as `5`? does `254`?), and nothing
here depends on the answer. Worth a line in item 10's upstream list if that
policy ever changes.

---

## 7. The version picker only listed one device's releases (done)

**File:** `docs/_static/ccos-meta.js`

The dropdown was built from the first device of the first table on the page.
Release history differs a lot per device — stable counts: `one_m0` 9,
`lite_s2` 12, `engine_s2` 6, `two_s3` 6, `x_s2` 6, `m4g_s3` 3, `t4g_s2` 1 — so
which versions a reader was offered depended on which table happened to come
first, and versions other devices shipped never appeared at all.

**Done: the picker now lists the union of every device on the page, minus the
versions that publish no setting metadata.**

The intersection was measured before choosing, and it collapses. Across the six
devices the generated tables cover, exactly one stable release is common to all
of them: 3.0.0. A picker with a single entry is not a picker.

The union was measured too, by asking for `settings.json` on all 297
device/version pairs those six devices list (2026-08):

- 80 distinct versions, of which **54 publish metadata and 26 answer 500 on
  every device**.
- The cutoff is clean: everything from **2.1.0-rc.0** up is published,
  everything below it is dead. No exceptions in either direction.
- Probing only `one_m0` offered 61 versions, **22 of them dead** — including
  six of its nine stable releases, since 2.0.x and everything older publishes
  nothing.
- It also hid 15 versions that do work, all pre-releases (`3.1.0-beta.*`,
  `2.2.0-beta.*`), because the One never shipped them.

So the change both widens and narrows the list. With pre-releases hidden, which
is the default, the dropdown is now 3.0.0 / 2.1.1 / 2.1.0 — three entries that
all work, where it used to be nine of which six failed.

The em dashes the union adds are correct and were accepted: 2.1.1 blanks the X
and the Engine rows because those devices never shipped 2.1.x. That is the
question the picker exists to answer.

Dropping the dead versions by version comparison rather than by probing each
one costs a hardcoded floor, `MIN_METADATA_VERSION`. It is a claim about the
past, which does not move, and the failure mode is mild in both directions: if
CharaChorder backfills older builds they simply will not be listed, and the
500-handling path in `apply()` is still there if the floor ever turns out to be
wrong. Probing 54 versions × 6 devices on page load to avoid the constant is
not worth it.

Not addressed: the picker still fetches one directory listing per device on the
page (six instead of one). Responses are cached per URL and the tables already
fetch all six devices on any version switch, so this only moves work that was
happening a moment later anyway.

---

## 8. Prose that quotes stale numbers (done)

Converting the tables fixed the tables, not the sentences around them. Four
mismatches were listed here. Two had already gone with the tables that carried
them, and re-reading the pages turned up two more that were never listed.

**8a. `autocorrect/timeout` — fixed.** `GenerativeTextMenu.rst` offered "as low
as 0.0 seconds (s) or as high as 25.0 seconds (s)". The API says `[0, 25500]`
at `scale 0.001`, so the ceiling is 25.5 s. The range was dropped from the
sentence rather than corrected: the generated table sits directly underneath
and says the same thing more precisely, and a second hand-written copy is just
somewhere else to go stale. The warning below it — that 0.0 s leaves chords
firing without erasing their inputs — describes behaviour no table carries, and
stayed.

**8b. Chord tolerances "0-150 ms" — nothing to fix.** The 150 was in the
hand-written table, not the prose, and went with it in `9e48ffd`. Neither
tolerance section states a range at all. One number does sit nearby: the
`25ms` in the GTM screen example at line 51, which illustrates what the menu
looks like rather than claiming a default. Recorded under item 13 to be
checked with the rest of that page on a device.

**8c. SerialAPI defaults "7ms on the One and 20ms on the Lite" — nothing to
fix.** Removed with the hand-written table in `fb0c398`. The generated rows say
more rather than less — `Range 0 ms to 255 ms. Default 16 ms.` — and the old
numbers were wrong anyway: `0x64` claimed 1500 ms where the API says 1000.
Diffing the 38 old rows against the 44 generated ones did turn up eight codes
that vanished without a replacement, which is now item 16.

**8d. `misc/operating system` — the contradiction is now stated as one.** The
page recommended matching the setting to your computer and then warned, in a
note dated December 2023, that it does nothing. Nothing settles it: the Meta
API publishes the setting and its values but not what reads them, and
`Beta Releases.rst` does not mention it in either direction. Deleting the
warning would assert it works; deleting the advice would assert it does not.
The warning now says the question is open and that matching your computer costs
nothing either way. The one hint found, too weak to act on, is that
`keyboard/command control swap` exists separately and is described as easing
the move between Mac and other systems — which would leave this setting with
little to do. Item 6 covers the same setting from the Serial API side.

**8e. Debounce Press / Release — converted.** Two hand-written tables in
`GenerativeTextMenu.rst` were stale in every column: defaults of 7/12/1 ms per
device against the API's 16 ms everywhere, a 100 ms ceiling against 255, and
three devices listed out of eleven. Both are now
`.. ccos-setting:: keyboard/debounce press` / `release`.

**8f. Scan Rate and Keystroke Delay — deleted.** Neither has a setting in
3.0.0. Tracking the parameter ids across versions says why:

| | `0x14` | `0x17` | `0x26` |
|---|---|---|---|
| 2.1.0, 2.1.1 | `keyboard/poll rate` | — | `mouse/poll rate` |
| 2.2.0-beta.0 | — | — | — |
| 2.2.0-beta.29 onward | — | `keyboard/rollover` | — |

`0x14` is the old "Key Scan Duration", and it disappeared alongside
`mouse/poll rate` in 2.2.0-beta.0 — both halves of `Beta Releases.rst:215`,
"Replaced the mouse/keyboard poll rate settings (which didn't actually change
the poll rate) with a USB poll rate setting". Item 2a acted on that sentence for
the mouse and missed the keyboard. The replacement, `usb/poll rate`, is already
documented in `Device Manager.rst`.

Keystroke Delay (`0x17`, "Keyboard Output Character Microsecond Delays") is
absent from 2.1.0, the oldest version publishing metadata, and its id now
belongs to `keyboard/rollover`. Same situation as spurring in item 2b: no
version has it, so it was not renamed, it is gone. Leaving it documented would
point readers at an id that now writes something else.

Deleted: both `GenerativeTextMenu.rst` sections with their tables, the
`Key Scan Rate` and `Output Character Delay` dropdowns in `Device Manager.rst`
that repeated them, and "and even a customizable scan rate" from the CCOS
feature list in `CCOS.rst:18`.

Checking `keyboard/rollover` afterwards led to item 17.

---

## 9. Tables in `SerialAPI.rst` that stayed hand-written (answered)

Of the 24 `csv-table` blocks, 2 are now generated. The rest were left alone:

- **17 protocol frame tables** (`"I/O","Index","Name","Type","Example","Notes"`)
  describe the serial wire format and have no counterpart in the Meta API.
- **Command / CML / VAR / RST subcommand lists** — protocol, not settings.
- **Keymap codes** (`Primary` A1, `Secondary` A2, `Tertiary` A3) — not exposed
  as settings.
- **Chord Construction** bit layout table.
- **Operating system codes** — decided in item 6: stays hand-written,
  because `Unknown`/255 is not in the API's enum and nothing verifies it.

**Answered: no, the protocol is not published machine-readable.** Checked the
whole Meta API surface. A version directory
(`https://charachorder.io/firmware/one_m0/3.0.0/`) holds exactly 13 files:
`meta.json`, `settings.json`, `actions.json`, `factory_settings.json`,
`factory_layout.json`, `changelog.json`, `recipes.json`, the four chord sets
(`starter`, `functional`, `riley`, `arpeggiates`), `firmware.bin` and
`CURRENT.UF2`. `meta.json` indexes those files and nothing else — there is no
command, subcommand or frame description anywhere in it.

The CCOS-firmware README says so itself. Its "Serial API" section names two
references and neither is data: this docs page, and a hand-written TypeScript
client at `DeviceManager/src/lib/serial/device.ts`. That client hardcodes
`"C0"`, `"B0"` and the rest as inline string literals, so it is not a table
anyone could generate from either.

**Done:** `docs/SerialAPI.rst` now carries a note at the top saying which two
tables are generated and that the wire format is maintained by hand, so the
next person does not repeat this search. The reference implementation is
linked from it — see item 18 for what comparing against it turned up.

---

## 10. Upstream data quirks worth reporting to CharaChorder (decided)

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
- Requests for versions older than 2.1.0-rc.0 answer **HTTP 500 without CORS
  headers** rather than 404, which browsers can only report as a generic
  network failure. Item 7 has the measured boundary: 26 of the 80 versions the
  documented devices list answer 500 on every device.
- `fuzzy modifiers/enable` is an on/off setting with `range [0, 1]`, but it
  carries `unit: "ms"`. The other nine `[0, 1]` settings across the API have no
  unit, and its neighbours in the same group (`press theshold`, `release
  theshold`, `release guard threshold`) are genuinely in ms, so the unit looks
  copied. It renders as "Range 0 ms to 1 ms. Default 0 ms." The docs leave it
  verbatim rather than special-casing it, so a fix upstream will show up here.

**Decided: do not open issues upstream for now.** The list stays here as a
record. Nothing on it breaks the generated docs today — the two misspellings
and the stray `unit: "ms"` render verbatim, the inline HTML is stripped by the
extension, and the `actions.json` key inconsistencies are in fields the
generator never reads. The only one with real user impact is the HTTP 500
without CORS headers, and item 7 already routes around it with
`MIN_METADATA_VERSION`.

The same decision covers item 18's four Serial API gaps (`QRY KEY`, `CML C5`,
`RST OTA`, profile addressing), which that item proposed filing alongside this
list. They are documentation gaps rather than data quirks, so if the call is
ever reversed they belong in an issue of their own, not this one.

Note that filing any of these means writing the upstream-facing version: which
file, which version snapshot it was observed in (all of the above are from the
3.0.0 data cached here, checked 2026-08), and what the expected value is. That
work has not been done.

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

### 12a. A whole section was commented out — `docs/Master Forge.rst:333` (done)

```rst
.. Dropdown: Only use in Emergency
```

One colon, not two. `.. dropdown::` is a directive; `.. Dropdown:` is a
**comment**, so docutils swallowed everything indented beneath it — lines
334–418, i.e. 62 non-blank lines and 9 images. The entire *"Only use in
Emergency"* manual firmware-update procedure was absent from the published
page.

**Done: it is a real `.. dropdown::` now, and the block was reindented so it
parses.** Turning the comment into a directive alone was not enough — building
with the one-character fix and nothing else produced 16 warnings and 5 errors,
all inside the block:

- Every line used tabs and spaces mixed, at depths that do not line up once
  docutils expands tabs to 8 columns. Each `.. image::` and its `:width:` /
  `:alt:` lines sat at three different indents, so the option block was read as
  the option *value*: `invalid option value: (option: "width"; value: '435\n:alt:
  Popup to select serial device')`, five times. One image swallowed its options
  as content instead (`no content permitted`).
- One of those errors surfaced as a bogus missing-image warning for
  `assets/images/DM-CCOS-button.jpg:width:600` — the option text glued to the
  filename. The file itself is fine.
- Two explicit labels were defined twice, `Bootloader button` and
  `Current.uf2 button`, once per digitizer half.

What the fix consisted of, beyond the one character:

- The whole block reindented to spaces: 3 for the dropdown's own content, 6 for
  content belonging to a numbered step, 9 for image options. Blank lines
  inserted where a step follows an indented block, which is what the remaining
  `Block quote ends without a blank line` warnings were.
- The four labels of the second half suffixed `Emergency Right`, and the first
  half's `Bootloader button` / `Current.uf2 button` suffixed `Emergency`, to
  match the `Connect Button Emergency` / `Serial Port Popup Emergency` already
  there and the `... Check Firmware` / `... Update Firmware` convention the
  other device pages use. Nothing referenced any of them — they were
  unreachable inside a comment.
- The two `FW-connect-button.jpg` references corrected to `.JPG`, which is
  12b's remaining half.
- One sentence was split across a blank line (`Once again, your Forge will
  automatically reboot and the` / `Forge drive will have disappeared.`), which
  would have rendered as two broken paragraphs. Joined.

Verified: the build is back to its baseline 20 warnings with none in
`Master Forge.rst`, and the rendered dropdown contains all 9 images, both
warning admonitions, and one continuous `<ol>` numbering the 16 steps 1-16. The
block's text was diffed against `HEAD` with whitespace normalised to confirm
that only the edits listed above changed.

### 12b. Image paths whose case does not match the file on disk (done)

| Reference | File in git | Effect |
|---|---|---|
| `Device Manager.rst:379` → `ManagerSettingsAutocorrect.png` | `ManagerSettingsAutoCorrect.png` | **Fixed** — was missing from the published page |
| `Master Forge.rst:325` → `DM-apply-update-button-M4G.png` | `DM-apply-update-button-m4g.png` | **Fixed** — was missing from the published page |
| `Master Forge.rst:342` → `FW-connect-button.jpg` | `FW-connect-button.JPG` | **Fixed** — with 12a, which made the block render |
| `Master Forge.rst:385` → `FW-connect-button.jpg` | `FW-connect-button.JPG` | **Fixed** — with 12a, which made the block render |

**Done: the first two were the only `image file not readable` warnings the CI
build emitted, and both references were corrected** rather than renaming the
files, so nothing else that points at them had to move. The other two were
fixed as part of 12a, which is what made that block render at all.

Note `Master Forge.rst:241` and `:291` already spell the same file `.JPG`
correctly, so only the copies inside the commented block are wrong.

### 12c. Cross-references that do not resolve (done)

This item used to list four `:ref:` targets as missing. **Three of the four were
never broken.** They were found by comparing the target string against section
titles by hand, and Sphinx does not match that way: it lowercases labels before
looking them up, so a case difference costs nothing.

Building the docs is what settles it (`.venv/bin/python -m sphinx -b html docs
<out>`, Sphinx 9.1.0). Before the fixes below the build emitted exactly one
undefined-label warning, and the other three resolved to real links in the
generated HTML:

| Reference | Verdict |
|---|---|
| `Chords.rst:103` → `Chords:Impulse Chording` | fine — resolves to `#impulse-chording`; the heading is `Impulse chording` |
| `Device Manager.rst:618` → `Device Manager:Action Code Categories` | fine — resolves to `#action-code-categories` |
| `SerialAPI.rst:31` → `SerialAPI:ID` | fine — resolves to `#id` |
| `Glossary.rst:35` → `Device Manager:Compound Timeout Setting` | **was broken** — rendered as plain text, no link |

**Fixed: `Glossary.rst:35` now says `:ref:`Compound timeout<Compound Timeout
Setting>``.** The target at `Device Manager.rst:358` is an explicit label
(`.. _Compound Timeout Setting:`, sitting above a `.. dropdown::` rather than a
section), and explicit labels are global — the `Device Manager:` prefix that
`autosectionlabel_prefix_document` adds applies only to generated section
labels, so prefixing it was what broke the lookup.

**Also fixed, and never listed here: `Master Forge.rst:188`** wrote
`:doc:`digitizers<Digitizers>`` when no `Digitizers.rst` exists, which the build
reported as `unknown document: 'Digitizers'`. Line 185 of the same paragraph
already used `:ref:`digitizer<Master Forge:The Digitizers>``, so 188 was changed
to match; `:12` and `:76` use the same form.

After both, the build emits **no `ref.ref` or `ref.doc` warnings at all** (22
warnings down to 20). The 20 that remain are unrelated and pre-existing: ten
files warn `Explicit markup ends without a blank line`, and the same ten are not
in any toctree. `sphinx.yml` does not pass `-W`, so none of this fails the
build.

### Question for all of item 12

**Fix in the fork, or send upstream?** None of 12a-12c is fork-specific — `git
log -L` points at upstream commits by `duianto`, 2025-08 — so upstream seems the
better home. 12b and 12c are already fixed here; the question is whether to also
send them as a separate PR. Note item 10 decided against opening upstream issues
for the data quirks, which is a different call: these are patches to this
repository's own content, not reports about someone else's data.

---

## 13. The GTM page had never been checked against a real device (done for the Two)

**Files:** `docs/GenerativeTextMenu.rst`, `docs/Device Manager.rst`,
`docs/CharaChorder_Lite.rst`

Every section on the page carries a `Path: GTM > ...` line claiming the
setting is reachable from that menu. The count recorded here used to say 26;
counting the actual `Path:` lines gives **23**:

| Menu | Claims |
|---|---|
| Keyboard | 5 |
| Mouse | 4 |
| Chording | 7 |
| Display | 6 |
| Resources | 1 |

This was not hypothetical. Three settings were placed on the page during the
item 2 work by reasoning from their API group, and all three turned out to be
absent from the GTM when someone opened it on a device: `usb/poll rate`,
`mouse/scroll throttle` and `chording/detection method`.

**Done: all 23 claims walked on a CharaChorder Two running CCOS 3.0.0**, menu
by menu, cross-checked against the Meta API's `two_s3` snapshot. 17 matched --
name, submenu structure and default value all consistent with what the page
already said. Six did not:

| Finding | Fix |
|---|---|
| `GUI-CTRL Soft Swap` heading said "(CharaChorder Lite only)" | Wrong: present in the Two's `Keyboard` menu, and the Meta API lists `keyboard/command control swap` on all 11 device slugs. Heading and a note corrected. |
| `Path: GTM > Keyboard > Operating System` | Setting is real (`misc/operating system`) but not reachable from the Two's `Keyboard` menu. Path line removed, warning rewritten to say so and to note Device Manager reachability is still unchecked. |
| `Path: GTM > Display > Startup` | Not in the Two's `Display` menu, and no device in the Meta API has a setting matching it at all -- unlike `Capslock`, which is a real toggle the API just does not track. Section merged into `Realtime Feedback`, which is what the old warning already said controlled it. Five `:ref:` links across `GenerativeTextMenu.rst`, `CharaChorder_Lite.rst` (×3) and `Device Manager.rst` retargeted. |
| `Chording > Compound` had no section | The Two's `Chording` menu has a `Compound` submenu (`Compound Timeout`, default 1000 ms) with no counterpart on this page at all -- the "menu entry with no section" case item 13 anticipated. Written up from `chording/compound timeout`, matching the existing `Compound timeout` dropdown already in `Device Manager.rst`. |
| `Chording > Spurring` still shows up in the menu | Confirms item 2b's call that the setting itself is gone, but adds a detail item 2b did not have: the GTM never cleaned up the menu label, so selecting it does nothing. Noted there rather than reopening the item. |
| `mouse/enable` is undocumented and absent from the GTM | Not one of item 17's original 13 -- found here because the Two's `Mouse` menu was enumerated in full. Added to that item as a 14th entry. |

`GenerativeTextMenu.rst:51`'s illustrative screen, `Press Tolerance [ Use
up/down arrow keys to adjust: 25ms ]`, was also checked: the Two draws the line
in that exact shape. Only the number is stale (30 ms is the 3.0.0 default) and
it stays as-is, same reasoning as before -- it is an illustration, not a
defaults claim.

**Scope of what "done" means here:** one device, one version. The Two was the
device on hand; Lite, X, Engine, One and Master Forge have not been walked.
Acting on a single device's result was a deliberate call, not an oversight --
CCOS is treated as one core shared across devices, with per-device differences
handled explicitly where they are known to exist (LEDs being the standing
example), so a menu structure confirmed on one device is trusted for the
others until something turns up device-specific about it.

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
  the high byte. **Confirmed from source, not hardware:** in
  `DeviceManager/src/routes/(app)/config/settings/+page.svelte`, any setting
  with `unit === "H"` renders as `<input type="color">` labeled "Color", not a
  number field. `DeviceManager/src/lib/setting.ts` backs that picker with
  `hsvToRgb`/`rgbToHsv`, reading and writing three *consecutive* setting ids —
  `id`, `id+1`, `id+2` — as H, S and V respectively. Settings whose unit is
  `S` or `B` render nothing of their own on that page (the same `{#if}` chain
  skips both). So *if* `leds/hue`, `leds/saturation` and `leds/brightness` have
  consecutive parameter ids in that order, the Device Manager shows one color
  picker for all three, not three controls — but the ids are not recorded
  anywhere in this repo, so that last step is unconfirmed. Worth checking on
  hardware together with the rest of this item.
  (Note: this repo also ships a hardcoded, stale `leds` block in
  `DeviceManager/src/lib/assets/settings.yml` — brightness `0-50`, a 14-color
  `enum` "base color code", `highlight` — matching the pre-3.0.0 table item 3
  already deleted from these docs. That block is not what the live settings
  page renders from; do not mistake it for current behaviour.)
- `leds/effect` has two options, `static` and `rainbow`, and `leds/effect cycle`
  (`0.1-25.5 s`) presumably sets the rainbow's period — but that it applies
  only to `rainbow` is a guess.

**What it needs:** someone with a Lite or a Master Forge open in the Device
Manager to say which controls appear in the RGB box and what each does. Then
the six get dropdowns and `ccos-setting` tables like the rest.

---

## 15. Every screenshot on the Device Manager page is out of date

**File:** `docs/Device Manager.rst`, `docs/assets/images/Manager*.png`

The page shows 15 screenshots. All of them predate CCOS 3.0.0 (released
2026-01-28), and two thirds predate the Master Forge:

| Last changed | Screenshots |
|---|---|
| 2024-01/02 | `ManagerSELECTDEVICE`, `ManagerColorScheme`, `ManagerLayoutSelector`, `ManagerSaveButton`, `ManagerSettingsArpeggiates`, `ManagerSettingsChentry`, `ManagerSettingsModifiers`, `ManagerSettingsMouse`, `ManagerSettingsRGB`, `ManagerUndoRedo` |
| 2025-02-25 | `ChordManager`, `ManagerHistoryMenu`, `ManagerSettingsDevice` |
| 2025-08-26 | `ManagerSettingsAutoCorrect`, `ManagerSettingsChording` |

Mismatches already known, without opening the app:

- `ManagerSettingsMouse.png` shows a Mouse box containing **Poll Rate**, which
  2.2.0 removed, and cannot show **Scroll Throttle**, which the page now
  documents (item 2).
- `ManagerSettingsRGB.png` predates the Master Forge, so it shows the box as it
  looked when RGB really was Lite-only — the claim item 3 had to delete.
- The `USB` section added for item 2 has **no screenshot at all**.
- `ManagerSettingsSpurring.png` is orphaned: item 3 deleted the section that
  used it, because the Device Manager has no spurring box any more.

**Also worth folding in while reshooting:**

- Item 12b's case bug was on this page and is now fixed by correcting the
  reference to `ManagerSettingsAutoCorrect.png`. A reshoot renames the file
  anyway, which is the moment to settle on one spelling.
- Eleven `Manager*.png` files in `assets/images` are referenced by no `.rst` at
  all: `ManagerBootloaderButton-Lite`, `ManagerCONNECT`,
  `ManagerDeviceButton-Lite`, `ManagerFirstTimeConnect`, `ManagerLinks`,
  `ManagerPowerButton-Lite`, `ManagerREDCONNECTBUTTON`, `ManagerSettingsResets`,
  `ManagerSettingsSpurring`, `ManagerTerminal`, `ManagerVersion`. Some are
  probably left from sections that were rewritten; worth deciding which to
  delete once the new set exists.

**What it needs:** a device connected to the current Device Manager, and a
decision about capture size. The existing set is inconsistent: widths run from
250px (`ManagerSaveButton`) to 1066px (`ManagerSettingsModifiers`), and 7 of
the 15 carry `:width: 1200` — an upscale for every one of them, since none is
that wide. Worth settling on one capture width and dropping the `:width:`
overrides rather than reproducing the mix.

---

## 16. Eight serial parameter codes vanished with the hand-written table (done)

**File:** `docs/SerialAPI.rst`

Generating the parameter code table (`fb0c398`) replaced 38 hand-written rows
with 44 generated ones. Fifteen of the old codes have no generated counterpart.
Seven of them are settings CCOS dropped -- `0x14` key scan duration, `0x26`
mouse poll duration, `0x32`/`0x33` chording character counter timeout,
`0x41`-`0x43` spurring -- and falling out of the table is the right outcome for
those. The other eight are not:

| Code | Old name |
|---|---|
| `0x01` | Enable Serial Header |
| `0x02` | Enable Serial Logging |
| `0x03` | Enable Serial Debugging |
| `0x04` | Enable Serial Raw |
| `0x05` | Enable Serial Chord |
| `0x06` | Enable Serial Keyboard |
| `0x07` | Enable Serial Mouse |
| `0x12` | Enable Character Entry |

These switch serial output on and off. They are not settings a user reaches
through the GTM or the Device Manager, which is what the Meta API publishes, so
they were never in the generated data and the table lost them silently. Someone
implementing the protocol is the exact reader who needs them.

**Not restored from the old rows, because those cannot be trusted on their
own.** `0x17` used to be "Keyboard Output Character Microsecond Delays" and is
now `keyboard/rollover`; `0x93` used to be "Enable CharaChorder Ready on
startup" and is now `usb/aggressive reporting throttle`. CCOS reuses parameter
ids when a setting goes away.
Pasting the old descriptions back would document values that may now write
something else entirely.

**Tested on hardware (2026-08, CCOS 3.0.0): all eight are alive.** Sent
`CMD_VAR_GET_PARAMETER` for each of `0x01`-`0x07` and `0x12`. All eight
answered, all defaulting to `0` -- consistent with the old "enable" names,
none of which look like they'd default to on.

Cross-checked the eight ids against `one_m0`'s current `settings.json`: none
of them is used by any setting the Meta API publishes today. That is the
opposite of `0x17` and `0x93`, which this item already flagged as reused, so
the risk the old names describe the wrong thing no longer applies here the
way it did there.

**Done: written up as a second, hand-written `Serial output toggles` table**
in `docs/SerialAPI.rst`, right after the generated `Parameter codes` table
and before `Operating system codes`. The note on it is explicit about what
was and was not checked: the ids are live and default to `0`, but nobody has
toggled each one and watched the resulting serial output to confirm the old
names still describe them correctly.

---

## 17. Thirteen settings the API exposes and the docs never mention

**Files:** `docs/GenerativeTextMenu.rst`, `docs/Device Manager.rst`

Item 14 counted the LED settings. Checking `keyboard/rollover` while closing
item 8f turned into the same count for everything else: of the 43 settings CCOS
3.0.0 publishes, 14 non-LED ones have no section, no dropdown and no table
anywhere in these docs. They appear only as a row in the generated Serial API
parameter table, under their API name.

| Setting | Code | Default | Values | API description |
|---|---|---|---|---|
| `arpeggiates/mode` | 0x55 | 0 | all, chord modifiers, arpeggiate chords | no |
| `chording/concatenation style` | 0x3E | 0 | appended, prepended | yes |
| `chording/minimum chord keys` | 0x38 | 2 | 1-12 | yes |
| `chording/tap dance tolerance` | 0x39 | 175 | 0-1275 step 5 | no |
| `fuzzy modifiers/enable` | 0x18 | 0 | 0-1 ms | no |
| `fuzzy modifiers/press theshold` | 0x19 | 50 | 0-255 ms | yes |
| `fuzzy modifiers/release theshold` | 0x1A | 110 | 0-255 ms | yes |
| `fuzzy modifiers/release guard threshold` | 0x1B | 50 | 0-255 ms | yes |
| `gaming/layer warp` | 0x70 | 0 | 0-1 | yes |
| `keyboard/rollover` | 0x17 | 1 | 6 key, 12 key, 18 key | yes |
| `mouse/enable` | 0x21 | 1 | 0-1 | no |
| `usb/aggressive reporting` | 0x95 | 0 | never, active only | yes |
| `usb/aggressive reporting throttle` | 0x93 | 0 | 0-25500 step 100 s scale 0.001 | no |
| `usb/hid resend throttle` | 0x97 | 10 | 10-2550 step 10 ms | no |

Five have something to start from in `Beta Releases.rst`: `keyboard/rollover`
("Keyboard Rollover Settings"), `gaming/layer warp`, `usb/aggressive
reporting`, `chording/concatenation style` ("Prepend concatenation style") and
`arpeggiates/mode`. Seven carry an API description, which is what the generated
Serial API rows already show.

Two settings that look missing are not: `mouse/caffeine` is documented as the
Device Manager's `Active Mouse`, and `keyboard/command control swap` as
`GUI-CTRL Soft Swap` on the GTM page. Neither name matches the API.

`mouse/enable` is the one entry in this table confirmed by a device rather
than by diffing docs against the API: the item 13 walk on a CharaChorder Two
(CCOS 3.0.0) listed every entry actually in the GTM's `Mouse` menu, and this
was not among them, sitting alongside `mouse/scroll throttle` which item 2
already moved to Device Manager. Unlike that one, `mouse/enable` has no
description in the API to explain what it does, and no home anywhere in either
doc.

**Why this is not just writing them up.** Same trap as item 2a: the API group
does not tell you where a user reaches a setting. `usb/poll rate`,
`mouse/scroll throttle` and `chording/detection method` were each placed by
reasoning from the group, and each turned out to be absent from the GTM when
someone looked. Eight of these fourteen sit in `fuzzy modifiers`, `gaming` and
`usb` — groups with no section on either page, so there is not even an
established home to add them to.

**What it would take:** the device walk from item 13, plus a pass over the
Device Manager's own UI, to see which surface offers what. After that the ones
with API descriptions can be written from the metadata.

Kept separate from item 14 because the LED settings have a known home (the
`RGB` section) and a specific obstacle (nothing distinguishes `off delay` from
`on off transition`). These have neither.

---

## 18. The Serial API page has drifted from the reference implementation

Found while answering item 9. `DeviceManager/src/lib/serial/device.ts` is the
client CharaChorder's own web app talks to devices with, and the CCOS-firmware
README offers it as the reference implementation of this protocol. Four things
it does are not on the page:

- **`QRY KEY`** — a whole command that is missing. `queryKey()` sends
  `QRY KEY` and reads back a number. `QRY` is in neither the Commands Overview
  table nor the `CMD` output example, which still lists
  `CMD,ID,VERSION,CML,VAR,RST,RAM,SIM`.
- **`CML C5`** — `getProgress()` sends it and parses a float. The CML
  subcommand table stops at `C4`.
- **`RST OTA`** — sent by `updateFirmware()` to start an over-the-air update.
  The RST subcommand table lists nine values and `OTA` is not among them.
  (`UPGRADECML` is documented but unused by the client.)
- **Profiles are missing from both `VAR` addressing schemes.** `setLayoutKey()`
  builds the keymap argument as `String.fromCodePoint('A' + profile) + layer`,
  so `A1`–`A3` is profile A and `B1`–`C3` address profiles B and C.
  `setSetting()` sends the parameter code as `id + profile * 0x100`, so profile
  B's copy of setting `0x15` is `0x115`. The page describes `A1`/`A2`/`A3` as
  three fixed keymaps and parameter codes as one flat byte. `docs/Beta
  Releases.rst` already documents the three profiles, so this is the Serial API
  page lagging behind, not new hardware.

**Why this is not just writing them up.** A client sending a command proves
the firmware accepted it when that code was written, not what it returns, what
its arguments mean, or which devices and CCOS versions have it. The page's
tables give an index, type and example for every field; none of that can be
read off a call site. `QRY KEY` returning "a number" is the clearest case —
whether it is a key id, an action code or a status is not in the source.

**What it would take:** the device walk from item 13. Every one of these can be
tried on a real device over a serial terminal and its response transcribed,
which is how the rest of the page reads.

**Not fork staleness.** The official page at
<https://docs.charachorder.com/SerialAPI.html> was fetched and searched: it
contains no `QRY`, no `C5`, no `RST OTA` and no mention of profiles either. So
these are upstream documentation gaps, worth filing alongside item 10's list.

---

## 19. Contact details still point readers at CharaChorder

**File:** `docs/index.rst:24`

> If you would like to submit a correction to something you've read in this
> guide, or if you have suggestions for the guide, please email
> alan@charachorder.com.

That line was written for the official guide. Here it sends corrections about
**this fork's** content — generated tables, the version picker, the sections
items 2, 3 and 8f moved or deleted — to a CharaChorder employee who cannot act
on them and did not ask for them. The reader has no way to tell, because the
sentence sits three paragraphs below the note that says this is a fork.

Everything else found is a link to an official community, which is fine to keep
because it is about the devices rather than about the docs:

| File | What it points at |
|---|---|
| `docs/FAQs.rst:15` | Discord invite `https://discord.gg/hYu6VW5YkM` |
| `docs/FAQs.rst:16` | `https://www.youtube.com/charachorder` |
| `docs/CharaChorder Engine.rst:14` | Engine Discord channel invite |

**What it needs:** a decision on where fork corrections should go. The obvious
candidate is this repository's issue tracker, which costs nothing to point at
and keeps the report next to the code that produced the table. An email address
would work too, but that is the maintainer's to choose and is not recorded
anywhere in the repo today.

Whichever it is, the sentence should also say which corrections belong where:
content inherited from the official guide is worth sending upstream, and only
the fork's own output belongs here. Item 12 is the live example — three fixes
that are not fork-specific at all.

---

## 20. No page explains how this fork differs from the official docs

**Files:** `docs/index.rst`, plus a new page

All a reader gets today is a five-line `.. note::` at `docs/index.rst:9`,
saying the setting tables are generated from the Meta API and may differ from
the official guide. The title carries `(Tangent's fork)` and so does
`conf.py:57`. That is the whole disclosure.

The actual difference is much larger than "tables are generated". Against the
commit this fork started from (`a5a75a5`, 2025-08-29) it is 20 files and 25
commits, and the parts a reader would notice are:

- **Generated setting tables.** `docs/_ext/ccos_meta.py` renders the
  `ccos-setting` directive from cached Meta API data, so ranges, defaults,
  units and per-device columns come from the firmware rather than from prose.
- **A version picker.** `docs/_static/ccos-meta.js` re-renders every table on
  the page for a chosen CCOS release. Item 7 covers what it lists and why.
- **Sections the official guide still has, which are gone here.** Mouse and
  keyboard poll rate, scan rate, keystroke delay, and the spurring settings and
  timeout — all removed from CCOS, all still documented upstream (items 2 and
  8f).
- **Sections moved between pages** after checking a device, because the API
  group a setting belongs to does not say where a user reaches it: `usb/poll
  rate` and `mouse/scroll throttle` are documented under Device Manager here
  and on the GTM page upstream (item 2a).
- **Scope corrections**, such as LED settings no longer being described as
  Lite-only (item 3).
- **Presentation choices** that make generated output differ from the
  hand-written original: enum values kept in the API's lower case (item 5) and
  HSB component letters suppressed as units (item 4).
- **Fixes that are not fork-specific at all** and would be equally right
  upstream (item 12).

**What it needs:** a decision on shape before writing. Specifically:

- Where it lives and what it is called — `About this fork` reads better in a
  sidebar than `Differences from the official documentation`, and it has to be
  added to the `toctree` in `index.rst` or it will not render (the file itself
  says so in a comment at the top).
- Whether the index note shrinks to a link once the page exists, or stays as
  it is and gains a "read more" line.
- How much of it should be generated. The list of moved and deleted sections
  is the part most likely to go stale, and it is exactly the part this TODO
  already tracks per item, so one option is to write the page by hand and keep
  it honest by linking each entry to its item here.
