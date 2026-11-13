"""
Parse the ANSI escape codes that programs print to style terminal text.

This module does not use wx, so it can be tested without a display.
"""
import re
from collections import namedtuple

# An escape code is ESC [, then parameters, then intermediates, then one
# final character. The final character is missing when the code is cut
# short.
_ESCAPE_CODE = re.compile(
    r"\x1b(?:\[(?P<params>[0-?]*)(?P<intermediates>[ -/]*)(?P<final>[@-~])?)?"
)

Style = namedtuple(
    "Style", ["bold", "italic", "underline", "foreground", "background"]
)
Style.__doc__ = """The style of a piece of console text.

Attributes
----------
bold : bool
    The flag for bold text.
italic : bool
    The flag for italic text.
underline : bool
    The flag for underlined text.
foreground : tuple of int or None
    The text color as (red, green, blue), or None for the default color.
background : tuple of int or None
    The background color as (red, green, blue), or None for the default
    color.
"""

DEFAULT_STYLE = Style(
    bold=False, italic=False, underline=False, foreground=None, background=None
)


def _build_palette():
    # The 16 named colors, then a 6x6x6 color cube, then 24 shades of grey.
    palette = [
        (0, 0, 0),
        (128, 0, 0),
        (0, 128, 0),
        (128, 128, 0),
        (0, 0, 128),
        (128, 0, 128),
        (0, 128, 128),
        (192, 192, 192),
        (128, 128, 128),
        (255, 0, 0),
        (0, 255, 0),
        (255, 255, 0),
        (0, 0, 255),
        (255, 0, 255),
        (0, 255, 255),
        (255, 255, 255),
    ]
    levels = (0, 95, 135, 175, 215, 255)
    palette.extend((r, g, b) for r in levels for g in levels for b in levels)
    palette.extend((grey, grey, grey) for grey in range(8, 248, 10))
    return tuple(palette)


PALETTE = _build_palette()


class AnsiParser(object):
    """Split program output into pieces of text and their styles.

    The parser remembers the current style between calls to ``feed``, so a
    color that starts in one piece of output carries on into the next.

    Attributes
    ----------
    style : Style
        The style that applies to the text that comes next.
    """

    def __init__(self):
        self.style = DEFAULT_STYLE
        self._pending = ""

    def reset(self):
        """Forget the current style and any unfinished escape code."""
        self.style = DEFAULT_STYLE
        self._pending = ""

    def feed(self, text):
        """Return the text without escape codes, split by style.

        Style codes change the style of the text after them. All other
        escape codes, such as cursor movement, are removed. An escape code
        that is cut off at the end of the text is kept back and finished
        by the next call.

        Parameters
        ----------
        text : str
            The output of the program, which may contain escape codes.

        Returns
        -------
        list of tuple
            The (text, style) pairs in the order they appear, where text is
            a str without escape codes and style is the Style it has.
        """
        text = self._pending + text
        self._pending = ""
        spans = []
        position = 0
        for code in _ESCAPE_CODE.finditer(text):
            if code.group("final") is None:
                if code.end() == len(text):
                    # The rest of this code may arrive in the next call
                    self._add_span(spans, text[position : code.start()])
                    self._pending = code.group()
                    return spans
                if code.group("params") is None:
                    # ESC that does not start an escape code stays as text
                    continue
            self._add_span(spans, text[position : code.start()])
            position = code.end()
            if code.group("final") == "m" and not code.group("intermediates"):
                self._apply_style_code(code.group("params"))
        self._add_span(spans, text[position:])
        return spans

    def _add_span(self, spans, text):
        if not text:
            return
        if spans and spans[-1][1] == self.style:
            spans[-1] = (spans[-1][0] + text, self.style)
        else:
            spans.append((text, self.style))

    def _apply_style_code(self, params):
        try:
            numbers = [int(number or 0) for number in params.split(";")]
        except ValueError:
            # Parameters that are not plain numbers are not supported
            return
        style = self.style
        numbers = iter(numbers)
        for number in numbers:
            if number == 0:
                style = DEFAULT_STYLE
            elif number == 1:
                style = style._replace(bold=True)
            elif number in (21, 22):
                # 22 ends bold. colored 1.x sends 21 for res_bold
                style = style._replace(bold=False)
            elif number == 3:
                style = style._replace(italic=True)
            elif number == 23:
                style = style._replace(italic=False)
            elif number == 4:
                style = style._replace(underline=True)
            elif number == 24:
                style = style._replace(underline=False)
            elif 30 <= number <= 37:
                style = style._replace(foreground=PALETTE[number - 30])
            elif 90 <= number <= 97:
                style = style._replace(foreground=PALETTE[number - 90 + 8])
            elif number == 39:
                style = style._replace(foreground=None)
            elif 40 <= number <= 47:
                style = style._replace(background=PALETTE[number - 40])
            elif 100 <= number <= 107:
                style = style._replace(background=PALETTE[number - 100 + 8])
            elif number == 49:
                style = style._replace(background=None)
            elif number in (38, 48):
                color = self._read_extended_color(numbers)
                if color is None:
                    # The rest of the code cannot be understood
                    break
                if number == 38:
                    style = style._replace(foreground=color)
                else:
                    style = style._replace(background=color)
        self.style = style

    @staticmethod
    def _read_extended_color(numbers):
        # 5;n picks color n of the palette and 2;r;g;b gives the color itself
        mode = next(numbers, None)
        if mode == 5:
            index = next(numbers, None)
            if index is not None and 0 <= index < len(PALETTE):
                return PALETTE[index]
        elif mode == 2:
            rgb = tuple(next(numbers, None) for _ in range(3))
            if all(value is not None and 0 <= value <= 255 for value in rgb):
                return rgb
        return None
