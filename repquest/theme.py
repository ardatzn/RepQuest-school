"""Colors, type styles and the font shared by every screen.

The values follow the original RepQuest Android app (``ui/theme/Color.kt``, ``Type.kt`` and ``Shape.kt``): a dark
palette, monospace text and sharp 0dp corners.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


def _rgba(hex_color: str, alpha: float = 1.0) -> tuple[float, float, float, float]:
    value = hex_color.lstrip("#")
    red, green, blue = (int(value[i : i + 2], 16) / 255 for i in (0, 2, 4))
    return (red, green, blue, alpha)


BACKGROUND = _rgba("#0D1117")
SURFACE = _rgba("#161B22")
SURFACE_VARIANT = _rgba("#21262D")  # Avatar slot, selected tab, pressed rows
DIVIDER = _rgba("#30363D")  # Card borders and dividers
OUTLINE = _rgba("#8B949E")  # XP bar outline
TEXT_PRIMARY = _rgba("#F0F6FC")
TEXT_BODY = _rgba("#C9D1D9")
TEXT_SECONDARY = _rgba("#8B949E")
PRIMARY = _rgba("#1F6FEB")  # Primary button fill
PRIMARY_LIGHT = _rgba("#58A6FF")  # Primary button border, secondary actions, selected-tab indicator
PRIMARY_PRESSED = _rgba("#1A5FCC")
PROGRESSION = _rgba("#A371F7")  # Game level and XP only
SUCCESS = _rgba("#3FB950")
WARNING = _rgba("#D29922")

PRIMARY_HEX = "58A6FF"
SECONDARY_HEX = "8B949E"


@dataclass(frozen=True)
class TextStyle:
    """A text style in sp: font size, line height and whether the text is bold."""

    size: float
    line_height: float
    bold: bool = False


# The type scale of the original app. SemiBold and Bold both render bold, as they do with the Android monospace font.
WORDMARK = TextStyle(24, 32, bold=True)
HEADLINE = TextStyle(24, 32, bold=True)
TITLE = TextStyle(20, 28, bold=True)
BODY = TextStyle(16, 24)
BUTTON = TextStyle(16, 24, bold=True)
LABEL = TextStyle(14, 20)
CAPTION = TextStyle(12, 16)

WORDMARK_LETTER_SPACING = 4  # sp

# Android 14 and newer scale large text less than small text when the phone's font size is above 100%. These are the
# platform's conversion points (sp to dp) for each font scale; Kivy alone would scale every size linearly.
_FROM_SP = (8, 10, 12, 14, 18, 20, 24, 30, 100)
_TO_DP = {
    1.0: _FROM_SP,
    1.15: (9.2, 11.5, 13.8, 16.4, 19.8, 21.8, 25.2, 30, 100),
    1.3: (10.4, 13, 15.6, 18.8, 21.6, 23.6, 26.4, 30, 100),
    1.5: (12, 15, 18, 22, 24, 26, 28, 30, 100),
    1.8: (14.4, 18, 21.6, 24.4, 27.6, 30.8, 32.8, 34.8, 100),
    2.0: (16, 20, 24, 26, 30, 34, 36, 38, 100),
}
_MIN_NON_LINEAR_SCALE = 1.03


def _lerp(x: float, xs, ys) -> float:
    if x <= xs[0]:
        return x * ys[0] / xs[0]
    for (x0, x1), (y0, y1) in zip(zip(xs, xs[1:]), zip(ys, ys[1:])):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return x * ys[-1] / xs[-1]


def sp_to_dp(value: float, font_scale: float) -> float:
    """Converts ``value`` sp to dp at ``font_scale`` the way Android 14+ does."""
    if font_scale < _MIN_NON_LINEAR_SCALE:
        return value * font_scale
    scales = sorted(_TO_DP)
    if font_scale >= scales[-1]:
        return _lerp(value, _FROM_SP, _TO_DP[scales[-1]]) * font_scale / scales[-1]
    low = max(scale for scale in scales if scale <= font_scale)
    high = min(scale for scale in scales if scale > font_scale)
    at_low, at_high = _lerp(value, _FROM_SP, _TO_DP[low]), _lerp(value, _FROM_SP, _TO_DP[high])
    return at_low + (at_high - at_low) * (font_scale - low) / (high - low)


def font_px(value: float) -> float:
    """``value`` sp in pixels for the current screen density and font scale."""
    from kivy.metrics import Metrics, dp

    return dp(sp_to_dp(value, Metrics.fontscale))

FONT_NAME = "RepQuestMono"

# The original app uses Android's monospace font, which is Droid Sans Mono. The APK uses the phone's own copy.
# Droid Sans Mono has no bold file, so bold text is drawn with a thin outline, the way Android fakes bold.
# On a computer the first monospace font found is used; the layout is the same, only the glyphs may differ.
_FONT_CANDIDATES = (
    ("/system/fonts/DroidSansMono.ttf", None),
    ("/usr/share/fonts/truetype/droid/DroidSansMono.ttf", None),
    ("/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf", "/usr/share/fonts/truetype/noto/NotoSansMono-Bold.ttf"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"),
    ("/System/Library/Fonts/Supplemental/Courier New.ttf", "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"),
    ("C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/consolab.ttf"),
)

# True when the registered font has no bold file and bold text needs the outline.
fake_bold = False


def register_font() -> str | None:
    """Registers ``FONT_NAME`` with Kivy and returns the regular font file, or None for Kivy's default font."""
    global fake_bold
    from kivy.core.text import LabelBase

    for regular, bold in _FONT_CANDIDATES:
        if os.path.isfile(regular):
            has_bold = bold is not None and os.path.isfile(bold)
            LabelBase.register(FONT_NAME, regular, fn_bold=bold if has_bold else None)
            fake_bold = not has_bold
            return regular
    LabelBase.register(FONT_NAME, "Roboto-Regular.ttf", fn_bold="Roboto-Bold.ttf")
    fake_bold = False
    return None
