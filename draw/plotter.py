from __future__ import annotations

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from config import DEFAULT_PLOT_CONFIG, FontSizePolicy, LayoutMode, PlotConfig, normalize_layout_mode

from .strategies import ChartType, DrawStrategy, STRATEGY_BY_CHART_TYPE


class MatplotlibDrawer:
    """Matplotlib drawing context that delegates to chart strategies."""

    def __init__(
        self,
        *,
        config: PlotConfig = DEFAULT_PLOT_CONFIG,
        policy: FontSizePolicy | None = None,
        dpi: int = 300,
    ) -> None:
        self.config = config
        self.policy = policy
        self.dpi = dpi

    def _get_strategy(self, chart_type: ChartType) -> DrawStrategy:
        return STRATEGY_BY_CHART_TYPE[chart_type]

    def draw_line(
        self,
        *,
        source_file: str,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        label: str | None = None,
        layout_mode: LayoutMode | str = LayoutMode.ONE_PER_ROW,
        save_path: str | None = None,
    ) -> tuple[Figure, Axes]:
        """Draw a line chart from a CSV source file."""
        mode = normalize_layout_mode(layout_mode)
        strategy = self._get_strategy(ChartType.LINE)
        fig, ax = strategy.draw(
            config=self.config,
            layout_mode=mode,
            policy=self.policy,
            source_file=source_file,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            label=label,
            save_path=save_path,
            dpi=self.dpi,
        )
        return fig, ax

    def draw_grid(
        self,
        source_files: list[str],
        *,
        layout_mode: LayoutMode | str = LayoutMode.TWO_PER_ROW,
        figure_title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        save_path: str | None = None,
    ) -> tuple[Figure, list[Axes]]:
        """Draw a grid chart from CSV source files."""
        mode = normalize_layout_mode(layout_mode)
        strategy = self._get_strategy(ChartType.GRID)
        fig, axes = strategy.draw(
            config=self.config,
            layout_mode=mode,
            policy=self.policy,
            source_files=source_files,
            figure_title=figure_title,
            xlabel=xlabel,
            ylabel=ylabel,
            save_path=save_path,
            dpi=self.dpi,
        )
        return fig, axes


def draw_line_chart(
    *,
    source_file: str,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    label: str | None = None,
    layout_mode: LayoutMode | str = LayoutMode.ONE_PER_ROW,
    save_path: str | None = None,
    config: PlotConfig = DEFAULT_PLOT_CONFIG,
    policy: FontSizePolicy | None = None,
    dpi: int = 300,
) -> tuple[Figure, Axes]:
    drawer = MatplotlibDrawer(config=config, policy=policy, dpi=dpi)
    return drawer.draw_line(
        source_file=source_file,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        label=label,
        layout_mode=layout_mode,
        save_path=save_path,
    )


def draw_grid_chart(
    source_files: list[str],
    *,
    layout_mode: LayoutMode | str = LayoutMode.TWO_PER_ROW,
    figure_title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    save_path: str | None = None,
    config: PlotConfig = DEFAULT_PLOT_CONFIG,
    policy: FontSizePolicy | None = None,
    dpi: int = 300,
) -> tuple[Figure, list[Axes]]:
    drawer = MatplotlibDrawer(config=config, policy=policy, dpi=dpi)
    return drawer.draw_grid(
        source_files,
        layout_mode=layout_mode,
        figure_title=figure_title,
        xlabel=xlabel,
        ylabel=ylabel,
        save_path=save_path,
    )
