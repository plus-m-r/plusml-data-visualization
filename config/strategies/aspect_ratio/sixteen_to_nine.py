"""16:9 aspect ratio strategy."""

from __future__ import annotations

from ...models.plot_config import PlotConfig


class SixteenToNineStrategy:
    """Widescreen 16:9 aspect ratio (height = width × 0.5625).
    
    Suitable for modern presentations and digital displays.
    """

    def calc_figure_height_inch(self, config: PlotConfig, width_inch: float, nrows: int = 1) -> float:
        return max(2.4, width_inch * 0.5625 * nrows)
