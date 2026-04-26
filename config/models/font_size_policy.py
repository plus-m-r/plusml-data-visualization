from enum import Enum


class FontSizePolicy(str, Enum):
    """Strategy selector for plotting-time font size."""

    FIXED_SOURCE_WIDTH = "fixed_source_width"
    FINAL_WIDTH_DIRECT = "final_width_direct"
