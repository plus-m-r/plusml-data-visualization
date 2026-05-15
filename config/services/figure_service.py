"""Figure dimension services."""

from __future__ import annotations

from ..factories import get_aspect_ratio_strategy
from ..models import AspectRatioPolicy, PlotConfig
from ..presets import DEFAULT_PLOT_CONFIG


def get_figure_height_inch(
    config: PlotConfig = DEFAULT_PLOT_CONFIG,
    width_inch: float = 0.0,
    nrows: int = 1,
    policy: AspectRatioPolicy | None = None,
) -> float:
    """Get figure height in inches based on aspect ratio policy.
    
    Args:
        config: Plot configuration (uses default if not provided).
        width_inch: Figure width in inches.
        nrows: Number of rows (for grid charts).
        policy: Aspect ratio policy (uses default from config if None).
    
    Returns:
        Figure height in inches.
    """
    selected_policy = policy or config.default_aspect_ratio_policy
    strategy = get_aspect_ratio_strategy(selected_policy)
    return strategy.calc_figure_height_inch(config, width_inch, nrows)
