About this fork
================

This page describes what makes this guide different from the official
CharaChorder documentation at https://docs.charachorder.com/, beyond the
five-line note on the front page. It is maintained by Tangent and is not
affiliated with CharaChorder.

.. contents::
   :local:

Generated setting tables
-------------------------

Tables that describe an individual setting -- its default, its range or enum,
which devices support it -- are rendered from the `CCOS Firmware Meta API
<https://github.com/CharaChorder/CCOS-firmware#firmware-meta-api>`__ rather
than written by hand. This means their contents come directly from the
firmware rather than from prose, so they can be more precise about
per-device differences than the official guide, but they also inherit
whatever the Meta API itself gets wrong or spells inconsistently.

A version picker
-----------------

Every generated table on a settings page can be redrawn for a different CCOS
release using the dropdown above it, since not every setting exists on every
version. The list only includes releases that publish machine-readable
settings data (2.1.0-rc.0 and later); older releases are not offered.

Settings CCOS has since removed
--------------------------------

A few settings the official guide still documents no longer exist in current
firmware, and this fork's generated tables cannot show a setting that is not
in the Meta API. Mouse and keyboard poll rate, scan rate and keystroke delay,
and the spurring settings and timeout, are all removed from CCOS 3.0.0 but
still described upstream.

Sections moved between pages
------------------------------

The API groups a setting into does not say which menu or app a user actually
reaches it from, so a few settings live on a different page here than they do
upstream, based on checking where they actually appear: ``usb/poll rate`` and
``mouse/scroll throttle`` are documented under :doc:`Device Manager` here,
and on the :doc:`GenerativeTextMenu` page upstream.

Scope corrections
------------------

A handful of sections describe different hardware than the official guide.
For example, the LED settings on the :doc:`Device Manager` page are no
longer described as Lite-only, since the CharaChorder Master Forge also has
them.

Presentation choices
----------------------

The generated tables make a couple of small, deliberate choices that make
their output differ from the hand-written original: enum values are kept in
the Meta API's lower case rather than capitalized, and single-letter unit
labels on HSB (hue/saturation/brightness) settings are suppressed, since the
API applies them inconsistently there.
