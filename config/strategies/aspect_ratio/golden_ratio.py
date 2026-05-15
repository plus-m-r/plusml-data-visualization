"""Golden ratio aspect ratio strategy."""

from __future__ import annotations

from ...models.plot_config import PlotConfig


class GoldenRatioStrategy:
    """Golden ratio aspect ratio (~1.618:1, height = width / 1.618).
    
    Aesthetically pleasing ratio often used in design and art.
    """

    def calc_figure_height_inch(self, config: PlotConfig, width_inch: float, nrows: int = 1) -> float:
        return max(2.4, width_inch / 1.618 * nrows)
