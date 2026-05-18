"""Preset configurations."""

from ..colors import DEFAULT_COLOR_PALETTE_NAME
from ..models import AspectRatioPolicy, FontSizePolicy, LayoutMode, PlotConfig


DEFAULT_PLOT_CONFIG = PlotConfig(
    font_family="Times New Roman",
    final_publication_font_pt=7.0,
    source_figure_width_mm=190.0,
    output_dir="figures",
    color_palette_name=DEFAULT_COLOR_PALETTE_NAME,
    default_font_size_policy=FontSizePolicy.FIXED_SOURCE_WIDTH,
    default_aspect_ratio_policy=AspectRatioPolicy.FOUR_TO_THREE,
    final_subplot_width_mm_by_mode={
        LayoutMode.ONE_PER_ROW: 90.0,
        LayoutMode.TWO_PER_ROW: 90.0,
        LayoutMode.THREE_PER_ROW: 60.0,
    },
)
 