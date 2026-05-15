"""Strategy pattern implementations for plotting configuration."""

from .base import FontSizeStrategy, AspectRatioStrategy
from .font_size.fixed_width import FixedSourceWidthStrategy
from .font_size.direct import FinalWidthDirectStrategy
from .aspect_ratio.four_to_three import FourToThreeStrategy
from .aspect_ratio.sixteen_to_nine import SixteenToNineStrategy
from .aspect_ratio.golden_ratio import GoldenRatioStrategy
from .aspect_ratio.square import SquareStrategy

__all__ = [
    "FontSizeStrategy",
    "AspectRatioStrategy",
    "FixedSourceWidthStrategy",
    "FinalWidthDirectStrategy",
    "FourToThreeStrategy",
    "SixteenToNineStrategy",
    "GoldenRatioStrategy",
    "SquareStrategy",
]
