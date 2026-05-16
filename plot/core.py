from __future__ import annotations

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing import Sequence

from config import DEFAULT_PLOT_CONFIG, FontSizePolicy, PlotConfig, normalize_layout_mode

from .strategies import LINE_STRATEGY, SCATTER_STRATEGY, HEATMAP_STRATEGY


class Plotter:
    """PlusML plotting interface - single chart only."""

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

    def line(
        self,
        data_specs: Sequence[tuple[str, str | None, str | None, str | None]],
        *,
        title: str | None = None,
        layout: str = "1x1",
        save_path: str | None = None,
    ) -> tuple[Figure, Axes]:
        """Draw a line chart with one or more data series.
        
        Args:
            data_specs: List of tuples (source_file, xlabel, ylabel, label)
                - source_file: Path to CSV data file (required)
                - xlabel: X-axis label (optional, use first non-None value)
                - ylabel: Y-axis label (optional, use first non-None value)
                - label: Legend label for this series (optional)
            title: Chart title
            layout: Layout mode ("1x1", "2x1", "3x1")
            save_path: Output file path
            
        Returns:
            Tuple of (Figure, Axes)
            
        Examples:
            # Single curve
            p.line([
                ("data.csv", "Time", "Value", "Series 1")
            ], title="Single Line")
            
            # Multiple curves
            p.line([
                ("data1.csv", "Time", "Value", "Series 1"),
                ("data2.csv", "Time", "Value", "Series 2"),
            ], title="Multiple Lines")
        """
        from config import LayoutMode
        mode = normalize_layout_mode(layout)
        
        if not data_specs:
            raise ValueError("data_specs cannot be empty")
        
        # Extract source files and labels
        source_files = [spec[0] for spec in data_specs]
        labels = [spec[3] if len(spec) > 3 else None for spec in data_specs]
        
        # Use first data source's labels as default
        first_spec = data_specs[0]
        xlabel = first_spec[1] if len(first_spec) > 1 else None
        ylabel = first_spec[2] if len(first_spec) > 2 else None
        
        fig, ax = LINE_STRATEGY.draw_line(
            config=self.config,
            layout_mode=mode,
            source_files=source_files,
            labels=labels,
            policy=self.policy,
            aspect_ratio_policy=None,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            save_path=save_path,
            dpi=self.dpi,
        )
        return fig, ax

    def scatter(
        self,
        data_specs: Sequence[tuple[str, str | None, str | None, str | None]],
        *,
        title: str | None = None,
        layout: str = "1x1",
        save_path: str | None = None,
    ) -> tuple[Figure, Axes]:
        """Draw a scatter chart with one or more data series.
        
        Args:
            data_specs: List of tuples (source_file, xlabel, ylabel, label)
                - source_file: Path to CSV data file (required)
                - xlabel: X-axis label (optional, use first non-None value)
                - ylabel: Y-axis label (optional, use first non-None value)
                - label: Legend label for this series (optional)
            title: Chart title
            layout: Layout mode ("1x1", "2x1", "3x1")
            save_path: Output file path
            
        Returns:
            Tuple of (Figure, Axes)
            
        Examples:
            # Single scatter plot
            p.scatter([
                ("data.csv", "X", "Y", "Series 1")
            ], title="Single Scatter")
            
            # Multiple scatter plots
            p.scatter([
                ("data1.csv", "X", "Y", "Series 1"),
                ("data2.csv", "X", "Y", "Series 2"),
            ], title="Multiple Scatter")
        """
        from config import LayoutMode
        mode = normalize_layout_mode(layout)
        
        if not data_specs:
            raise ValueError("data_specs cannot be empty")
        
        # Extract source files and labels
        source_files = [spec[0] for spec in data_specs]
        labels = [spec[3] if len(spec) > 3 else None for spec in data_specs]
        
        # Use first data source's labels as default
        first_spec = data_specs[0]
        xlabel = first_spec[1] if len(first_spec) > 1 else None
        ylabel = first_spec[2] if len(first_spec) > 2 else None
        
        fig, ax = SCATTER_STRATEGY.draw_scatter(
            config=self.config,
            layout_mode=mode,
            source_files=source_files,
            labels=labels,
            policy=self.policy,
            aspect_ratio_policy=None,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            save_path=save_path,
            dpi=self.dpi,
        )
        return fig, ax

    def heatmap(
        self,
        data_file: str,
        *,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        layout: str = "1x1",
        save_path: str | None = None,
        cmap: str = "viridis",
        show_values: bool = False,
        value_format: str = ".2f",
    ) -> tuple[Figure, Axes]:
        """Draw a heatmap from a CSV file containing matrix data.
        
        Args:
            data_file: Path to CSV file with matrix data
                - First row contains column headers
                - First column contains row headers
                - Remaining cells contain numeric values
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            layout: Layout mode ("1x1", "1x2", "1x3")
            save_path: Output file path
            cmap: Colormap name (matplotlib colormap)
            show_values: Whether to show values in cells
            value_format: Format string for cell values
            
        Returns:
            Tuple of (Figure, Axes)
            
        Note:
            Heatmaps use square aspect ratio by default for better visualization.
            
        Examples:
            # Basic heatmap
            p.heatmap("matrix.csv", title="Correlation Matrix")
            
            # Heatmap with custom colormap and values shown
            p.heatmap("data.csv", title="Heatmap", cmap="coolwarm", show_values=True)
        """
        from config import LayoutMode
        mode = normalize_layout_mode(layout)
        
        fig, ax = HEATMAP_STRATEGY.draw_heatmap(
            config=self.config,
            layout_mode=mode,
            source_file=data_file,
            policy=self.policy,
            aspect_ratio_policy=None,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            save_path=save_path,
            dpi=self.dpi,
            cmap=cmap,
            show_values=show_values,
            value_format=value_format,
        )
        return fig, ax
