**Added:**

* Support ``colored`` 2.x. Gooey now accepts ``colored>=1.3.93`` instead of ``colored>=1.3.93,<2``.

**Changed:**

* <news item>

**Deprecated:**

* <news item>

**Removed:**

* <news item>

**Fixed:**

* Fix the rich text console failing to open with ``colored`` 2.x installed when ``richtext_controls=True``.
* Fix ``colored`` 1.4+ and 2.x output showing without colors in the rich text console. Gooey now sets ``FORCE_COLOR=1`` for the program it runs when ``richtext_controls=True``, unless ``FORCE_COLOR`` or ``NO_COLOR`` is already set.

**Security:**

* <news item>
