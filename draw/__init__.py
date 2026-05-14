"""Drawing interfaces based on Matplotlib."""

from .draw_interface import DrawInterface
from .font_utils import configure_matplotlib_for_chinese, detect_chinese_font
from .plotter import MatplotlibDrawer, draw_grid_chart, draw_line_chart
from .strategies import ChartType, DrawStrategy, GridChartStrategy, LineChartStrategy, STRATEGY_BY_CHART_TYPE

__all__ = [
    "ChartType",
    "DrawStrategy",
    "DrawInterface",
    "GridChartStrategy",
    "LineChartStrategy",
    "STRATEGY_BY_CHART_TYPE",
    "MatplotlibDrawer",
    "draw_line_chart",
    "draw_grid_chart",
    # Font utilities
    "configure_matplotlib_for_chinese",
    "detect_chinese_font",
]
