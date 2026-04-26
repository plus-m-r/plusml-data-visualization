from __future__ import annotations

from typing import Protocol

from ..models.font_size_policy import FontSizePolicy
from ..models.layout_mode import LayoutMode
from ..models.plot_config import PlotConfig


class FontSizeStrategy(Protocol):
    """Font size strategy interface."""

    def calc_plot_font_size_pt(self, config: PlotConfig, layout_mode: LayoutMode) -> float:
        """Return plotting-time font size in pt for a layout mode."""
