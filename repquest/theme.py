"""Colors and sizes shared by every screen. Based on the dark palette of the original RepQuest app."""

from __future__ import annotations


def _rgba(hex_color: str, alpha: float = 1.0) -> tuple[float, float, float, float]:
    value = hex_color.lstrip("#")
    red, green, blue = (int(value[i : i + 2], 16) / 255 for i in (0, 2, 4))
    return (red, green, blue, alpha)


BACKGROUND = _rgba("#0D1117")
SURFACE = _rgba("#161B22")
SURFACE_VARIANT = _rgba("#21262D")
DIVIDER = _rgba("#30363D")
TEXT_PRIMARY = _rgba("#F0F6FC")
TEXT_BODY = _rgba("#C9D1D9")
TEXT_SECONDARY = _rgba("#8B949E")
PRIMARY = _rgba("#1F6FEB")
PRIMARY_LIGHT = _rgba("#58A6FF")
PROGRESSION = _rgba("#A371F7")
SUCCESS = _rgba("#3FB950")
WARNING = _rgba("#D29922")

PRIMARY_HEX = "58A6FF"
SECONDARY_HEX = "8B949E"
