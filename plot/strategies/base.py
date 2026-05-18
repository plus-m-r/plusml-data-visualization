from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Sequence

from config import FontSizePolicy, LayoutMode, PlotConfig, CHINESE_FONTS, TITLE_POSITION_Y, TITLE_VERTICAL_ALIGNMENT, TITLE_HORIZONTAL_ALIGNMENT, TITLE_FONT_SIZE
from config.constants import FONT_SIZE_HIERARCHY, AXES_LINEWIDTH_BY_CONTEXT, DEFAULT_FONT_SIZE_CONTEXT
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def auto_detect_chinese_font(preferred_font: str) -> str:
    """Auto-detect an available Chinese font from the system.
    
    Checks the configured Chinese font list and returns the first available font.
    Falls back to the preferred font or 'sans-serif' if no Chinese font is found.
    
    Args:
        preferred_font: The user's preferred font name.
        
    Returns:
        The name of an available font.
    """
    import matplotlib.font_manager as fm
    
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    # Try to find an available Chinese font first
    for font in CHINESE_FONTS:
        if font in available_fonts:
            return font
    
    # If no Chinese font found, fall back to preferred font or sans-serif
    if preferred_font in available_fonts:
        return preferred_font
    
    return 'sans-serif'


def set_title_below(ax, title: str) -> None:
    """Place title at the bottom of the figure.
    
    Args:
        ax: The matplotlib axes object.
        title: The title text to display.
    """
    ax.text(0.5, TITLE_POSITION_Y, title, transform=ax.transAxes,
            fontsize=TITLE_FONT_SIZE, verticalalignment=TITLE_VERTICAL_ALIGNMENT,
            horizontalalignment=TITLE_HORIZONTAL_ALIGNMENT)


def apply_font_hierarchy(ax: Axes, context: str = None) -> None:
    """Apply Nature-Figure font size hierarchy to axes elements.
    
    Based on nature-figure skill typography standards. Sets appropriate font sizes
    for axis labels, tick labels, title, legend, and annotations based on context.
    
    Args:
        ax: The matplotlib axes object.
        context: Font size context ("journal_final", "large_panel", or "compact_panel").
                If None, uses DEFAULT_FONT_SIZE_CONTEXT.
    """
    if context is None:
        context = DEFAULT_FONT_SIZE_CONTEXT
    
    # Get font sizes for this context
    sizes = FONT_SIZE_HIERARCHY.get(context, FONT_SIZE_HIERARCHY[DEFAULT_FONT_SIZE_CONTEXT])
    
    # Apply to axis labels
    xlabel = ax.get_xlabel()
    ylabel = ax.get_ylabel()
    if xlabel:
        ax.xaxis.label.set_size(sizes["axis_label"])
    if ylabel:
        ax.yaxis.label.set_size(sizes["axis_label"])
    
    # Apply to tick labels
    ax.tick_params(axis='both', which='major', labelsize=sizes["tick_label"])
    
    # Apply to title
    title = ax.get_title()
    if title:
        # Find the title text object and update its size
        for text in ax.texts:
            if text.get_text() == title:
                text.set_fontsize(sizes["title"])
                break
    
    # Apply to legend
    legend = ax.get_legend()
    if legend:
        for text in legend.get_texts():
            text.set_fontsize(sizes["legend"])


def resolve_fallback_name(title: str | None, paths: list[Path], default: str = "plot") -> str:
    """Resolve fallback filename from title or first file path.
    
    Priority:
    1. title (if provided)
    2. First file's stem name
    3. Default name
    
    Args:
        title: Optional title to use as filename.
        paths: List of validated file paths.
        default: Default name if title and paths are not available.
        
    Returns:
        The fallback filename without extension.
    """
    if title:
        return title
    if paths and paths[0].stem:
        return paths[0].stem
    return default


class DrawStrategy(ABC):
    """Shared helper methods for drawing strategies."""

    @staticmethod
    def validate_source_file(source_file: str) -> Path:
        """Validate CSV-only source files and ensure the file exists."""
        path = Path(source_file)
        if not path.exists() or not path.is_file():
            raise ValueError(f"Source file does not exist or is not a file: {path}")
        if path.suffix.lower() != ".csv":
            raise ValueError(
                f"Unsupported source file format: {path.suffix or '<none>'}. Allowed formats: .csv"
            )
        return path

    @staticmethod
    def resolve_output_path(
        output_dir: str,
        save_path: str | None,
        *,
        fallback_name: str,
    ) -> Path:
        """Resolve and validate the final output path under the fixed output root."""
        base_dir = Path(output_dir).expanduser().resolve()
        base_dir.mkdir(parents=True, exist_ok=True)

        if save_path is None:
            return base_dir / f"{fallback_name}.png"

        candidate = Path(save_path).expanduser()
        if not candidate.is_absolute():
            candidate = (base_dir / candidate).resolve()
        else:
            candidate = candidate.resolve()

        try:
            candidate.relative_to(base_dir)
        except ValueError as exc:
            raise ValueError(
                f"save_path must be inside the configured output directory: {base_dir}"
            ) from exc

        candidate.parent.mkdir(parents=True, exist_ok=True)
        return candidate


class LineDrawStrategy(DrawStrategy):
    """Interface for line chart strategies (supports multiple data series)."""

    @abstractmethod
    def draw_line(
        self,
        *,
        config: PlotConfig,
        layout_mode: LayoutMode,
        source_files: Sequence[str],
        labels: Sequence[str | None] | None = None,
        policy: FontSizePolicy | None = None,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        save_path: str | None = None,
        dpi: int = 300,
    ) -> tuple[Figure, Axes]:
        """Draw a line chart from one or more CSV files.
        
        Args:
            source_files: List of CSV file paths
            labels: Optional legend labels for each series
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
        """
