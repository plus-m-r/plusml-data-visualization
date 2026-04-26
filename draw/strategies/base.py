from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Sequence

from config import FontSizePolicy, LayoutMode, PlotConfig
from matplotlib.axes import Axes
from matplotlib.figure import Figure


class DrawStrategy(ABC):
    """Abstract strategy for drawing a specific chart type."""

    @abstractmethod
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
    ) -> tuple[Figure, Axes] | tuple[Figure, list[Axes]]:
        """Draw a chart with the given inputs."""

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
