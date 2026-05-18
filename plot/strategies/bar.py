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
)

from .base import DrawStrategy, auto_detect_chinese_font, set_title_below, resolve_fallback_name, apply_font_hierarchy

_MM_PER_INCH = 25.4


class BarChartStrategy(DrawStrategy):
    """Strategy for drawing bar charts with Nature-Figure standards.
    
    Features:
    - Bar edge colors for better visual separation
    - Value annotations inside/outside bars
    - Dynamic Y-axis scaling based on data range
    - Semantic color palette support
    """

    def draw_bar(
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
        annotate_values: bool = True,  # Phase 1: Enable value annotations by default
        show_edge_color: bool = True,  # Phase 1: Enable edge colors by default
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
            categories, values = self._read_categorical_data(path)
            data_series.append((categories, values, path))
        
        # Create figure
        fig, ax = self._create_figure(config, aspect_ratio_policy)
        
        # Plot bars with Nature-Figure styling
        palette = get_color_palette(config.color_palette_name)
        n_colors = len(palette.colors)
        
        # Calculate bar positions for grouped bars
        n_series = len(data_series)
        bar_width = 0.8 / n_series if n_series > 1 else 0.6
        
        all_bars = []
        for i, (categories, values, path) in enumerate(data_series):
            label = labels[i] if labels and i < len(labels) else None
            
            # Use semantic color palette
            color = palette.colors[i % n_colors]
            
            # Calculate x positions
            x_positions = list(range(len(categories)))
            offset = (i - (n_series - 1) / 2) * bar_width
            x_positions = [x + offset for x in x_positions]
            
            # Phase 1: Draw bars with edge colors
            bars = ax.bar(
                x_positions,
                values,
                width=bar_width,
                label=label,
                color=color,
                edgecolor='white' if show_edge_color else None,
                linewidth=1.5 if show_edge_color else 0,
            )
            
            all_bars.append((bars, values))
        
        # Phase 1: Add value annotations
        if annotate_values:
            font_size = get_plot_font_size_pt(mode, config=config, policy=policy, rounded=True)
            annotation_size = max(font_size - 1, 6)  # Slightly smaller than base font
            self._annotate_bars(ax, all_bars, annotation_size)
        
        # Set labels and title
        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        if title:
            set_title_below(ax, title)
        
        # Set x-axis ticks
        if data_series:
            categories = data_series[0][0]
            tick_positions = list(range(len(categories)))
            ax.set_xticks(tick_positions)
            ax.set_xticklabels(categories, rotation=0, ha='center')
        
        # Add legend if labels provided
        if labels and any(labels):
            ax.legend(loc='best', frameon=False)
        
        # Apply font hierarchy (Phase 1)
        context = getattr(config, 'font_size_context', 'journal_final')
        apply_font_hierarchy(ax, context)
        
        # Save figure
        fallback_name = resolve_fallback_name(title, paths, "bar_chart")
        output_path = self.resolve_output_path(config.output_dir, save_path, fallback_name=fallback_name)
        fig.savefig(output_path, dpi=dpi, bbox_inches='tight', facecolor='white')
        
        return fig, ax
    
    def _read_categorical_data(self, path: Path) -> tuple[list[str], list[float]]:
        """Read categorical data from CSV file.
        
        Expected format:
        category,value
        Category A,10.5
        Category B,20.3
        ...
        
        Args:
            path: Path to CSV file.
            
        Returns:
            Tuple of (categories, values).
        """
        categories = []
        values = []
        
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip header
            
            for row in reader:
                if len(row) >= 2:
                    categories.append(row[0].strip())
                    try:
                        values.append(float(row[1].strip()))
                    except ValueError:
                        continue
        
        if not categories:
            raise ValueError(f"No valid data found in {path}")
        
        return categories, values
    
    def _annotate_bars(self, ax: Axes, all_bars: list, fontsize: float) -> None:
        """Add value annotations to bars.
        
        Phase 1: Implements smart text color selection based on bar luminance.
        
        Args:
            ax: The matplotlib axes object.
            all_bars: List of (bars, values) tuples.
            fontsize: Font size for annotations.
        """
        for bars, values in all_bars:
            for bar, value in zip(bars, values):
                # Get bar color for smart text color selection
                bar_color = bar.get_facecolor()
                
                # Calculate luminance to determine text color
                # Formula: 0.299*R + 0.587*G + 0.114*B
                luminance = 0.299 * bar_color[0] + 0.587 * bar_color[1] + 0.114 * bar_color[2]
                
                # Choose contrasting text color
                textcolor = 'white' if luminance < 0.5 else 'black'
                
                # Position: slightly below the top of the bar
                y_position = bar.get_height() - (bar.get_height() * 0.05)
                
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    y_position,
                    f'{value:.2f}',
                    ha='center',
                    va='bottom',
                    fontsize=fontsize,
                    color=textcolor,
                    fontweight='bold',
                )
    
    def _create_figure(self, config: PlotConfig, aspect_ratio_policy: AspectRatioPolicy | None = None) -> tuple[Figure, Axes]:
        """Create a matplotlib figure with proper sizing."""
        width_inch = config.source_figure_width_mm / _MM_PER_INCH
        height_inch = get_figure_height_inch(config, width_inch, nrows=1, policy=aspect_ratio_policy)
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(width_inch, height_inch))
        return fig, ax
    
    def _apply_style(self, config: PlotConfig, layout_mode: LayoutMode, policy: FontSizePolicy | None) -> None:
        """Apply global matplotlib styling."""
        palette = get_color_palette(config.color_palette_name)
        font_size = get_plot_font_size_pt(
            layout_mode,
            config=config,
            policy=policy,
            rounded=True,
        )
        
        # Auto-configure Chinese font support
        actual_font = auto_detect_chinese_font(config.font_family)
        
        # Phase 1: Get axes linewidth based on font size context
        from config.constants import AXES_LINEWIDTH_BY_CONTEXT, DEFAULT_FONT_SIZE_CONTEXT
        context = getattr(config, 'font_size_context', DEFAULT_FONT_SIZE_CONTEXT)
        axes_linewidth = AXES_LINEWIDTH_BY_CONTEXT.get(context, 0.8)
        
        plt.rcParams.update(
            {
                "font.family": actual_font,
                "font.sans-serif": [actual_font, "Arial", "Helvetica", "DejaVu Sans"],
                "font.size": font_size,
                "axes.linewidth": axes_linewidth,
                "axes.spines.top": False,
                "axes.spines.right": False,
                "axes.labelsize": font_size + 2,
                "xtick.labelsize": font_size + 1,
                "ytick.labelsize": font_size + 1,
                "legend.fontsize": font_size,
                "figure.titlesize": font_size + 3,
                "svg.fonttype": "none",  # Keep text editable in SVG
                "axes.prop_cycle": cycler(color=palette.colors),
            }
        )
