from enum import Enum


class LayoutMode(str, Enum):
    """Layout modes: number of charts in one row."""

    ONE_PER_ROW = "1x1"
    TWO_PER_ROW = "1x2"
    THREE_PER_ROW = "1x3"
