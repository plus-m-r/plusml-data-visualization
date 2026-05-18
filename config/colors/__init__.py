"""Color palette presets for scientific plotting."""

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
    TWO_COLOR,
    TRI_COLOR,
)
from .registry import COLOR_PALETTES, DEFAULT_COLOR_PALETTE_NAME, get_color_palette, normalize_color_palette_name

__all__ = [
    "ABLATION_SINGLE",
    "BLUE_ORANGE_SAFE",
    "BLUE_PURPLE_SAFE",
    "BLUE_YELLOW_SAFE",
    "CLASSIC_ACADEMIC_BLUE",
    "COLOR_PALETTES",
    "DEFAULT_COLOR_PALETTE_NAME",
    "DISTINCT_QUALITATIVE",
    "MACARON",
    "NATURAL_FRIENDLY",
    "NMI_PASTEL",
    "SEMANTIC_NATURE",
    "TWO_COLOR",
    "TRI_COLOR",
    "get_color_palette",
    "normalize_color_palette_name",
]
