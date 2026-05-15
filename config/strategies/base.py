"""Base strategy interfaces using Protocol pattern."""

from __future__ import annotations

from typing import Protocol


class FontSizeStrategy(Protocol):
    """Font size calculation strategy interface."""

    def calc_plot_font_size_pt(self, config: 'PlotConfig', layout_mode: 'LayoutMode') -> float:
        """Return plotting-time font size in pt for a layout mode."""
        ...


class AspectRatioStrategy(Protocol):
    """Aspect ratio calculation strategy interface."""

    def calc_figure_height_inch(self, config: 'PlotConfig', width_inch: float, nrows: int = 1) -> float:
        """Return figure height in inches based on width and aspect ratio policy."""
        ...
