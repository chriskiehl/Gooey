**Added:**

* Support ``colored`` 2.x. Gooey now accepts ``colored>=1.3.93`` instead of ``colored>=1.3.93,<2``.

**Changed:**

* New installs of Gooey now get ``colored`` 2.x. Programs that use names only found in ``colored`` 1.x, such as ``colored.fore.RED``, ``colored.style.BOLD``, or ``attr('underlined')``, need to pin ``colored<2`` or switch to the 2.x names, such as ``colored.Fore.red``, ``colored.Style.bold``, or ``attr('underline')``.

**Deprecated:**

* <news item>

**Removed:**

* <news item>

**Fixed:**

* Fix the rich text console failing to open with ``colored`` 2.x installed when ``richtext_controls=True``.
* Fix ``colored`` 1.4+ and 2.x output showing without colors in the rich text console. Gooey now sets ``FORCE_COLOR=1`` for the program it runs when ``richtext_controls=True``, unless ``FORCE_COLOR`` or ``NO_COLOR`` is already set.

**Security:**

* <news item>
