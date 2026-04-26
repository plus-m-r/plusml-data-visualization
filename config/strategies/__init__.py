"""Font size strategies for plotting configuration."""

from .base import FontSizeStrategy
from .direct import FinalWidthDirectStrategy
from .fixed_width import FixedSourceWidthStrategy
from .registry import STRATEGY_BY_POLICY

__all__ = [
    "FontSizeStrategy",
    "FixedSourceWidthStrategy",
    "FinalWidthDirectStrategy",
    "STRATEGY_BY_POLICY",
]
