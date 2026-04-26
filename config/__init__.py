"""Project-level plotting configuration package."""

from .api import calc_plot_font_size_pt, get_plot_font_size_pt, normalize_layout_mode
from .colors import (
    BLUE_ORANGE_SAFE,
    BLUE_PURPLE_SAFE,
    BLUE_YELLOW_SAFE,
    CLASSIC_ACADEMIC_BLUE,
    COLOR_PALETTES,
    DEFAULT_COLOR_PALETTE_NAME,
    DISTINCT_QUALITATIVE,
    MACARON,
    NATURAL_FRIENDLY,
    TRI_COLOR,
    TWO_COLOR,
    get_color_palette,
    normalize_color_palette_name,
)
from .defaults import DEFAULT_PLOT_CONFIG
from .models import ColorPalette, FontSizePolicy, LayoutMode, PlotConfig
from .strategies import STRATEGY_BY_POLICY

# Backward-compatible constants.
FONT_FAMILY = DEFAULT_PLOT_CONFIG.font_family
OUTPUT_DIR = DEFAULT_PLOT_CONFIG.output_dir
COLOR_PALETTE_NAME = DEFAULT_PLOT_CONFIG.color_palette_name
DEFAULT_COLOR_PALETTE = get_color_palette(COLOR_PALETTE_NAME)

MODE_ONE_PER_ROW = LayoutMode.ONE_PER_ROW.value
MODE_TWO_PER_ROW = LayoutMode.TWO_PER_ROW.value
MODE_THREE_PER_ROW = LayoutMode.THREE_PER_ROW.value

FINAL_PUBLICATION_FONT_PT = DEFAULT_PLOT_CONFIG.final_publication_font_pt
SOURCE_FIGURE_WIDTH_MM = DEFAULT_PLOT_CONFIG.source_figure_width_mm

FINAL_SUBPLOT_WIDTH_MM_BY_MODE = {
    mode.value: width_mm
    for mode, width_mm in DEFAULT_PLOT_CONFIG.final_subplot_width_mm_by_mode.items()
}

PLOT_FONT_SIZE_PT_BY_MODE = {
    mode.value: get_plot_font_size_pt(mode)
    for mode in LayoutMode
}

RECOMMENDED_PLOT_FONT_SIZE_PT_BY_MODE = {
    mode.value: round(get_plot_font_size_pt(mode))
    for mode in LayoutMode
}

# Optional 1x1 full-width values for double-column full-width figures.
MODE_ONE_PER_ROW_FULL_WIDTH_MM = 190.0
MODE_ONE_PER_ROW_FULL_WIDTH_FONT_PT = round(
    calc_plot_font_size_pt(MODE_ONE_PER_ROW_FULL_WIDTH_MM)
)

__all__ = [
    "LayoutMode",
    "ColorPalette",
    "FontSizePolicy",
    "PlotConfig",
    "DEFAULT_PLOT_CONFIG",
    "STRATEGY_BY_POLICY",
    "COLOR_PALETTE_NAME",
    "DEFAULT_COLOR_PALETTE",
    "DEFAULT_COLOR_PALETTE_NAME",
    "COLOR_PALETTES",
    "get_color_palette",
    "normalize_color_palette_name",
    "CLASSIC_ACADEMIC_BLUE",
    "NATURAL_FRIENDLY",
    "DISTINCT_QUALITATIVE",
    "MACARON",
    "BLUE_ORANGE_SAFE",
    "BLUE_YELLOW_SAFE",
    "BLUE_PURPLE_SAFE",
    "TWO_COLOR",
    "TRI_COLOR",
    "normalize_layout_mode",
    "get_plot_font_size_pt",
    "calc_plot_font_size_pt",
    "FONT_FAMILY",
    "OUTPUT_DIR",
    "MODE_ONE_PER_ROW",
    "MODE_TWO_PER_ROW",
    "MODE_THREE_PER_ROW",
    "FINAL_PUBLICATION_FONT_PT",
    "SOURCE_FIGURE_WIDTH_MM",
    "FINAL_SUBPLOT_WIDTH_MM_BY_MODE",
    "PLOT_FONT_SIZE_PT_BY_MODE",
    "RECOMMENDED_PLOT_FONT_SIZE_PT_BY_MODE",
    "MODE_ONE_PER_ROW_FULL_WIDTH_MM",
    "MODE_ONE_PER_ROW_FULL_WIDTH_FONT_PT",
]
