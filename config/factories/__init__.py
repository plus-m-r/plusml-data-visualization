"""Factory pattern for strategy creation."""

from .font_size_factory import get_font_size_strategy
from .aspect_ratio_factory import get_aspect_ratio_strategy

__all__ = ["get_font_size_strategy", "get_aspect_ratio_strategy"]
