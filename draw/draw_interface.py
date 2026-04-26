from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Sequence

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from config import LayoutMode


class DrawInterface(ABC):
    """Abstract drawing interface for different plotting backends."""

    SUPPORTED_SOURCE_SUFFIXES = (".csv",)

    @classmethod
    def validate_source_file(cls, source_file: str) -> Path:
        """Validate a source file path and enforce supported file format."""
        path = Path(source_file)
        if not path.exists() or not path.is_file():
            raise ValueError(f"Source file does not exist or is not a file: {path}")
        suffix = path.suffix.lower()
        if suffix not in cls.SUPPORTED_SOURCE_SUFFIXES:
            allowed = ", ".join(cls.SUPPORTED_SOURCE_SUFFIXES)
            raise ValueError(
                f"Unsupported source file format: {suffix or '<none>'}. "
                f"Allowed formats: {allowed}"
            )
        return path

    @abstractmethod
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
        """Draw a single line chart from a validated source file."""

    @abstractmethod
    def draw_grid(
        self,
        source_files: Sequence[str],
        *,
        layout_mode: LayoutMode | str = LayoutMode.TWO_PER_ROW,
        figure_title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        save_path: str | None = None,
    ) -> tuple[Figure, list[Axes]]:
        """Draw a grid chart from validated source files."""
