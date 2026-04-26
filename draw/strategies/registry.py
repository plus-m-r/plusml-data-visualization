from __future__ import annotations

from enum import Enum
from typing import Mapping

from .base import DrawStrategy, GridDrawStrategy, LineDrawStrategy
from .grid import GridChartStrategy
from .line import LineChartStrategy


class ChartType(str, Enum):
    """Supported chart types."""

    LINE = "line"
    GRID = "grid"


LINE_STRATEGY: LineDrawStrategy = LineChartStrategy()
GRID_STRATEGY: GridDrawStrategy = GridChartStrategy()


STRATEGY_BY_CHART_TYPE: Mapping[ChartType, DrawStrategy] = {
    ChartType.LINE: LINE_STRATEGY,
    ChartType.GRID: GRID_STRATEGY,
}
