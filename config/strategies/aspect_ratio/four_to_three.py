"""4:3 aspect ratio strategy."""

from __future__ import annotations

from ...models.plot_config import PlotConfig


class FourToThreeStrategy:
    """Standard 4:3 aspect ratio (height = width × 0.75).
    
    Suitable for traditional academic publications and presentations.
    """

    def calc_figure_height_inch(self, config: PlotConfig, width_inch: float, nrows: int = 1) -> float:
        return max(2.4, width_inch * 0.75 * nrows)
