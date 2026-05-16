from __future__ import annotations

from .base import LineDrawStrategy
from .line import LineChartStrategy
from .scatter import ScatterChartStrategy
from .heatmap import HeatmapDrawStrategy


LINE_STRATEGY: LineDrawStrategy = LineChartStrategy()
SCATTER_STRATEGY = ScatterChartStrategy()
HEATMAP_STRATEGY: HeatmapDrawStrategy = HeatmapDrawStrategy()
