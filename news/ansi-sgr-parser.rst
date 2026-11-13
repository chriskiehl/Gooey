**Added:**

* Support the standard ANSI style codes in the rich text console, not only the ones that ``colored`` sends. Output from other libraries, such as ``termcolor``, ``colorama``, or ``rich``, is now styled too. This adds basic and bright colors, colors given as red, green, and blue values, background colors, italic text, the standard end bold code (``22``), and several styles combined in one code such as ``\x1b[1;31m``.

**Changed:**

* Read escape codes with a parser in ``gooey/gui/util/ansi.py`` that does not need ``wx``. The rich text console no longer uses a lookup table of the exact codes that ``colored`` sends.

**Deprecated:**

* <news item>

**Removed:**

* <news item>

**Fixed:**

* Fix a style left on at the end of one run carrying over into the output of the next run in the rich text console.

**Security:**

* <news item>
