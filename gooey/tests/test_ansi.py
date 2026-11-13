import pytest

from gooey.gui.util.ansi import DEFAULT_STYLE, PALETTE, AnsiParser

RED = (128, 0, 0)
GREEN = (0, 128, 0)
BRIGHT_RED = (255, 0, 0)


def style(**changes):
    return DEFAULT_STYLE._replace(**changes)


# The parser removes escape codes from program output and returns the text
# in pieces, each with the style set by the style codes before it. Each case
# feeds one string to a new parser.
@pytest.mark.parametrize(
    "input_text, expected_spans",
    [
        # C1: Text without escape codes, expect one piece in the default
        # style.
        pytest.param(
            "hello\n", [("hello\n", DEFAULT_STYLE)], id="plain-text"
        ),
        # C2: Bold code then text, expect bold text.
        pytest.param(
            "\x1b[1mhello", [("hello", style(bold=True))], id="bold"
        ),
        # C3: Italic code then text, expect italic text.
        pytest.param(
            "\x1b[3mhello", [("hello", style(italic=True))], id="italic"
        ),
        # C4: Underline code then text, expect underlined text.
        pytest.param(
            "\x1b[4mhello", [("hello", style(underline=True))], id="underline"
        ),
        # C5: One of the 8 basic text colors, as sent by termcolor and
        # colorama, expect red text.
        pytest.param(
            "\x1b[31mhello",
            [("hello", style(foreground=RED))],
            id="basic-foreground",
        ),
        # C6: One of the 8 bright text colors, expect bright red text.
        pytest.param(
            "\x1b[91mhello",
            [("hello", style(foreground=BRIGHT_RED))],
            id="bright-foreground",
        ),
        # C7: Basic and bright background colors, expect each background
        # on the text after its code.
        pytest.param(
            "\x1b[42mhello\x1b[101mworld",
            [
                ("hello", style(background=GREEN)),
                ("world", style(background=BRIGHT_RED)),
            ],
            id="basic-and-bright-background",
        ),
        # C8: Text color picked from the 256 color palette, as sent by
        # colored, expect green text.
        pytest.param(
            "\x1b[38;5;2mhello",
            [("hello", style(foreground=GREEN))],
            id="palette-foreground",
        ),
        # C9: Background color picked from the 256 color palette, expect a
        # green background.
        pytest.param(
            "\x1b[48;5;2mhello",
            [("hello", style(background=GREEN))],
            id="palette-background",
        ),
        # C10: Text and background colors given as red, green and blue
        # values, expect exactly those colors.
        pytest.param(
            "\x1b[38;2;1;2;3;48;2;4;5;6mhello",
            [("hello", style(foreground=(1, 2, 3), background=(4, 5, 6)))],
            id="rgb-colors",
        ),
        # C11: Several styles in one code, as sent by rich, expect all of
        # them on the text.
        pytest.param(
            "\x1b[1;4;31mhello",
            [("hello", style(bold=True, underline=True, foreground=RED))],
            id="combined-code",
        ),
        # C12: Styles in separate codes one after another, as sent by
        # colored, expect all of them on the text.
        pytest.param(
            "\x1b[38;5;1m\x1b[1mhello",
            [("hello", style(bold=True, foreground=RED))],
            id="consecutive-codes",
        ),
        # C13: Reset code between two words, expect the style on the first
        # word only.
        pytest.param(
            "\x1b[1mhello\x1b[0m world",
            [("hello", style(bold=True)), (" world", DEFAULT_STYLE)],
            id="reset",
        ),
        # C14: Reset code without a number, expect the same as reset.
        pytest.param(
            "\x1b[1mhello\x1b[m world",
            [("hello", style(bold=True)), (" world", DEFAULT_STYLE)],
            id="reset-without-number",
        ),
        # C15: Codes that end bold (22, and 21 from colored 1.x), italic
        # and underline, expect each to end only its own style.
        pytest.param(
            "\x1b[1;3;4ma\x1b[22mb\x1b[1;23mc\x1b[21;24md",
            [
                ("a", style(bold=True, italic=True, underline=True)),
                ("b", style(italic=True, underline=True)),
                ("c", style(bold=True, underline=True)),
                ("d", DEFAULT_STYLE),
            ],
            id="end-single-styles",
        ),
        # C16: Codes for the default text and background colors, expect
        # the colors removed and the bold kept.
        pytest.param(
            "\x1b[1;31;42ma\x1b[39mb\x1b[49mc",
            [
                ("a", style(bold=True, foreground=RED, background=GREEN)),
                ("b", style(bold=True, background=GREEN)),
                ("c", style(bold=True)),
            ],
            id="default-colors",
        ),
        # C17: Cursor and line codes around text, as sent by progress
        # bars, expect the codes removed and the text in one piece.
        pytest.param(
            "\x1b[2K\x1b[?25lhello \x1b[1Aworld\x1b[?25h\n",
            [("hello world\n", DEFAULT_STYLE)],
            id="non-style-codes-removed",
        ),
        # C18: A cursor code between a style code and its text, expect the
        # style is kept.
        pytest.param(
            "\x1b[31m\x1b[2Khello",
            [("hello", style(foreground=RED))],
            id="style-kept-after-non-style-code",
        ),
        # C19: A style number that is not supported next to one that is,
        # expect the supported one applied.
        pytest.param(
            "\x1b[5;1mhello",
            [("hello", style(bold=True))],
            id="unsupported-number-skipped",
        ),
        # C20: A palette color outside 0 to 255, expect the style
        # unchanged.
        pytest.param(
            "\x1b[38;5;256mhello",
            [("hello", DEFAULT_STYLE)],
            id="palette-color-out-of-range",
        ),
        # C21: A color code with its values missing, expect the style
        # unchanged.
        pytest.param(
            "\x1b[38mhello", [("hello", DEFAULT_STYLE)], id="color-cut-short"
        ),
        # C22: A code that stops in the middle of the text, expect the
        # unfinished code removed and the text kept.
        pytest.param(
            "hello\x1b[\n",
            [("hello\n", DEFAULT_STYLE)],
            id="unfinished-code-inside-text",
        ),
        # C23: Only escape codes, expect no text.
        pytest.param("\x1b[1m\x1b[0m", [], id="codes-only"),
        # C24: Empty string, expect no text.
        pytest.param("", [], id="empty"),
    ],
)
def test_feed(input_text, expected_spans):
    actual_spans = AnsiParser().feed(input_text)
    assert actual_spans == expected_spans


# The parser keeps its state between calls to feed, because Gooey passes
# on the output of the program piece by piece. Each case feeds several
# strings to one parser and collects the results of every call.
@pytest.mark.parametrize(
    "input_texts, expected_spans_per_call",
    [
        # C1: A style set in one call with no reset, expect it on the text
        # of the next call.
        pytest.param(
            ["\x1b[1mhello\n", "world\n"],
            [[("hello\n", style(bold=True))], [("world\n", style(bold=True))]],
            id="style-carries-over",
        ),
        # C2: A style code cut in two between calls, expect no stray
        # characters and the style on the text after the code.
        pytest.param(
            ["hello\x1b[38;5", ";2mworld"],
            [[("hello", DEFAULT_STYLE)], [("world", style(foreground=GREEN))]],
            id="code-split-between-calls",
        ),
        # C3: A call that ends right after the escape character, expect
        # the code finished by the next call.
        pytest.param(
            ["hello\x1b", "[1mworld"],
            [[("hello", DEFAULT_STYLE)], [("world", style(bold=True))]],
            id="escape-character-split-between-calls",
        ),
    ],
)
def test_feed_keeps_state_between_calls(input_texts, expected_spans_per_call):
    parser = AnsiParser()
    actual_spans_per_call = [parser.feed(text) for text in input_texts]
    assert actual_spans_per_call == expected_spans_per_call


def test_reset():
    # After reset the parser forgets the style and the unfinished code, so
    # the next text is in the default style with no stray characters.
    parser = AnsiParser()
    parser.feed("\x1b[1mhello\x1b[38;5")
    parser.reset()
    actual_spans = parser.feed("world")
    expected_spans = [("world", DEFAULT_STYLE)]
    assert actual_spans == expected_spans


# The palette follows the xterm 256 color table: 16 named colors, a color
# cube, then shades of grey.
@pytest.mark.parametrize(
    "input_index, expected_color",
    [
        # C1: First named color, expect black.
        pytest.param(0, (0, 0, 0), id="first-named-color"),
        # C2: Last named color, expect white.
        pytest.param(15, (255, 255, 255), id="last-named-color"),
        # C3: First step of blue in the color cube, expect #00005f.
        pytest.param(17, (0, 0, 95), id="color-cube-blue-step"),
        # C4: A color inside the cube, expect #d78700.
        pytest.param(172, (215, 135, 0), id="color-cube-inside"),
        # C5: Last color of the cube, expect white.
        pytest.param(231, (255, 255, 255), id="color-cube-last"),
        # C6: First shade of grey, expect #080808.
        pytest.param(232, (8, 8, 8), id="first-grey"),
        # C7: Last shade of grey, expect #eeeeee.
        pytest.param(255, (238, 238, 238), id="last-grey"),
    ],
)
def test_palette(input_index, expected_color):
    actual_color = PALETTE[input_index]
    assert actual_color == expected_color


def test_palette_length():
    assert len(PALETTE) == 256
