Device Manager
==============

The CharaChorder Device Manager is the one-stop-shop for users with a CCOS-powered device. It boasts high quality graphics, animations and a simple user interface. On the device manager, you can change your device's :ref:`layout<Device Manager:Layout>`, manage your :ref:`chord library<Device Manager:Library>`, and adjust your :ref:`settings<Device Manager:Device>`.

In this section, we'll talk about the device manager and how you can navigate around it to configure your device to your liking. First, we'll discuss the website and where to find useful buttons on it, then we'll cover the main pages on the device manager and how to use them, and, lastly, we'll touch upon some other features and useful tools on the manager.

Feel free to use the links below to skip to whatever section you would like to read or scroll to start with the first section.

.. contents:: Table of Contents of this Page
   :local:


Connecting to the Device Manager
********************************

You can follow the steps below to connect to the device manager for the first time.

.. Note::
	If you have connected this device from this browser before, you can skip the serial port permission popup: click "Connect" and choose your device from the :ref:`Recent Devices<Recent Devices>` list instead.

1. On a chromium based browser, such as Chrome or Edge, go to the `CharaChorder Device Manager <https://charachorder.io>`__
2. Click “Connect” at the bottom center of the screen
3. When the popup box comes up that reads “charachorder.io wants to connect to a serial port”, choose your CharaChorder device, then click the “Connect” button

.. image:: /assets/images/ManagerSELECTDEVICE.png
  :width: 400
  :alt: Image showing the dialogue box requesting permission to open a serial connection

If these steps were performed correctly, you can see the connected device name in the bottom bar where "Connect" was previously.

.. _Recent Devices:

Once you've connected a device this way, the browser remembers it. The next time you click "Connect", you'll see a "Recent Devices" list with that device already in it -- click its name to reconnect without going through the serial port permission popup again.

.. _serialportaccess:

Linux Serial Port Access
------------------------

.. warning::
    For **Linux** based users: serial port access is often restricted to specific user groups for security.
    To enable serial port access in a browser like Chromium, you'll need to add your user to the appropriate
    group based on your Linux distribution.  Follow the steps below to grant access.


For Ubuntu, Debian, Fedora, Linux Mint, openSUSE, CentOS, Elementary OS, Zorin OS:

.. code-block:: bash

    sudo usermod -aG dialout $USER

For Arch Linux, Manjaro:

.. code-block:: bash

	sudo usermod -aG uucp $USER

Replace ``$USER`` with your username or use ``$USER`` to automatically reference the current user.
Log out and log back in for the changes to take effect.

If the above commands don't work, check the group ownership of the serial device (e.g., ``/dev/ttyUSB0``) using:

.. code-block:: bash

    ls -l /dev/ttyUSB0

This command will display the device's group. Replace ``/dev/ttyUSB0`` with the appropriate device file for your system.
After identifying the group (e.g., ``dialout``, ``uucp``, or another), add your user to that group using:

.. code-block:: bash

    sudo usermod -aG <group_name> $USER

Replace ``<group_name>`` with the name of the group displayed in the previous step.
Log out and log back in to apply the changes. Your user will now have the necessary permissions to access the serial port.

Device Manager Website
**********************

The device manager comes with a navigation menu on the left hand side of the screen.
Otherwise, regardless of what page you are on, there are a few helpful buttons you should know about.

Connect / Device name
---------------------

The bottom center of the screen is where you connect to your device and see which you are connected to, as well as other info such as the site version and your device's CCOS version.

Undo and Redo
-------------

.. image:: /assets/images/ManagerUndoRedo.png
  :alt: The Undo and Redo arrows

Near the top left corner, the device manager has handy undo and redo buttons which do exactly what their names describe. If you're making changes to your layout, your chords, or your layout, you can step back, one change at a time, all the way back to the very first change that you made during that session. Once you're stepped back, you can step forward to redo the change(s) that was/were undone.

Color Scheme
------------
On the bottom right of the device manager, you'll see a circle with a solid color. Hovering over this circle will reveal the label "color scheme." You can click this circle to change the color scheme of the device manager. In the color scheme menu, you can choose your preferred color using a color pallette, an RGB color system, or by clicking the dropper icon to choose a color on your screen.

.. image:: /assets/images/ManagerColorScheme.png
  :alt: The Color Scheme Menu

Light and Dark Mode
-------------------
Also in the bottom right-hand corner, you'll find a sun or moon icon where you can toggle between light and dark mode. This toggle can help those who would rather a brighter screen to see better or a darker screen to reduce eye strain.

Apply Button
------------

.. image:: /assets/images/ManagerSaveButton.png
  :alt: The Apply Button

If you make changes in the :ref:`library<Device Manager:Library>`, the :ref:`layout editor<Device Manager:Layout>` or the :ref:`device menu<Device Manager:Device>`, a colored "apply" button will pop up on your screen, towards the top left corner.

.. Note::
	Your changes will not take effect until you click the apply button.


Device
******
The Device Tab is the place where you can configure most settings of your :ref:`connected<Device Manager:Connecting to the Device Manager>` CCOS device and create backups.
Read on to see the different settings you can change. You can find more detailed explanations in the :doc:`GTM<GenerativeTextMenu>` section.

Backup Section
--------------

There are different kinds of backups that you can create on the Device Manager -- of your chords, your layout, or even your settings -- and we'll cover all of them below. These backups are made using the "Backup" box in the :ref:`Device Section<Device Manager:Device Section>`.

Creating a Backup
~~~~~~~~~~~~~~~~~
.. Note::
	In order to follow these steps, you must already have your device :ref:`connected<Device Manager:Connecting to the Device Manager>` to the device manager.

1. Open the Settings tab and scroll down to the "Backup" box.

2. Choose an individual "Library", "Layout" or "Settings" backup to download to your computer, or select "Full profile" to download a single file with all three parts. The file(s) will be downloaded in .json format.

	.. note::
		You can make individual backups of just your chords, just your layout, or just your settings. The "Full profile" option will download all three of these in a single file instead of three separate files.

3. If prompted, select a location to save to on your computer and rename the file to your liking.

Congratulations! Now you have created a backup.

Restoring from a Backup
~~~~~~~~~~~~~~~~~~~~~~~
Additionally, you can restore your chords, your layout, and your settings on the Device Manager. Follow the steps below to do so.

.. Note::
	In order to follow these steps, you must already have your device :ref:`connected<Device Manager:Connecting to the Device Manager>` to the device manager.

1. Open the Settings tab and scroll down to the "Backup" box.

2. Click on "Restore".

3. Select a file to use to restore from. This file should be in .json format.

	.. note::
		Files that you can restore from will have been created ahead of time by following the :ref:`steps to create a backup<Device Manager:Creating a Backup>`.

4. If there are changes, the :ref:`apply button<Device Manager:Apply Button>` will appear on the top left. Note the changes in the appropriate tab. If you restored chords, check the :ref:`chords tab<Device Manager:Library>`, if you restored a layout, check the :ref:`layout tab<Device Manager:Layout>`, and if you restored settings, check the :ref:`settings tab<Device Manager:Device>`.

	.. note::
		The restore feature does NOT erase data from your device. If there is a conflict (such as a changed setting, a different key in the layout, or a chord that has a different :ref:`output<Chords:Chord Output>`), that will be overwritten by the restore file. Settings and layout backups ALWAYS overwrite everything.

5. Once you see the changes that the restore file made, you can click :ref:`apply<Device Manager:Apply Button>` to apply the changes.

Device Section
--------------

The settings box that used to live here has since split into two smaller boxes: Misc and Backup.

Misc
~~~~
.. image:: /assets/images/ManagerSettingsMisc.png
  :alt: The Misc settings box

Here you can select your device's operating system and toggle :ref:`realtime feedback<GenerativeTextMenu:Realtime Feedback>` on or off.

Backup
~~~~~~
.. image:: /assets/images/ManagerSettingsBackup.png
  :alt: The Backup settings box

This box lets you export your library, layout, or settings individually, download or restore a full profile backup, reset your device to factory settings, or enter recovery mode.

Arpeggiates
-----------
.. dropdown:: What are arpeggiates?

	Arpeggiate actions are timed actions that can modify a :ref:`chord<Chords:What are Chords?>` after the chord is performed. A quick example of this is the use of :ref:`chord modifiers<Device Manager:Chord Modifiers>` after you perform the chord. You can read that section for information on how the chord modifiers work.

	With arpeggiates enabled, you can chord the word run and then, within the :ref:`arpeggiate timeout window<GenerativeTextMenu:Arpeggiate Timeout>`, press the :ref:`past tense modifier<Device Manager:Past Tense>` for the word to be “modified” into its past tense variant; in english, ran.

.. image:: /assets/images/ManagerSettingsArpeggiates.png
  :alt: The Arpeggiates settings box

In this box, ou can enable or disable arpeggiates as well as increase or decrease the :ref:`arpeggiate timeout setting<GenerativeTextMenu:Arpeggiate Timeout>`.

.. dropdown:: Mode

	.. ccos-setting:: arpeggiates/mode

Chord Modifiers
---------------
.. dropdown:: What are chord modifiers?

	Chord modifiers are actions that change a chord when :ref:`chorded<Chords:What are Chords?>` at the same time as the :ref:`chord input<Chords:Chord Input>`, or when pressed immediately after (arpeggiately) the :ref:`chord<Chords:What are Chords?>`, provided that :ref:`arpeggiates<GenerativeTextMenu:Arpeggiate>` are enabled.

	As of February of 2024, only the CharaChorder One and CharaChorder Lite support the use of chord modifiers. Additionally, as of that same time, chord modifiers only work in English.

	.. note::
		Chord modifiers are NOT the same as keyboard modifiers. Keyboard modifiers affect keys pressed on a keyboard. Those keys include ``CTRL``, ``ALT``, and ``FN``. Chord modifiers affect chords.

Capitalization
~~~~~~~~~~~~~~
The capitalization modifier modifies any chord so that the first letter is capitalized on :ref:`output<Chords:Chord Output>`. This :ref:`modifier<Device Manager:Chord Modifiers>` can be performed together with a :ref:`chord<Chords:What are Chords?>` or :ref:`arpeggiately<GenerativeTextMenu:Arpeggiate>`.

The capitalization modifier is located on the ``SHIFT`` key. In the :ref:`layout editor<Device Manager:Layout>`, this key can be either "Shift Keyboard Modifier (Left)" or "Shift Keyboard Modifier (Right)".

.. note::
	If you have ``CAPS LOCK`` active, all letters in a chord will be capitalized except the first one when using this modifier.

Present Tense
~~~~~~~~~~~~~
The present tense modifier modifies supported chords so that they turn into their present tense variants. The word "run" would be modified into "running" and the word "work" would be turned into "working". This :ref:`modifier<Device Manager:Chord Modifiers>` can be performed together with a :ref:`chord<Chords:What are Chords?>` or :ref:`arpeggiately<GenerativeTextMenu:Arpeggiate>`.

The present tense modifier has different locations depending on your device. On the CharaChorder One, this modifier is linked to the "AMBIDEXTROUS THROWOVER (LEFT)" key. On the CharaChorder Lite, it's linked to the "NUMERIC LAYER (LEFT)" key.

Pluralizer
~~~~~~~~~~
The pluralizer modifier makes supported chords plural. It will add an "s" or "es" to the end of supported chords. "Box" will turn into "boxes" and "dog" will become "dogs". This :ref:`modifier<Device Manager:Chord Modifiers>` can be performed together with a :ref:`chord<Chords:What are Chords?>` or :ref:`arpeggiately<GenerativeTextMenu:Arpeggiate>`.

The pluralizer modifier has different locations depending on your device. On the CharaChorder One, it's linked to the "AMBIDEXTROUS THROWOVER (RIGHT)" key. On the CharaChorder Lite, it's linked to the "RIGHT SPACEBAR" key, not to be confused with the "SPACE" key.

Past Tense
~~~~~~~~~~
The past tense modifier modifies supported chords so that they turn into their past tense variants. The word "run" would be modified into "ran". The word "work" would be turned into "worked". This :ref:`modifier<Device Manager:Chord Modifiers>` can be performed together with a :ref:`chord<Chords:What are Chords?>` or :ref:`arpeggiately<GenerativeTextMenu:Arpeggiate>`.

The past tense modifier has different locations depending on your device. On the CharaChorder One, it's linked to the "NUMERIC LAYER (LEFT)" key. On the CharaChorder Lite, it's linked to the "SPACE" key, not to be confused with the "RIGHT SPACEBAR" key.

Comparative
~~~~~~~~~~~
The comparative modifier modifies supported chords so that they turn into their comparative variant. "Big" becomes "bigger" and "small" turns into "smaller". This :ref:`modifier<Device Manager:Chord Modifiers>` can be performed together with a :ref:`chord<Chords:What are Chords?>` or :ref:`arpeggiately<GenerativeTextMenu:Arpeggiate>`.

The comparative modifier is located on the "NUMERIC LAYER (RIGHT)" key on both the CharaChorder One and the CharaChorder Lite.


Character Entry
---------------
.. dropdown:: What is Character Entry?

	Character entry, known to the CharaChorder community as "chentry," refers to typing one character at time.

.. dropdown:: Swap Keymap 0 and 1

	This setting will swap the behavior of the two keys on the bottom-left of the CharaChorder Lite.

	Traditional QWERTY keyboards keep the ``CTRL`` key at the bottom left corner of the keyboard with the ``GUI`` key (Command key on Mac, Windows key on Windows, Super key on Linux, etc.) to the right of the ``CTRL`` key. The CharaChorder Lite has these two keys swapped by default, which some users find odd and difficult to adjust to. A brand new CharaChorder Lite will have the ``GUI`` key at the bottom-left corner with the ``CTRL`` key to the right of the ``GUI`` key.

	With this setting, you can effectively swap the two keys’ location at the level of the CCOS so that CTRL is at the bottom-left corner.

.. dropdown:: Character Entry (chentry)

	This setting is a toggle that disables chording capabilities on CCOS devices. It is off by default and can be enabled in case we don’t want any chording at all. This setting can be useful in cases where we don’t want to accidentally trigger chords unintentionally, such as when gaming.

	If your CCOS device suddenly loses its chording ability, it’s a good idea to check if this setting is toggled off.

.. dropdown:: Key Debounce Press

	The debounce press setting refers to the time frame (measured in milliseconds) in which :doc:`CCOS<CCOS>` will filter out duplicate key activations on a press event. In other words, any duplicate activations within the given time frame will only be counted as one.

	We should adjust this setting if we are having unintentional duplicate characters while typing. Increasing this value will lower the probability that unwanted duplicate characters will appear because it tells :doc:`CCOS<CCOS>` to wait longer before typing an additional character that’s assigned to the same switch-direction. However, having this setting set too high might also cause issues with :doc:`CCOS<CCOS>` not reading intentional double-presses, so it’s recommended to try different numbers in small increments. This setting should be used in connection with the debounce release setting.

.. dropdown:: Key Debounce Release

	The debounce release setting refers to the time frame (measured in milliseconds) in which :doc:`CCOS<CCOS>` will filter out duplicate key activations on a release event. In other words, any duplicate activations within the given time frame will only be counted as one.

	We should adjust this setting if we are having unintentional duplicate characters while typing. Increasing this value will lower the probability that unwanted duplicate characters will appear because it tells :doc:`CCOS<CCOS>` to wait longer before typing an additional character that’s assigned to the same switch-direction. However, having this setting set too high might also cause issues with :doc:`CCOS<CCOS>` not reading intentional double-presses, so it’s recommended to try different numbers in small increments. This setting should be used in connection with the debounce press setting.


Keyboard
--------
.. image:: /assets/images/ManagerSettingsKeyboard.png
  :alt: The Keyboard settings box

In this box, you can adjust settings relating to :doc:`CCOS'<CCOS>` keyboard input, or turn keyboard input off altogether.

.. dropdown:: Enable

	Turns the device's keyboard input off entirely. Chording and mouse input, controlled by their own "Enable" toggles below, keep working independently of this one.

.. dropdown:: Command Control Swap

	Swaps the ``CTRL`` and ``GUI`` (Command on Mac) keys, to make transitioning between Mac and other systems easier.

	You can read a more in-depth explanation in the :ref:`GTM section<GenerativeTextMenu:GUI-CTRL Soft Swap>`.

.. dropdown:: Debounce Press

	The debounce press setting refers to the time frame (measured in milliseconds) in which :doc:`CCOS<CCOS>` will filter out duplicate key activations on a press event.

	You can read a more in-depth explanation in the :ref:`GTM section<GenerativeTextMenu:Debounce Press>`.

.. dropdown:: Debounce Release

	The debounce release setting refers to the time frame (measured in milliseconds) in which :doc:`CCOS<CCOS>` will filter out duplicate key activations on a release event.

	You can read a more in-depth explanation in the :ref:`GTM section<GenerativeTextMenu:Debounce Release>`.

.. dropdown:: Rollover

	How many keys can be held at once and still be detected by your PC, excluding modifier keys. Older hardware or especially BIOS/UEFI might only support 6-key rollover. This only affects reporting to the host system; CCOS always uses full n-key rollover. Requires a replug to be effective.

	.. ccos-setting:: keyboard/rollover

Mouse
-----
.. dropdown:: Mouse???

	:doc:`CCOS<CCOS>` has mouse functionality. This means that your CharaChorder, or CCOS-powered keyboard, has the ability to control your computer's mouse. These settings affect the mouse usage on your CharaChorder.

.. image:: /assets/images/ManagerSettingsMouse.png
  :alt: The Mouse settings box

In this box, you can adjust settings relating to :doc:`CCOS'<CCOS>` mouse abilities.

.. dropdown:: Enable

	Turns the device's mouse functionality off entirely.

.. dropdown:: Mouse Speed(s)

	:doc:`CCOS<CCOS>` has two mouse speeds, a fast speed and a slow speed. The slow speed is activated when you use only one of the mouse keys in a single direction (as opposed to using 2 keys in the same direction). The fast speed is activated when you use two mouse keys in a single direction (as opposed to using only one key in the same direction).

	You can read a more in-depth explanation of mouse speeds in the :ref:`GTM section<GenerativeTextMenu:Slow Speed>`.

.. dropdown:: Scroll Speed

	Scroll speed refers to the speed at which your :doc:`CCOS<CCOS>` scroll will scroll.

	You can read a more in-depth explanation of the scroll speed in the :ref:`GTM section<GenerativeTextMenu:Scroll Speed>`.

.. dropdown:: Scroll Throttle

	Scroll throttle sets the shortest time CCOS will leave between two scroll events. It exists because Windows struggles to process fast scrolling: without a gap between the events, some of them are dropped and the page scrolls less than you asked for.

	Increase this setting if scrolling is unreliable on your computer. Lower it if scrolling feels sluggish and your computer keeps up with it.

	.. ccos-setting:: mouse/scroll throttle

.. dropdown:: Caffeine

	Caffeine nudges your mouse cursor one pixel every minute or so (not a specific timing). This setting can be used to keep your computer from going to sleep. You might turn this setting off if you notice desktop apps are preventing you from getting mobile notifications (for example on Discord or Microsoft Teams).

Gaming
------
.. image:: /assets/images/ManagerSettingsGaming.png
  :alt: The Gaming settings box

.. dropdown:: Layer Warp

	Re-presses held keys with their new layer's mappings when you switch layers while still holding them down.

	.. ccos-setting:: gaming/layer warp

Fuzzy modifiers
---------------
.. image:: /assets/images/ManagerSettingsFuzzyModifiers.png
  :alt: The Fuzzy modifiers settings box

Modifiers (like ``SHIFT`` or a layer key) normally only work if you press them before the key you want to modify, and release them before pressing any key you don't want modified. Fuzzy modifiers relax this rule: they let you press or release the modifier at almost the same time as the key, checking whether the modifier's press or release happened close enough in time to the key press instead of requiring a strict order.

.. dropdown:: Enable

	Turns fuzzy modifiers off entirely. The three thresholds below have no effect while this is off.

.. dropdown:: Press theshold

	The time between a modifier press and the previous key press.

	.. ccos-setting:: fuzzy modifiers/press theshold

.. dropdown:: Release theshold

	The time between a modifier release and the previous key press.

	.. ccos-setting:: fuzzy modifiers/release theshold

.. dropdown:: Release guard threshold

	The time between a modifier press and a subsequent key press that prevents the next modifier release from affecting it.

	.. ccos-setting:: fuzzy modifiers/release guard threshold

Chording
--------
.. dropdown:: What is Chording?

	Chording is the beautiful ability of pressing multiple keys at a time to get a predefined output, whether it's a single word, an entire phrase, or important addresses.

	A chord is a type of input/output action on a keyboard: you press two or more keys at the same time and release them at the same time, after which a predefined output will replace the originally pressed keys.

	By chording, we are able to type one word at a time instead of one letter at a time. It’s even possible to have chords for phrases and entire sentences.

.. image:: /assets/images/ManagerSettingsChording.png
  :alt: The Chording settings

In this box, you can adjust settings relating to :doc:`CCOS'<CCOS>` :doc:`chording<Chords>` abilities as well as turn off :doc:`chording<Chords>` altogether, should you choose to.

.. dropdown:: Press Tolerance

	The press tolerance refers to a window of time in which a chord can be performed, measured in milliseconds (ms). This timer is initiated upon the first “press” action of the first key in a chord and ends once the last key of the chord is pressed, or until the press tolerance runs out, whichever comes first. Read the :ref:`GTM section<GenerativeTextMenu:Press Tolerance>` for a more in-depth explanation.

.. dropdown:: Release Tolerance

	The release tolerance refers to a window of time in which a chord can be performed, measured in milliseconds (ms). This timer is initiated upon the first “release” action of any key in a chord and ends once the chord is fully performed, or until the release tolerance runs out, whichever comes first. Read the :ref:`GTM section<GenerativeTextMenu:Release Tolerance>` for a more in-depth explanation.

.. dropdown:: Minimum Chord Keys

	The fewest keys, pressed at the same time, that count as a chord. Setting this to 1 can very slightly affect typing latency.

	.. ccos-setting:: chording/minimum chord keys

.. dropdown:: Tap Dance Tolerance

	.. ccos-setting:: chording/tap dance tolerance

.. _Compound Timeout Setting:
.. dropdown:: Compound timeout

	The Compound timeout determines if a :ref:`compound chord<Chords:Compound Chords>` succeeds or fails.

	If the time between the individual chords in a compound chord is:

	* less than the Compound timeout, then it succeeds and the individual chords are replaced with the compound chord's output
	* greater than the Compound timeout, then it fails and the individual chords remain

.. dropdown:: Detection method

	There are three detection methods:

	* Latency (classic) mode. Each key is printed instantly and backspaced after a successful chord.
	* Smart adds a small amount of latency depending on your tolerances, and only prints characters when it is no longer plausible for the inputs to be a chord input.
	* Continuous (spurring) allows you to jump from one chord to the next without releasing all keys, with more potential speed traded against the flexibility of character entry.

.. dropdown:: Concatenation Style

	Appended (classic) places spaces directly after a chord. Recommended for typists. Prepended places spaces lazily between two chords. Recommended for text editing and coding.

	.. ccos-setting:: chording/concatenation style
	   :columns: Device, Default

Autocorrect
-----------

.. image:: /assets/images/ManagerSettingsAutoCorrect.png
  :alt: The Autocorrect settings

.. dropdown:: Maximum attempts

	Set to 0 to turn off autocorrect. An attempt is every stroke from the first keypress to the next full release. Recommended to turn off when you are comfortable using Quickfix.

.. dropdown:: Timeout

	This setting will change how long CCOS counts time in order to replace characters that precede a chord.

	CCOS devices have a running timer that starts after every single character that is entered in traditional chentry (character entry, i.e. one letter at a time). This timer controls whether or not the next chord that you perform deletes the preceding characters.

	This feature allows users to misfire chords, yet be able to correct them by quickly performing the chord correctly, without having to backspace manually to erase the misfired chord. The result is that the timeout will automatically backspace all of the preceding characters (up to the last breaking character) and replace them with the intended chord.

RGB
---
These settings adjust the color and brightness of the LEDs on the devices that have them: the :doc:`CharaChorder Lite<CharaChorder_Lite>` and the :doc:`Master Forge<Master Forge>`. The Master Forge stores them per half, so each :ref:`digitizer<Master Forge:The Digitizers>` can be lit in its own color.

The :ref:`GTM<GenerativeTextMenu:LEDs>` only offers the on/off toggle and the brightness slider. Everything below is only reachable here.


.. image:: /assets/images/ManagerSettingsRGB.png
  :alt: The RGB settings box

.. dropdown:: Enable

	Turns the LEDs off entirely.

.. dropdown:: Color

	This box is a single color picker, not separate hue, saturation and brightness fields: picking a color sets all three settings below at once.

	.. ccos-setting:: leds/hue
	   :devices: lite_s2, m4g_s3

	.. ccos-setting:: leds/saturation
	   :devices: lite_s2, m4g_s3

	.. ccos-setting:: leds/brightness
	   :devices: lite_s2, m4g_s3

.. dropdown:: Effect

	Chooses whether the LEDs hold a static color or cycle through the rainbow.

	.. ccos-setting:: leds/effect
	   :columns: Device, Default
	   :devices: lite_s2, m4g_s3

.. dropdown:: Effect Cycle

	How long one full rainbow cycle takes. Confirmed on a CharaChorder Lite: this field stays enabled and adjustable even while the Effect setting above is set to Static, though it has nothing to affect until Effect is switched back to Rainbow.

	.. ccos-setting:: leds/effect cycle
	   :devices: lite_s2, m4g_s3

.. dropdown:: Off delay

	Confirmed on a CharaChorder Lite: the delay between turning the LEDs off and the first LED actually going dark.

	.. ccos-setting:: leds/off delay
	   :devices: lite_s2, m4g_s3

.. dropdown:: On off transition

	Confirmed on a CharaChorder Lite: once the first LED has changed state, how long the rest take to follow it one by one, whether that is fading out until every LED is off or fading in until every LED is lit.

	.. ccos-setting:: leds/on off transition
	   :devices: lite_s2, m4g_s3

USB
---
These settings are experimental. They are not in the :doc:`GTM<GenerativeTextMenu>`, so the Device Manager and the :doc:`Serial API<SerialAPI>` are the only ways to change them.

.. image:: /assets/images/ManagerSettingsUsb.png
  :alt: The Usb settings box

.. dropdown:: Poll Rate

	The polling rate (poll rate) is the frequency at which the device sends its input reports to the computer it is connected to, expressed in Hz (Hertz). At 1000 Hz the device reports 1000 times every second.

	Changing this setting requires unplugging and replugging the device before it takes effect.

	This setting arrived in CCOS 2.2.0, replacing the separate mouse and keyboard poll rate settings. Those older settings did not actually change the poll rate.

	.. ccos-setting:: usb/poll rate
	   :columns: Device, Default

.. dropdown:: Aggressive Reporting

	Some hardware combinations, especially with USB hubs, might cause the host to time out waiting for responses. Enabling this setting will cause the device to always respond with the last report.

	.. ccos-setting:: usb/aggressive reporting
	   :columns: Device, Default

.. dropdown:: Aggressive Reporting Throttle

	.. ccos-setting:: usb/aggressive reporting throttle

.. dropdown:: Hid Resend Throttle

	.. ccos-setting:: usb/hid resend throttle

Library
*******
.. image:: /assets/images/ChordManager.png
  :width: 1200
  :alt: A picture of the Library

The Library is a powerful tool that lets you add, delete and edit chords stored in your chord library. It's easy to use and quick to load. We'll go over how to use it below.

When you :ref:`connect<Device Manager:Connecting to the Device Manager>` your device to the device manager, the webpage will start reading the chords on your device. It may take a couple of seconds — or even over a minute for very large libraries — to load the first time. Reconnecting a device you've connected before, e.g. via the :ref:`Recent Devices<Recent Devices>` list, loads much faster.

Chords displayed here are shown in alphabetical order, using the list of :ref:`chord outputs<Chords:Chord Output>`. The number of chords shown on the library depends on your screen size and browser zoom settings. Above the chords list, you'll see the search bar which will display the number of chords on your CCOS device until something is typed there.

.. _search bar:

You can search through your chords by searching :ref:`chord outputs<Chords:Chord Output>` (the word that displays once you've performed a chord). This textbox is not case sensitive, so you can type in capital or lowercase letters regardless of whether or not the chord has a capital letter in it. This search bar is also intuitive enough that you are also able to search partial words/phrases.

To the right of the search bar, you'll find two numbers separated by a forward slash (``/``). These numbers indicate the page number that you're on out of the total number of pages that compose your chord library. Using the angle brackets to the right of those numbers will allow you to flip through the different pages of your chord library which is sorted in alphabetical order.

Under the page-turning brackets, you'll see a tall box with the text "Try typing here". You can use this text box to test your new chords as you edit them in the manager.

Under the text box if your device supports it you can find some shortcuts to help you clear your chord library, add back in the starter chords that came on your device, add functional utility chords, and download a text file with all of your chord outputs separated by a pipe character for importing into practice tools.

Finally, at the bottom of the page, if you hover over the Device name you'll notice that you can hold Shift and click on it to "Sync".  If you do this, it will have the device manager read your device's chord library again. This process can take a few seconds.

Creating a Chord
----------------
You can follow the steps below to create a new chord on the device manager.

.. Note::
	In order to follow these steps, you must already have your device :ref:`connected<Device Manager:Connecting to the Device Manager>` to the device manager.

1. Find the "New chord" text under the :ref:`search bar<search bar>` and click it.


2. When the text displays "Hold chord," press and hold all of the keys that you want to use as your :ref:`chord input<Chords:Chord Input>`. Once you have pressed all of the keys, release the keys.

    You will now see the :ref:`chord input<Chords:Chord Input>` in the left column as letters inside individual boxes. These boxed-letters will be highlighted in a color (as opposed to black or white). The color depends on your selected :ref:`color scheme<Device Manager:Color Scheme>`. You will also notice a single, floating dot highlighted in the same color off to the right of the boxed-letters.

	.. Note::
		You can add any number of chords at a time without defining the desired :ref:`chord output<Chords:Chord Output>`.

	.. Warning::
		If you click :ref:`apply<Device Manager:Apply Button>`, before defining a :ref:`chord output<Chords:Chord Output>` as described in :ref:`step three<Step 3>`, any chords that you've created will save to your device with a blank output and will lead to strange behavior.

.. _Step 3:

3. Click into the text box to the right of the :ref:`chord input<Chords:Chord Input>` that you created in the previous step and type your desired :ref:`chord output<Chords:Chord Output>`.

	.. dropdown:: Using Action Codes

		As you type your :ref:`chord output<Chords:Chord Output>`, you'll notice that your cursor will have a bubble with a ``+`` above it. You can click this to open the :ref:`action codes menu<Device Manager:Using Action Codes>` where you can search for specific action codes or browse through the action codes available to assign into a :ref:`chord output<Chords:Chord Output>`. Read the :ref:`action codes section<Device Manager:Using Action Codes>` for information on the different kinds of action codes.

	As you type, you'll notice that your text has changed color to match your :ref:`color scheme<Device Manager:Color Scheme>` and that the end of your text has a floating dot immediately to the right.

4. Once you are satisfied with your :ref:`output<Chords:Chord Output>`, you can proceed to modify another chord or click :ref:`apply<Device Manager:Apply Button>`.


Deleting a Chord
----------------
You can follow the steps below to delete a chord in the device manager.

.. Note::
	In order to follow these steps, you must already have your device :ref:`connected<Device Manager:Connecting to the Device Manager>` to the device manager.

1. Locate the chord that you would like to delete.

2. When you hover over the chord that you would like to delete, you will notice a small trash icon appear in line with that chord map. Click the trash icon in order to mark it for deletion.

	When you click the trash icon, the boxed-letters in the left column will have a line through them and they will turn red. You can unmark chords for deletion by clicking the "undo" arrow next to the trash icon. The chord will return to its original color and the line will disappear.

	.. Tip::
		You can mark multiple chords for deletion at a time. Flipping through the pages in your chord library will not unmark the chords that you have marked for deletion.

3. Once you have marked the undesired chords for deletion and are ready to delete them, click the :ref:`apply button<Device Manager:Apply Button>`.

	Once you click save, the marked chord maps will disappear from the list.


Editing a Chord
---------------
You can follow the steps below to edit an existing chord in the device manager.

.. Note::
	In order to follow these steps, you must already have your device :ref:`connected<Device Manager:Connecting to the Device Manager>` to the device manager.

1. Locate the chord that you would like to edit.

2. Click the textbox in the right column where the :ref:`chord output<Chords:Chord Output>` is displayed.

3. Edit the :ref:`chord output<Chords:Chord Output>` to be whatever you would like. As you type, you will notice that the text changes color to match your :ref:`color scheme<Device Manager:Color Scheme>` and that the end of your text has a floating dot immediately to the right.

	.. dropdown:: Using Action Codes

		As you type your :ref:`chord output<Chords:Chord Output>`, you'll notice that your cursor will have a bubble with a ``+`` above it. You can click this to open the :ref:`action codes menu<Device Manager:Using Action Codes>` where you can search for specific action codes or browse through the action codes available to assign into a :ref:`chord output<Chords:Chord Output>`. Read the :ref:`action codes section<Device Manager:Using Action Codes>` for information on the different kinds of action codes.

	.. Tip::
		You can edit multiple chords before :ref:`applying<Device Manager:Apply Button>` your changes. Flipping through the pages in your chord library will not undo the changes that you have made to your existing chords.

4. Once you are ready to :ref:`apply<Device Manager:Apply Button>` your changes, click :ref:`apply<Device Manager:Apply Button>`.

	Once you click :ref:`apply<Device Manager:Apply Button>`, the chord(s) that you've modified will change color to match the rest of the list and the floating dot will disappear.

Share button
------------
Next to every chord, you will see a share icon. You can share individual chord maps with others by pressing this button. When you do, your computer's clipboard will copy a URL that you can share with anyone who can then add that exact chord map to their own CharaChorder through the Device Manager.

When you follow a chord map link, you'll be taken to the Library where you'll see the new chord map ready to be :ref:`applied<Device Manager:Apply Button>`.


Layout
******
The Device Manager has a very intuitive layer editor. It's the third option in the main navigation bar at the left of the page. When you go to this tab, you'll see a diagram of your device, with each key filled in with the corresponding :ref:`action code<Device Manager:Using Action Codes>`.


Layer Selector
--------------

.. dropdown:: Explanation of Layers on CCOS Devices

	As of CCOS 3.0.0, :doc:`CCOS<CCOS>` devices come with four (4) layers that you can make use of: the base layer, called the A1 (Alpha) layer, the secondary layer, referred to as A2 (Numeric), the tertiary layer, named A3 (Function), and the quaternary layer, named A4 (Flag).

	In order to access layers, you need to press and hold a "layer access" button. You MUST hold the button in order to use keys mapped to layers other than the alpha layer. The alpha layer is active by default.

	.. note::
		In this section, we’ll refer only to the default layouts on CCOS devices. If you have modified your layout to something different, then the next portion might not be accurate for your device. If you have purchased your device from CharaChorder, then the following is accurate to your device.

	**A1 Layer**

	The A1 layer, also known as the alpha layer, is the main layer that is active by default. Your device will always be in the A1 layer upon boot.

	**A2 Layer**

	The A2 layer, sometimes referred to as the numeric layer, is accessible with the :doc:`A2 access key<CharaChorder Keys>`. In the Device Manager, this key has the name “Numeric Layer (Left)” and “Numeric Layer (Right)”, one for each hand.

	The A2 Layer is accessible by pressing and holding one layer access button. Any key that is mapped to the A2 Layer can only be accessed by pressing and holding the A2 Layer access key along with the target key. You do not need to :doc:`chord<Chords>` the keys together; it’s only required that the A2 Layer access key is pressed while the target key is pressed.

	**A3 Layer**

	The A3 layer, sometimes referred to as the “function layer”, is accessible with the :doc:`A3 access key<CharaChorder Keys>`. In the Device Manager, this key is assignable by the names “Function Layer (Left)” and “Function Layer (Right)”.

	Once you’ve mapped the A3 layer access buttons, the A3 Layer is accessible by pressing and holding either one of them. You do not have to hold them both in order to access the A3 layer. Any key that is on the A3 Layer can only be accessed by pressing and holding the :doc:`A3 access key<CharaChorder Keys>`, along with the target key. You do not need to :doc:`chord<Chords>` the keys together; it’s only required that the A3 layer access key is pressed while the target key is pressed.

	**A4 Layer**

	The A4 layer, also known as the "Flag" layer, is accessible with the A4 access key, named "Flag Layer" in the Device Manager’s action codes menu (one entry for the left hand, one for the right, both sharing that name). It works the same way as the A2 and A3 layers: press and hold the A4 layer access key while pressing the target key.

	Unlike A1-A3, the A4 layer has no keys mapped by default -- every key starts out set to "No Action" -- so on a factory-default layout you’ll need to assign an A4 access key and remap the layer yourself before it does anything.

.. Note::
	The following section assumes that you have already :ref:`connected<Device Manager:Connecting to the Device Manager>` your device to the device manager.

.. image:: /assets/images/ManagerLayoutSelector.png
  :alt: Image of the Layer Selector bar

Above the diagram of your device, you'll see a row of tabs -- A1, A2, A3, A4 -- plus a circular icon. Click any tab to view and edit the keys mapped to that layer. The circular icon resets the currently selected layer back to its factory default; it doesn't undo edits to other layers.

.. Note::
	The tab labels change to match whichever :ref:`profile<Device Manager:Profile Selector>` is currently selected -- for example, they read B1-B4 while profile B is selected.

Profile Selector
-----------------

.. image:: /assets/images/ManagerProfileSelector.png
  :alt: Image of the Profile Selector buttons

Near the top of the page, next to the :ref:`Apply button<Device Manager:Apply Button>`, you'll see three buttons labelled A, B, and C -- the profile selector. Each profile has its own independent set of four layers (so profile A has layers A1-A4, profile B has B1-B4, and profile C has C1-C4) and its own settings; the chord library is shared across all three profiles. Clicking a letter here switches which profile you're viewing and editing in the Device Manager.

To switch the active profile on the device itself, assign the "Profile A", "Profile B", or "Profile C" action to a key or chord through the :ref:`action codes menu<Device Manager:Using Action Codes>` (all three are listed under the "Modifiers" category).

Remapping
---------
On the layer editor, you can remap your layout by using :ref:`action codes<Device Manager:Using Action Codes>`. Follow the instructions below to remap your device one key at a time.

How to Remap Your Keys
~~~~~~~~~~~~~~~~~~~~~~

.. Note::
	In order to follow these steps, you must already have your device :ref:`connected<Device Manager:Connecting to the Device Manager>` to the device manager.

1. Choose the :ref:`layer<Device Manager:Layer Selector>` where you want to change the key.

2. Click on the key that you would like to change. This will bring up the :ref:`action codes menu<Device Manager:Using Action Codes>`.

3. Use the search feature in the :ref:`action codes menu<Device Manager:Using Action Codes>` or scroll through available :ref:`action codes<Device Manager:What are Action Codes>`. Once you've found the desired :ref:`action code<Device Manager:Using Action Codes>`, click on it.

	Once you select the :ref:`action code<Device Manager:Using Action Codes>`, you will notice that the layout diagram now reflects the selected :ref:`action code<Device Manager:Using Action Codes>` highlighted according to your :ref:`color scheme<Device Manager:Color Scheme>` and it will be accompanied by a floating dot.

	.. Tip::
		You can edit multiple keys before :ref:`applying<Device Manager:Apply Button>` your changes. Flipping through the :ref:`layers<Device Manager:Layer Selector>` will not undo the changes that you have made to the layout so far.

4. Once you have changed the desired key(s), click the :ref:`apply button<Device Manager:Apply Button>`.

	.. note::
		Your changes will not take effect until you click :ref:`apply<Device Manager:Apply Button>`.

	Once you click :ref:`apply<Device Manager:Apply Button>`, the highlighted key(s) will lose their highlight and the floating dot will disappear. Your layout diagram will be black and white.

Using Action Codes
~~~~~~~~~~~~~~~~~~
You can use action codes in chord outputs as well as while :ref:`remapping<Device Manager:Remapping>` keys.

What are Action Codes
^^^^^^^^^^^^^^^^^^^^^
Action codes are data that :doc:`CCOS<CCOS>` interprets as characters. **Put simply, they are the characters that we see while typing.** These include letters, numbers, special characters, function keys, and others.

Action Code Menu
^^^^^^^^^^^^^^^^
You can open the action codes menu one of two ways:

1. While typing a chord :ref:`chord output<Chords:Chord Output>` in the :ref:`library<Device Manager:Library>`, you’ll notice that your cursor will have a bubble with a + above it. You can click this to open the action codes menu.

2. While editing your layout in the :ref:`layout editor<Device Manager:Layout>`, click on a key to bring up the action codes menu.

In this menu, you can scroll through :ref:`available action codes<Device Manager:Available Action Codes>` by :ref:`category<Device Manager:Action Code Categories>`, or simply search specific actions.

If you ever need to leave the action codes menu, simply click the X at the top right of the menu. This will close out the box and not make any changes.

Action Code Categories
......................
There are eight different categories in the action code menu. These are: ASCII Macros, ASCII, CharaChorder One, CharaChorder, CP-1252, Keyboard, Mouse, and Key Codes.



.. ASCII Macros
   ,,,,,,,,,,,,,,

   ASCII
   ,,,,,,,,,,,

   CharaChorder One
   ,,,,,,,,,,,,,,,,,,,,,,,,,

   CharaChorder
   ,,,,,,,,,,,,,,,,,,,,,,,,,

   CP-1252
   ,,,,,,,,,,,,,,,,,,,,,,,,,

   Keyboard
   ,,,,,,,,,,,,,,,,,,,,,,,,,

   Mouse
   ,,,,,,,,,,,,,,,,,,,,,,,,,

   Key Codes
   ,,,,,,,,,,,,,,,,,,,,,,,,,

Remove Button
.............
You can use the "Remove" button on the top right of the action codes menu to remove the currently assigned action code from the selected key in the :ref:`layout editor<Device Manager:Layout>`.

If you select the "Remove" button while typing a :ref:`chord output<Chords:Chord Output>` in the :ref:`library<Device Manager:Library>`, it will NOT remove any action. Instead, it will add a "blank" action that will be labeled ``0x0``.



Available Action Codes
^^^^^^^^^^^^^^^^^^^^^^
You can view the `action codes here. <https://docs.google.com/spreadsheets/d/1--T9bXshCIC-OVly-CY3rK87fgb7AHgJl3IySh7cmHc/edit#gid=0>`__
