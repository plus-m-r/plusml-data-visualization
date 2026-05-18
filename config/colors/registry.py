from __future__ import annotations

from typing import Mapping

from ..models import ColorPalette
from .presets import (
    ABLATION_SINGLE,
    BLUE_ORANGE_SAFE,
    BLUE_PURPLE_SAFE,
    BLUE_YELLOW_SAFE,
    CLASSIC_ACADEMIC_BLUE,
    DISTINCT_QUALITATIVE,
    MACARON,
    NATURAL_FRIENDLY,
    NMI_PASTEL,
    SEMANTIC_NATURE,
    TRI_COLOR,
    TWO_COLOR,
)

DEFAULT_COLOR_PALETTE_NAME = CLASSIC_ACADEMIC_BLUE.name

COLOR_PALETTES: Mapping[str, ColorPalette] = {
    palette.name: palette
    for palette in (
        CLASSIC_ACADEMIC_BLUE,
        NATURAL_FRIENDLY,
        DISTINCT_QUALITATIVE,
        MACARON,
        BLUE_ORANGE_SAFE,
        BLUE_YELLOW_SAFE,
        BLUE_PURPLE_SAFE,
        TWO_COLOR,
        TRI_COLOR,
        # Nature-Figure semantic palettes (Phase 1)
        SEMANTIC_NATURE,
        NMI_PASTEL,
        ABLATION_SINGLE,
    )
}


def normalize_color_palette_name(name: str) -> str:
    """Normalize a palette name for lookup."""
    return name.strip().lower().replace(" ", "_")


def get_color_palette(name: str) -> ColorPalette:
    """Return a named color palette or raise a clear error."""
    normalized = normalize_color_palette_name(name)
    try:
        return COLOR_PALETTES[normalized]
    except KeyError as exc:
        valid = ", ".join(sorted(COLOR_PALETTES))
        raise ValueError(f"Unknown color palette: {name}. Available palettes: {valid}") from exc
