/*
 * Live CCOS version switching for tables emitted by the ccos_meta Sphinx
 * extension (docs/_ext/ccos_meta.py).
 *
 * The build bakes in one cached firmware version so the page is complete and
 * searchable without JavaScript. This script adds a picker that re-reads the
 * Firmware Meta API directly, letting a reader check any device/version combo:
 *
 *   https://charachorder.io/firmware/{device}/{version}/settings.json
 *   https://charachorder.io/firmware/{device}/{version}/factory_settings.json
 *
 * The API sends `access-control-allow-origin: *`, so the browser can fetch it.
 * If anything fails we put the baked-in table back rather than showing nothing.
 */
(function () {
  "use strict";

  var API_ROOT = "https://charachorder.io/firmware";
  /* HSB component letters the API sends as units, which read as nonsense next
     to a number. Keep this in step with UNIT_DISPLAY in docs/_ext/ccos_meta.py. */
  var UNIT_DISPLAY = { B: "", H: "", S: "" };
  var MISSING = "—";
  var STORAGE_KEY = "ccos-docs-version";
  /* CCOS only publishes setting metadata from 2.1.0-rc.0 onward; older builds
     answer 500. Every one of the 80 versions the documented devices list was
     checked (2026-08) and the cutoff is clean, so the picker can drop the dead
     ones by comparison rather than by probing each one. apply() still reports a
     500 as missing metadata in case an older build starts publishing. */
  var MIN_METADATA_VERSION = "2.1.0-rc.0";
  var cache = new Map();

  function fetchJson(url) {
    if (!cache.has(url)) {
      cache.set(
        url,
        fetch(url).then(function (response) {
          if (!response.ok) throw new Error(url + " -> " + response.status);
          return response.json();
        })
      );
    }
    return cache.get(url);
  }

  /* Mirrors normalize() in scripts/update_ccos_meta.py: settings.json describes
     each setting, factory_settings.json is a sparse array indexed by id. */
  function normalize(groups, factory) {
    var defaults = (factory && factory.settings) || [];
    var out = {};
    groups.forEach(function (group) {
      (group.items || []).forEach(function (item) {
        out[group.name + "/" + item.name] = {
          range: item.range,
          step: item.step,
          unit: item.unit,
          scale: item.scale,
          enum: item.enum,
          default: item.id < defaults.length ? defaults[item.id] : null,
          id: item.id,
        };
      });
    });
    return out;
  }

  function loadSettings(device, version) {
    var base = API_ROOT + "/" + device + "/" + version;
    return Promise.all([
      fetchJson(base + "/settings.json"),
      fetchJson(base + "/factory_settings.json"),
    ]).then(function (parts) {
      return normalize(parts[0], parts[1]);
    });
  }

  function formatNumber(value) {
    return Number.isInteger(value) ? String(value) : String(parseFloat(value.toFixed(6)));
  }

  function formatValue(value, setting, isStep) {
    if (value === null || value === undefined) return MISSING;
    if (setting.enum && !isStep) {
      return setting.enum[value] !== undefined ? setting.enum[value] : String(value);
    }
    var scaled = setting.scale ? value * setting.scale : value;
    var text = formatNumber(scaled);
    var unit = UNIT_DISPLAY.hasOwnProperty(setting.unit)
      ? UNIT_DISPLAY[setting.unit]
      : setting.unit;
    return unit ? text + " " + unit : text;
  }

  function cellFor(column, setting) {
    if (!setting) return MISSING;
    var bounds = setting.range || [null, null];
    var step = setting.step;
    if (step === undefined && !setting.enum && bounds[0] !== null) step = 1;
    switch (column) {
      case "default":
        return formatValue(setting.default, setting, false);
      case "min. value":
        return formatValue(bounds[0], setting, true);
      case "max. value":
        return formatValue(bounds[1], setting, true);
      case "increments":
        return formatValue(step === undefined ? null : step, setting, true);
      case "setting id":
        return String(setting.id);
      default:
        return MISSING;
    }
  }

  function devicesIn(blocks) {
    var slugs = new Set();
    blocks.forEach(function (block) {
      block.dataset.devices.split(",").forEach(function (device) {
        slugs.add(device);
      });
    });
    return Array.from(slugs);
  }

  function columnsOf(table) {
    return Array.prototype.map.call(table.querySelectorAll("thead th"), function (th) {
      return th.textContent.trim().toLowerCase();
    });
  }

  function isPreRelease(version) {
    return version.indexOf("-") !== -1;
  }

  /* Newest first, and a release outranks its own pre-releases. */
  function compareVersions(a, b) {
    var splitA = a.split("-");
    var splitB = b.split("-");
    var coreA = splitA[0].split(".").map(Number);
    var coreB = splitB[0].split(".").map(Number);
    for (var i = 0; i < 3; i++) {
      if ((coreA[i] || 0) !== (coreB[i] || 0)) return (coreB[i] || 0) - (coreA[i] || 0);
    }
    if (!splitA[1] !== !splitB[1]) return splitA[1] ? 1 : -1;
    return (splitB[1] || "").localeCompare(splitA[1] || "", undefined, { numeric: true });
  }

  function render(block, settingsByDevice) {
    var table = block.querySelector("table");
    if (!table) return;
    var columns = columnsOf(table);
    var devices = block.dataset.devices.split(",");
    var rows = table.querySelectorAll("tbody tr");
    devices.forEach(function (device, index) {
      var row = rows[index];
      if (!row) return;
      var setting = settingsByDevice[device]
        ? settingsByDevice[device][block.dataset.setting]
        : null;
      Array.prototype.forEach.call(row.children, function (cell, column) {
        if (columns[column] === "device") return;
        cell.textContent = cellFor(columns[column], setting);
      });
    });
  }

  function apply(blocks, version, status) {
    var slugs = devicesIn(blocks);
    status.textContent = "Loading CCOS " + version + "…";
    return Promise.all(
      slugs.map(function (device) {
        // A device may simply not have this firmware version; treat as no data.
        return loadSettings(device, version).catch(function () {
          return null;
        });
      })
    ).then(function (results) {
      var byDevice = {};
      slugs.forEach(function (device, index) {
        byDevice[device] = results[index];
      });
      if (results.every(function (r) { return r === null; })) {
        /* CCOS only started publishing setting metadata around 2.1.0; older
           builds answer 500 with no CORS header, which surfaces here as a
           fetch failure. That is not the same as the API being unreachable. */
        var missing = new Error("no setting metadata published for " + version);
        missing.reason = "no-metadata";
        throw missing;
      }
      blocks.forEach(function (block) {
        render(block, byDevice);
      });
      status.textContent = "Showing CCOS " + version + " (live from the Firmware Meta API)";
    });
  }

  function restoreBaseline(blocks, status, baseline, bakedVersion, error) {
    blocks.forEach(function (block, index) {
      block.innerHTML = baseline[index];
    });
    status.textContent =
      error && error.reason === "no-metadata"
        ? "That CCOS version does not publish setting metadata — showing " +
          bakedVersion +
          " instead."
        : "Could not reach the Firmware Meta API — showing " + bakedVersion + " instead.";
  }

  function buildPicker(blocks, bakedVersion, versions) {
    var picker = document.createElement("div");
    picker.className = "ccos-picker";

    var label = document.createElement("label");
    label.textContent = "CCOS version:";
    var select = document.createElement("select");
    label.appendChild(select);

    var toggleLabel = document.createElement("label");
    toggleLabel.className = "ccos-picker-toggle";
    var toggle = document.createElement("input");
    toggle.type = "checkbox";
    toggleLabel.appendChild(toggle);
    toggleLabel.appendChild(document.createTextNode(" show pre-releases"));

    var status = document.createElement("span");
    status.className = "ccos-picker-status";

    picker.appendChild(label);
    picker.appendChild(toggleLabel);
    picker.appendChild(status);

    function fillOptions(selected) {
      select.innerHTML = "";
      versions
        .filter(function (v) {
          return toggle.checked || !isPreRelease(v) || v === selected;
        })
        .forEach(function (version) {
          var option = document.createElement("option");
          option.value = version;
          option.textContent = version + (version === bakedVersion ? " (in these docs)" : "");
          option.selected = version === selected;
          select.appendChild(option);
        });
    }

    return { picker: picker, select: select, toggle: toggle, status: status, fillOptions: fillOptions };
  }

  function init() {
    var blocks = Array.prototype.slice.call(document.querySelectorAll(".ccos-table"));
    if (!blocks.length) return;

    var baseline = blocks.map(function (block) {
      return block.innerHTML;
    });
    var bakedVersion = blocks[0].dataset.version;

    /* Release history differs per device -- the One never shipped 2.0.x, the
       Engine and the X never shipped 2.1.x -- so offer every version any device
       on this page has. One that another device skipped renders as em dashes in
       its row, which is what happened on that device. Listing only the first
       device's releases hid 15 builds and made the dropdown depend on which
       table came first on the page. */
    Promise.all(
      devicesIn(blocks).map(function (device) {
        return fetchJson(API_ROOT + "/" + device + "/").catch(function () {
          return [];
        });
      })
    )
      .then(function (listings) {
        var seen = new Set();
        listings.forEach(function (listing) {
          listing.forEach(function (entry) {
            if (entry.type === "directory") seen.add(entry.name);
          });
        });
        var versions = Array.from(seen)
          .filter(function (version) {
            return (
              version === bakedVersion ||
              compareVersions(version, MIN_METADATA_VERSION) <= 0
            );
          })
          .sort(compareVersions);
        /* Offline, blocked, or every listing failed: the baked-in tables are
           already correct, so say nothing rather than show a dead picker. */
        if (!versions.length) return;

        var ui = buildPicker(blocks, bakedVersion, versions);
        var requested =
          new URLSearchParams(window.location.search).get("ccos") ||
          window.localStorage.getItem(STORAGE_KEY) ||
          bakedVersion;
        if (versions.indexOf(requested) === -1) requested = bakedVersion;
        if (isPreRelease(requested)) ui.toggle.checked = true;
        ui.fillOptions(requested);

        // A page-level control: tables can sit far apart, so anchor it at the
        // top of the article and let CSS keep it in view while scrolling.
        var article = document.querySelector('[itemprop="articleBody"], [role="main"]');
        if (article) {
          article.insertBefore(ui.picker, article.firstChild);
        } else {
          blocks[0].parentNode.insertBefore(ui.picker, blocks[0]);
        }

        function select(version) {
          apply(blocks, version, ui.status)
            .then(function () {
              window.localStorage.setItem(STORAGE_KEY, version);
            })
            .catch(function (error) {
              restoreBaseline(blocks, ui.status, baseline, bakedVersion, error);
              // Do not leave the dropdown claiming a version the table is not showing.
              window.localStorage.removeItem(STORAGE_KEY);
              ui.fillOptions(bakedVersion);
            });
        }

        ui.select.addEventListener("change", function () {
          select(ui.select.value);
        });
        ui.toggle.addEventListener("change", function () {
          ui.fillOptions(ui.select.value);
        });

        if (requested !== bakedVersion) select(requested);
        else ui.status.textContent = "Showing CCOS " + bakedVersion + " (bundled with these docs)";
      })
      .catch(function () {
        /* A failed listing already resolves to an empty array, so reaching
           here means the API answered with something unexpected. Same call:
           leave the baked-in tables to speak for themselves. */
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
