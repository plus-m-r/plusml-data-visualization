from __future__ import annotations

import csv
from pathlib import Path
from typing import Sequence

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import numpy as np

from config import (
    AspectRatioPolicy,
    FontSizePolicy,
    LayoutMode,
    PlotConfig,
    get_color_palette,
    get_figure_height_inch,
    get_plot_font_size_pt,
)

from .base import DrawStrategy, auto_detect_chinese_font, set_title_below, resolve_fallback_name

_MM_PER_INCH = 25.4


class HeatmapDrawStrategy(DrawStrategy):
    """Strategy for drawing heatmaps from CSV data."""

    def draw_heatmap(
        self,
        *,
        config: PlotConfig,
        layout_mode: LayoutMode,
        source_file: str,
        policy: FontSizePolicy | None = None,
        aspect_ratio_policy: AspectRatioPolicy | None = None,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        save_path: str | None = None,
        dpi: int = 600,
        cmap: str = "viridis",
        show_values: bool = False,
        value_format: str = ".2f",
    ) -> tuple[Figure, Axes]:
        """Draw a heatmap from a CSV file containing matrix data.
        
        Args:
            config: Plot configuration
            layout_mode: Layout mode for the plot
            source_file: Path to CSV file with matrix data
            policy: Font size policy
            aspect_ratio_policy: Aspect ratio policy
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            save_path: Output file path
            dpi: Resolution for saved image
            cmap: Colormap name (matplotlib colormap)
            show_values: Whether to show values in cells
            value_format: Format string for cell values
            
        Returns:
            Tuple of (Figure, Axes)
        """
        mode = layout_mode
        self._apply_style(config, mode, policy)
        
        # Validate source file
        path = self.validate_source_file(source_file)
        
        # Read matrix data from CSV
        matrix_data, row_labels, col_labels = self._read_matrix_from_csv(path)
        
        # Create figure with square aspect ratio by default
        if aspect_ratio_policy is None:
            aspect_ratio_policy = AspectRatioPolicy.SQUARE
        fig, ax = self._create_figure(config, aspect_ratio_policy, len(row_labels), len(col_labels))
        
        # Plot heatmap with equal aspect ratio for square cells
        im = ax.imshow(matrix_data, cmap=cmap, aspect='equal')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Value', rotation=270, labelpad=15)
        
        # Set ticks and labels
        ax.set_xticks(range(len(col_labels)))
        ax.set_yticks(range(len(row_labels)))
        ax.set_xticklabels(col_labels)
        ax.set_yticklabels(row_labels)
        
        # Rotate x-axis labels for better readability
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Show values in cells if requested
        if show_values:
            for i in range(len(row_labels)):
                for j in range(len(col_labels)):
                    text = ax.text(j, i, f"{matrix_data[i, j]:{value_format}}",
                                 ha="center", va="center", color="white" if matrix_data[i, j] > np.max(matrix_data)/2 else "black")
        
        # Set labels and title
        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        if title:
            set_title_below(ax, title)

        fig.tight_layout()
        
        # Use title as filename, or fallback to file's name
        fallback_name = resolve_fallback_name(title, [path], "heatmap")
        output_path = self.resolve_output_path(
            config.output_dir,
            save_path,
            fallback_name=fallback_name,
        )
        fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
        return fig, ax

    def _apply_style(self, config: PlotConfig, layout_mode: LayoutMode, policy: FontSizePolicy | None) -> None:
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

    def _create_figure(self, config: PlotConfig, aspect_ratio_policy: AspectRatioPolicy | None = None, 
                      n_rows: int = 1, n_cols: int = 1) -> tuple[Figure, Axes]:
        width_inch = config.source_figure_width_mm / _MM_PER_INCH
        height_inch = get_figure_height_inch(config, width_inch, nrows=1, policy=aspect_ratio_policy)
        
        # For heatmap with square policy, adjust figure size to match matrix dimensions
        if aspect_ratio_policy == AspectRatioPolicy.SQUARE:
            # Make figure square by using the larger dimension
            square_size = max(width_inch, height_inch)
            width_inch = square_size
            height_inch = square_size
        
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(width_inch, height_inch))
        return fig, ax

    @staticmethod
    def _read_matrix_from_csv(path: Path) -> tuple[np.ndarray, list[str], list[str]]:
        """Read matrix data from CSV file.
        
        Expected format:
        - First row contains column headers
        - First column contains row headers
        - Remaining cells contain numeric values
        
        Args:
            path: Path to CSV file
            
        Returns:
            Tuple of (matrix_data, row_labels, col_labels)
        """
        rows: list[list[str]] = []
        with path.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row:
                    rows.append(row)

        if not rows:
            raise ValueError(f"No data found in CSV file: {path}")

        # Extract headers
        col_labels = rows[0][1:]  # Skip first column header
        row_labels = [row[0] for row in rows[1:]]  # First column of remaining rows
        
        # Extract numeric data
        numeric_data = []
        for row in rows[1:]:
            try:
                numeric_row = [float(value) for value in row[1:]]  # Skip first column (row label)
                numeric_data.append(numeric_row)
            except ValueError as e:
                raise ValueError(f"Non-numeric value found in data: {e}")

        if not numeric_data:
            raise ValueError(f"No numeric data found in CSV file: {path}")

        # Check that all rows have the same length
        row_lengths = [len(row) for row in numeric_data]
        if len(set(row_lengths)) != 1:
            raise ValueError(f"Inconsistent row lengths in CSV file: {row_lengths}")

        matrix_data = np.array(numeric_data)
        
        # Validate dimensions match labels
        if matrix_data.shape[0] != len(row_labels):
            raise ValueError(f"Number of rows ({matrix_data.shape[0]}) doesn't match row labels ({len(row_labels)})")
        if matrix_data.shape[1] != len(col_labels):
            raise ValueError(f"Number of columns ({matrix_data.shape[1]}) doesn't match column labels ({len(col_labels)})")

        return matrix_data, row_labels, col_labels
