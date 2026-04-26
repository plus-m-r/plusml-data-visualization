from __future__ import annotations

from enum import Enum
from typing import Mapping

from .base import DrawStrategy
from .grid import GridChartStrategy
from .line import LineChartStrategy


class ChartType(str, Enum):
    """Supported chart types."""

    LINE = "line"
    GRID = "grid"


STRATEGY_BY_CHART_TYPE: Mapping[ChartType, DrawStrategy] = {
    ChartType.LINE: LineChartStrategy(),
    ChartType.GRID: GridChartStrategy(),
}
