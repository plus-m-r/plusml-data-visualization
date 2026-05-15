from dataclasses import dataclass
from typing import Mapping

from .aspect_ratio_policy import AspectRatioPolicy
from .font_size_policy import FontSizePolicy
from .layout_mode import LayoutMode


@dataclass(frozen=True)
class PlotConfig:
    """Immutable plotting configuration."""

    font_family: str
    final_publication_font_pt: float
    source_figure_width_mm: float
    final_subplot_width_mm_by_mode: Mapping[LayoutMode, float]
    output_dir: str = "figures"
    color_palette_name: str = "classic_academic_blue"
    default_font_size_policy: FontSizePolicy = FontSizePolicy.FIXED_SOURCE_WIDTH
    default_aspect_ratio_policy: AspectRatioPolicy = AspectRatioPolicy.FOUR_TO_THREE
