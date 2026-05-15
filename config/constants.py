"""Pure constants with no dependencies.

This module contains only primitive constants that don't depend on any other modules.
"""

# Common Chinese font names in priority order
CHINESE_FONTS = [
    'STSong', 'STFangsong',  # 宋体、仿宋 (Adobe 字体)
    'SimSun', 'FangSong',  # 宋体、仿宋 (Windows 标准)
    'WenQuanYi Zen Hei', 'WenQuanYi Micro Hei',  # 文泉驿
    'Noto Serif SC', 'Noto Sans SC',  # 思源字体
    'SimHei', 'Microsoft YaHei',  # 黑体、微软雅黑
    'STHeiti', 'PingFang SC',  # macOS 字体
    'AR PL SungtiL GB', 'AR PL KaitiM GB',  # 文鼎字体
    'Droid Sans Fallback',
]

# Standard line styles for matplotlib plots
LINE_STYLES = ['-', '--', '-.', ':']

# Marker styles for matplotlib plots
MARKERS = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h', 'H', '+', 'x', 'X']

# Default plot styling constants
DEFAULT_MARKER_SIZE = 6
DEFAULT_LINE_WIDTH = 2

# Title positioning parameters
TITLE_POSITION_Y = -0.15  # Y position relative to axes (negative = below)
TITLE_VERTICAL_ALIGNMENT = 'top'
TITLE_HORIZONTAL_ALIGNMENT = 'center'
TITLE_FONT_SIZE = 'large'
