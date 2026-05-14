from __future__ import annotations

import csv
from math import ceil
from pathlib import Path
from typing import Sequence

from cycler import cycler
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from config import FontSizePolicy, LayoutMode, PlotConfig, get_color_palette, get_plot_font_size_pt

from .base import GridDrawStrategy
from ..font_utils import configure_matplotlib_for_chinese

_MM_PER_INCH = 25.4


class GridChartStrategy(GridDrawStrategy):
    """Strategy for drawing a one-row grid chart from CSV files."""

    def draw_grid(
        self,
        *,
        config: PlotConfig,
        layout_mode: LayoutMode,
        source_files: Sequence[str],
        policy: FontSizePolicy | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        figure_title: str | None = None,
        save_path: str | None = None,
        dpi: int = 300,
    ) -> tuple[Figure, list[Axes]]:
        if len(source_files) == 0:
            raise ValueError("source_files is required for grid charts.")

        max_subplots = self._layout_columns(layout_mode)
        if len(source_files) > max_subplots:
            raise ValueError(
                f"Layout mode {layout_mode.value} supports up to {max_subplots} subplots, "
                f"but received {len(source_files)} files."
            )

        self._apply_style(config, layout_mode, policy)
        fig, axes = self._create_figure(config, layout_mode, n_subplots=len(source_files))

        for index, (ax, source_file) in enumerate(zip(axes, source_files), start=1):
            path = self.validate_source_file(source_file)
            x_values, y_values = self._read_xy_from_csv(path)
            ax.plot(x_values, y_values, "-")
            ax.set_title(path.stem or f"Series {index}")
            if xlabel:
                ax.set_xlabel(xlabel)
            if ylabel:
                ax.set_ylabel(ylabel)

        if figure_title:
            fig.suptitle(figure_title)
        fig.tight_layout()
        fallback_name = "_".join(Path(source_file).stem for source_file in source_files) or "grid_chart"
        output_path = self.resolve_output_path(
            config.output_dir,
            save_path,
            fallback_name=fallback_name,
        )
        fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
        return fig, axes

    # Backward-compatible entrypoint for older internal calls.
    def draw(
        self,
        *,
        config: PlotConfig,
        layout_mode: LayoutMode,
        policy: FontSizePolicy | None = None,
        source_file: str | None = None,
        source_files: Sequence[str] | None = None,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        label: str | None = None,
        figure_title: str | None = None,
        save_path: str | None = None,
        dpi: int = 300,
    ) -> tuple[Figure, list[Axes]]:
        _ = source_file
        _ = title
        _ = label
        if source_files is None:
            raise ValueError("source_files is required for grid charts.")
        return self.draw_grid(
            config=config,
            layout_mode=layout_mode,
            source_files=source_files,
            policy=policy,
            xlabel=xlabel,
            ylabel=ylabel,
            figure_title=figure_title,
            save_path=save_path,
            dpi=dpi,
        )

    def _apply_style(self, config: PlotConfig, layout_mode: LayoutMode, policy: FontSizePolicy | None) -> None:
        palette = get_color_palette(config.color_palette_name)
        font_size = get_plot_font_size_pt(
            layout_mode,
            config=config,
            policy=policy,
            rounded=True,
        )
        
        # 自动配置中文字体支持
        actual_font = configure_matplotlib_for_chinese(config.font_family)
        
        plt.rcParams.update(
            {
                "font.family": actual_font,
                "font.size": font_size,
                "axes.titlesize": font_size,
                "axes.labelsize": font_size,
                "xtick.labelsize": font_size,
                "ytick.labelsize": font_size,
                "legend.fontsize": font_size,
                "axes.prop_cycle": cycler(color=palette.colors),
            }
        )

    def _create_figure(
        self,
        config: PlotConfig,
        layout_mode: LayoutMode,
        *,
        n_subplots: int,
    ) -> tuple[Figure, list[Axes]]:
        ncols = self._layout_columns(layout_mode)
        nrows = ceil(n_subplots / ncols)
        width_inch = config.source_figure_width_mm / _MM_PER_INCH
        height_inch = max(2.4, width_inch * 0.35 * nrows)

        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(width_inch, height_inch))
        if nrows == 1 and ncols == 1:
            return fig, [axes]

        axes_list: list[Axes] = list(axes.flat)
        for ax in axes_list[n_subplots:]:
            ax.set_visible(False)
        return fig, axes_list[:n_subplots]

    @staticmethod
    def _layout_columns(layout_mode: LayoutMode) -> int:
        return int(layout_mode.value.split("x", maxsplit=1)[1])

    @staticmethod
    def _read_xy_from_csv(path: Path) -> tuple[list[float], list[float]]:
        rows: list[list[str]] = []
        with path.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row:
                    rows.append(row)

        numeric_rows: list[list[float]] = []
        for row in rows:
            try:
                numeric_rows.append([float(value) for value in row])
            except ValueError:
                continue

        if not numeric_rows:
            raise ValueError(f"No numeric data found in CSV file: {path}")

        if len(numeric_rows[0]) == 1:
            y_values = [row[0] for row in numeric_rows]
            x_values = list(range(len(y_values)))
            return x_values, y_values

        x_values = [row[0] for row in numeric_rows]
        y_values = [row[1] for row in numeric_rows]
        return x_values, y_values
