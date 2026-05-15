"""Square aspect ratio strategy."""

from __future__ import annotations

from ...models.plot_config import PlotConfig


class SquareStrategy:
    """Square aspect ratio (1:1, height = width).
    
    Suitable for symmetric visualizations and grid layouts.
    """

    def calc_figure_height_inch(self, config: PlotConfig, width_inch: float, nrows: int = 1) -> float:
        return max(2.4, width_inch * nrows)
