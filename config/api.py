from .defaults import DEFAULT_PLOT_CONFIG, STRATEGY_BY_POLICY
from .models import FontSizePolicy, LayoutMode, PlotConfig


def normalize_layout_mode(layout_mode: LayoutMode | str) -> LayoutMode:
    """Convert user input to a validated LayoutMode."""
    if isinstance(layout_mode, LayoutMode):
        return layout_mode
    try:
        return LayoutMode(layout_mode)
    except ValueError as exc:
        valid = ", ".join(mode.value for mode in LayoutMode)
        raise ValueError(f"Invalid layout mode: {layout_mode}. Expected one of: {valid}") from exc


def get_plot_font_size_pt(
    layout_mode: LayoutMode | str,
    *,
    config: PlotConfig = DEFAULT_PLOT_CONFIG,
    policy: FontSizePolicy | None = None,
    rounded: bool = False,
) -> float:
    """Get plotting-time font size in pt for a layout mode and policy."""
    mode = normalize_layout_mode(layout_mode)
    selected_policy = policy or config.default_font_size_policy
    strategy = STRATEGY_BY_POLICY[selected_policy]
    size_pt = strategy.calc_plot_font_size_pt(config, mode)
    return float(round(size_pt)) if rounded else size_pt


def calc_plot_font_size_pt(final_subplot_width_mm: float) -> float:
    """Legacy helper: fixed-source-width formula using default config."""
    if final_subplot_width_mm <= 0:
        raise ValueError("Final subplot width must be > 0 mm.")
    return (
        DEFAULT_PLOT_CONFIG.final_publication_font_pt
        * DEFAULT_PLOT_CONFIG.source_figure_width_mm
        / final_subplot_width_mm
    )
