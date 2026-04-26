from __future__ import annotations

from ..models.layout_mode import LayoutMode
from ..models.plot_config import PlotConfig


class FixedSourceWidthStrategy:
    """Scale font size by source width / final width."""

    def calc_plot_font_size_pt(self, config: PlotConfig, layout_mode: LayoutMode) -> float:
        final_width_mm = config.final_subplot_width_mm_by_mode[layout_mode]
        if final_width_mm <= 0:
            raise ValueError("Final subplot width must be > 0 mm.")
        return config.final_publication_font_pt * config.source_figure_width_mm / final_width_mm
