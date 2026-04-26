from __future__ import annotations

import csv
from pathlib import Path
from typing import Sequence

from cycler import cycler
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from config import FontSizePolicy, LayoutMode, PlotConfig, get_color_palette, get_plot_font_size_pt

from .base import LineDrawStrategy

_MM_PER_INCH = 25.4


class LineChartStrategy(LineDrawStrategy):
    """Strategy for drawing a single line chart from a CSV file."""

    def draw_line(
        self,
        *,
        config: PlotConfig,
        layout_mode: LayoutMode,
        source_file: str,
        policy: FontSizePolicy | None = None,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        label: str | None = None,
        save_path: str | None = None,
        dpi: int = 300,
    ) -> tuple[Figure, Axes]:
        mode = layout_mode
        self._apply_style(config, mode, policy)
        path = self.validate_source_file(source_file)
        x_values, y_values = self._read_xy_from_csv(path)

        fig, ax = self._create_figure(config)
        ax.plot(x_values, y_values, label=label)
        if title:
            ax.set_title(title)
        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        if label:
            ax.legend(frameon=False)

        fig.tight_layout()
        output_path = self.resolve_output_path(
            config.output_dir,
            save_path,
            fallback_name=path.stem or "line_chart",
        )
        fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
        return fig, ax

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
    ) -> tuple[Figure, Axes]:
        _ = source_files
        _ = figure_title
        if source_file is None:
            raise ValueError("source_file is required for line charts.")
        return self.draw_line(
            config=config,
            layout_mode=layout_mode,
            source_file=source_file,
            policy=policy,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            label=label,
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
        plt.rcParams.update(
            {
                "font.family": config.font_family,
                "font.size": font_size,
                "axes.titlesize": font_size,
                "axes.labelsize": font_size,
                "xtick.labelsize": font_size,
                "ytick.labelsize": font_size,
                "legend.fontsize": font_size,
                "axes.prop_cycle": cycler(color=palette.colors),
            }
        )

    def _create_figure(self, config: PlotConfig) -> tuple[Figure, Axes]:
        width_inch = config.source_figure_width_mm / _MM_PER_INCH
        height_inch = max(2.4, width_inch * 0.35)
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(width_inch, height_inch))
        return fig, ax

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
