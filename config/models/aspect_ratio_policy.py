from enum import Enum


class AspectRatioPolicy(str, Enum):
    """Strategy selector for figure aspect ratio."""

    FOUR_TO_THREE = "4:3"
    SIXTEEN_TO_NINE = "16:9"
    GOLDEN_RATIO = "golden_ratio"
    SQUARE = "square"
