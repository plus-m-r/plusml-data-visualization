from typing import Mapping

from .colors import DEFAULT_COLOR_PALETTE_NAME
from .models import FontSizePolicy, LayoutMode, PlotConfig
from .strategies import FinalWidthDirectStrategy, FixedSourceWidthStrategy, FontSizeStrategy


STRATEGY_BY_POLICY: Mapping[FontSizePolicy, FontSizeStrategy] = {
    FontSizePolicy.FIXED_SOURCE_WIDTH: FixedSourceWidthStrategy(),
    FontSizePolicy.FINAL_WIDTH_DIRECT: FinalWidthDirectStrategy(),
}


DEFAULT_PLOT_CONFIG = PlotConfig(
    font_family="Times New Roman",
    final_publication_font_pt=7.0,
    source_figure_width_mm=190.0,
    output_dir="figures",
    color_palette_name=DEFAULT_COLOR_PALETTE_NAME,
    final_subplot_width_mm_by_mode={
        LayoutMode.ONE_PER_ROW: 90.0,
        LayoutMode.TWO_PER_ROW: 90.0,
        LayoutMode.THREE_PER_ROW: 60.0,
    },
)
