from __future__ import annotations

import csv
from pathlib import Path
from typing import Sequence

from cycler import cycler
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from config import (
    AspectRatioPolicy,
    FontSizePolicy,
    LayoutMode,
    PlotConfig,
    get_color_palette,
    get_figure_height_inch,
    get_plot_font_size_pt,
    MARKERS,
    DEFAULT_MARKER_SIZE,
)

from .base import DrawStrategy, auto_detect_chinese_font, set_title_below, resolve_fallback_name

_MM_PER_INCH = 25.4


class ScatterChartStrategy(DrawStrategy):
    """Strategy for drawing scatter charts with one or more data series."""

    def draw_scatter(
        self,
        *,
        config: PlotConfig,
        layout_mode: LayoutMode,
        source_files: Sequence[str],
        labels: Sequence[str | None] | None = None,
        policy: FontSizePolicy | None = None,
        aspect_ratio_policy: AspectRatioPolicy | None = None,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        save_path: str | None = None,
        dpi: int = 600,
    ) -> tuple[Figure, Axes]:
        mode = layout_mode
        self._apply_style(config, mode, policy)
        
        if not source_files:
            raise ValueError("source_files cannot be empty")
        
        # Validate all source files
        paths = [self.validate_source_file(sf) for sf in source_files]
        
        # Read all data series
        data_series = []
        for path in paths:
            x_values, y_values = self._read_xy_from_csv(path)
            data_series.append((x_values, y_values, path))
        
        # Create figure
        fig, ax = self._create_figure(config, aspect_ratio_policy)
        
        # Plot all series with color-blind friendly styles
        has_labels = False
        palette = get_color_palette(config.color_palette_name)
        
        n_colors = len(palette.colors)
        n_markers = len(MARKERS)
        
        for i, (x_values, y_values, path) in enumerate(data_series):
            label = labels[i] if labels and i < len(labels) else None
            
            # Distribute color and marker independently for maximum differentiation
            color = palette.colors[i % n_colors]
            marker = MARKERS[i % n_markers]
            
            ax.scatter(
                x_values, 
                y_values, 
                label=label,
                color=color,
                marker=marker,
                s=DEFAULT_MARKER_SIZE * 10,  # Size parameter for scatter plot
            )
            if label:
                has_labels = True
        
        # Set labels and title
        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        if has_labels:
            ax.legend(frameon=False)
        if title:
            set_title_below(ax, title)

        fig.tight_layout()
        
        # Use title as filename, or fallback to first file's name
        fallback_name = resolve_fallback_name(title, paths, "scatter_chart")
        output_path = self.resolve_output_path(
            config.output_dir,
            save_path,
            fallback_name=fallback_name,
        )
        fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
        return fig, ax

    def _apply_style(self, config: PlotConfig, layout_mode: LayoutMode, policy: FontSizePolicy | None) -> None:
        palette = get_color_palette(config.color_palette_name)
        font_size = get_plot_font_size_pt(
            layout_mode,
            config=config,
            policy=policy,
            rounded=True,
        )
        
        # Auto-configure Chinese font support
        actual_font = auto_detect_chinese_font(config.font_family)
        
        plt.rcParams.update(
            {
                "font.family": actual_font,
                "font.sans-serif": [actual_font, "Arial", "Helvetica", "DejaVu Sans"],
                "font.size": font_size,
                "axes.titlesize": font_size,
                "axes.labelsize": font_size,
                "xtick.labelsize": font_size,
                "ytick.labelsize": font_size,
                "legend.fontsize": font_size,
                "axes.unicode_minus": False,  # 解决负号显示问题
                # Nature style: minimalist axes
                "axes.spines.right": False,
                "axes.spines.top": False,
                "axes.linewidth": 0.8,
                "legend.frameon": False,
                "svg.fonttype": "none",  # Editable text in SVG
                "pdf.fonttype": 42,      # Embed TrueType in PDF
            }
        )

    def _create_figure(self, config: PlotConfig, aspect_ratio_policy: AspectRatioPolicy | None = None) -> tuple[Figure, Axes]:
        width_inch = config.source_figure_width_mm / _MM_PER_INCH
        height_inch = get_figure_height_inch(config, width_inch, nrows=1, policy=aspect_ratio_policy)
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