"""
draw.simple: 简明绘图配置与接口

- 提供一站式获取全局绘图配置（字体、色板、输出目录等）
- 便于策略/可视化模块内部自动加载和复用
- 兼容 plusml-data-visualization/config 下所有主流配置
"""
from pathlib import Path
from typing import Any, Dict

from config import (
    DEFAULT_PLOT_CONFIG,
    get_color_palette,
    FONT_FAMILY,
    OUTPUT_DIR,
    COLOR_PALETTE_NAME,
    DEFAULT_COLOR_PALETTE,
    FINAL_PUBLICATION_FONT_PT,
    SOURCE_FIGURE_WIDTH_MM,
    FINAL_SUBPLOT_WIDTH_MM_BY_MODE,
)


def get_default_plot_config() -> Dict[str, Any]:
    """获取全局默认绘图配置（dict 格式，便于前端/脚本调用）"""
    return {
        "font_family": FONT_FAMILY,
        "output_dir": str(OUTPUT_DIR),
        "color_palette_name": COLOR_PALETTE_NAME,
        "color_palette": list(DEFAULT_COLOR_PALETTE.colors),
        "final_publication_font_pt": FINAL_PUBLICATION_FONT_PT,
        "source_figure_width_mm": SOURCE_FIGURE_WIDTH_MM,
        "final_subplot_width_mm_by_mode": FINAL_SUBPLOT_WIDTH_MM_BY_MODE,
    }


def get_color_palette_by_name(name: str):
    """通过名称获取色板（返回 ColorPalette 对象）"""
    return get_color_palette(name)


def ensure_output_dir_exists():
    """确保输出目录存在。"""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


# 快捷别名
default_config = get_default_plot_config
get_palette = get_color_palette_by_name
ensure_output_dir = ensure_output_dir_exists
