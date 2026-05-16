from __future__ import annotations

from .base import LineDrawStrategy
from .line import LineChartStrategy
from .scatter import ScatterChartStrategy


LINE_STRATEGY: LineDrawStrategy = LineChartStrategy()
SCATTER_STRATEGY = ScatterChartStrategy()