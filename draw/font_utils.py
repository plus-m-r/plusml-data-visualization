"""Font management utilities for automatic Chinese font support."""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Optional

import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt


# 常见的中文字体名称（按优先级排序）
CHINESE_FONT_CANDIDATES = [
    # 首选：宋体和黑体（最常用、兼容性最好）
    "SimSun",                # 宋体（Windows/Linux通用）
    "STSong",                # 华文宋体（macOS）
    "SimHei",                # 黑体（Windows/Linux通用）
    "STHeiti",               # 华文黑体（macOS）
    
    # 次选：高质量开源字体
    "Noto Serif CJK SC",     # Noto宋体（Google，质量优秀）
    "Noto Sans CJK SC",      # Noto黑体（Google，质量优秀）
    
    # 备选：其他常见字体
    "Microsoft YaHei",       # 微软雅黑（Windows）
    "WenQuanYi Zen Hei",     # 文泉驿正黑（Linux）
    "WenQuanYi Micro Hei",   # 文泉驿微米黑（Linux）
    "KaiTi",                 # 楷体
    "FangSong",              # 仿宋
    "PingFang SC",           # 苹方（macOS）
    "AR PL UMing CN",        # 文鼎PL简中明
    "Droid Sans Fallback",   # Droid回退字体
]


def detect_chinese_font() -> Optional[str]:
    """
    检测系统中可用的中文字体。
    
    Returns:
        可用的中文字体名称，如果未找到则返回 None
    """
    # 按优先级直接尝试常见字体名称
    for candidate in CHINESE_FONT_CANDIDATES:
        try:
            # 尝试创建字体属性
            prop = fm.FontProperties(family=candidate)
            # 检查字体是否可用
            if prop.get_name() and prop.get_name() != 'DejaVu Sans':
                return candidate
        except Exception:
            continue
    
    # 如果常用字体都不可用，尝试从系统字体中查找
    try:
        font_paths = fm.findSystemFonts(fontpaths=None, fontext='ttf')
        
        # 模糊匹配中文字体
        chinese_keywords = ['cjk', 'chinese', 'simhei', 'simsun', 'wenquan', 
                           'noto', 'microsoft yahei', 'pingfang', 'stheiti']
        
        for font_path in font_paths[:100]:  # 只检查前100个字体以提高速度
            try:
                font_lower = font_path.lower()
                if any(keyword in font_lower for keyword in chinese_keywords):
                    font_prop = fm.FontProperties(fname=font_path)
                    return font_prop.get_name()
            except Exception:
                continue
    except Exception:
        pass
    
    return None


def setup_chinese_support(font_family: str) -> str:
    """
    配置matplotlib以支持中文显示。
    
    如果指定的字体不支持中文，自动检测并切换到可用的中文字体。
    
    Args:
        font_family: 用户指定的字体名称
        
    Returns:
        实际使用的字体名称
    """
    # 常见不支持中文的西文字体
    non_chinese_fonts = [
        "Times New Roman", "Arial", "Helvetica", "Courier New", 
        "Georgia", "Verdana", "Calibri", "Cambria"
    ]
    
    # 检查是否需要中文字体支持
    needs_chinese = font_family in non_chinese_fonts
    
    if not needs_chinese:
        # 用户可能已经指定了中文字体，直接使用
        return font_family
    
    # 尝试检测系统中的中文字体
    chinese_font = detect_chinese_font()
    
    if chinese_font:
        warnings.warn(
            f"Font '{font_family}' does not support Chinese characters. "
            f"Automatically switching to '{chinese_font}' for better Chinese support.",
            UserWarning,
            stacklevel=3
        )
        return chinese_font
    else:
        # 没有找到中文字体，使用默认sans-serif并警告
        warnings.warn(
            f"Font '{font_family}' does not support Chinese characters and "
            f"no Chinese font was found on the system. Chinese text may not display correctly. "
            f"Consider installing a Chinese font (e.g., fonts-noto-cjk on Linux).",
            UserWarning,
            stacklevel=3
        )
        return "sans-serif"


def configure_matplotlib_for_chinese(font_family: str) -> str:
    """
    配置matplotlib的全局字体设置以支持中文。
    
    Args:
        font_family: 基础字体名称
        
    Returns:
        实际配置的字体名称
    """
    # 检测并选择合适的字体
    actual_font = setup_chinese_support(font_family)
    
    # 配置matplotlib
    plt.rcParams['font.sans-serif'] = [actual_font] + plt.rcParams.get('font.sans-serif', [])
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    
    return actual_font


def clear_font_cache() -> bool:
    """
    清除matplotlib的字体缓存。
    
    Returns:
        是否成功清除缓存
    """
    try:
        cache_dir = Path(matplotlib.get_cachedir())
        if cache_dir.exists():
            import shutil
            shutil.rmtree(cache_dir)
            return True
    except Exception:
        pass
    return False


def rebuild_font_manager() -> None:
    """重建matplotlib字体管理器。"""
    try:
        fm._rebuild()
    except Exception:
        pass
