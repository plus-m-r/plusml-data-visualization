# PlusML Data Visualization

**⚠️ 开发测试阶段：当前版本仅用于内部验证，暂不可用于生产或正式科研流程。**

## 项目状态

⚠️ 当前项目处于开发测试阶段，功能与接口可能随时变动，暂不建议用于生产或正式科研流程。

## Project Status

**⚠️ Development and testing stage: This project is for internal validation only and must not be used in production or formal research workflows.**

## 项目简介

本小型 Python 代码库的目的在于构建一个画图框架，通过硬性规定字体及其大小与图片大小，以及图片生成方式，保证能够高质量的稳定产出优质图片，且从侧面辅助养成良好的科研习惯。

## 核心特性

- 📐 **标准化输出**：统一规定字体、字号和图片尺寸，确保输出一致性
- 🎨 **高质量绘图**：稳定的图片生成方式，保证科研级图像质量
- 🔬 **科研友好**：辅助培养规范的科研绘图习惯
- 🚀 **简单易用**：轻量级框架，快速上手

## Config 使用

当前配置采用 `config/` 包结构（模型 + 策略 + 默认值 + API），建议统一从包入口导入。

### 色系配置

论文绘图没有绝对统一的官方色谱，但可以使用一些更稳妥的安全模板。当前库内置了这些色盘：

- `classic_academic_blue`: 经典学术蓝
- `natural_friendly`: 自然亲和系
- `distinct_qualitative`: 区分度高的定性色板
- `macaron`: 马卡龙色系
- `blue_orange_safe`: 蓝橙安全双色
- `blue_yellow_safe`: 蓝黄橙安全组合
- `blue_purple_safe`: 蓝紫安全组合
- `two_color`: 简洁双色方案
- `tri_color`: 三色参考方案

默认色盘是 `classic_academic_blue`。如果你想在同一套风格下切换配色，只需要改 `PlotConfig.color_palette_name`。

### 1) 快速使用默认配置

```python
from config import (
    COLOR_PALETTE_NAME,
    DEFAULT_COLOR_PALETTE,
    FONT_FAMILY,
    MODE_ONE_PER_ROW,
    RECOMMENDED_PLOT_FONT_SIZE_PT_BY_MODE,
    get_plot_font_size_pt,
)

print(FONT_FAMILY)  # Times New Roman
print(COLOR_PALETTE_NAME)  # classic_academic_blue
print(DEFAULT_COLOR_PALETTE.colors)
print(RECOMMENDED_PLOT_FONT_SIZE_PT_BY_MODE[MODE_ONE_PER_ROW])

# 精确值（非四舍五入）
font_pt = get_plot_font_size_pt(MODE_ONE_PER_ROW)
print(font_pt)
```

### 2) 切换字号策略

```python
from config import FontSizePolicy, LayoutMode, get_plot_font_size_pt

# 策略一：固定原始宽度缩放（默认）
scaled_pt = get_plot_font_size_pt(LayoutMode.TWO_PER_ROW)

# 策略二：按最终出版宽度直接使用 7pt（所见即所得）
direct_pt = get_plot_font_size_pt(
    LayoutMode.TWO_PER_ROW,
    policy=FontSizePolicy.FINAL_WIDTH_DIRECT,
)

print(scaled_pt, direct_pt)
```

### 3) 使用字符串模式（兼容旧代码）

```python
from config import get_plot_font_size_pt

pt = get_plot_font_size_pt("1x3", rounded=True)
print(pt)  # 22
```

## Config 自定义拓展

### 1) 自定义期刊或项目配置

```python
from config import FontSizePolicy, LayoutMode, PlotConfig, get_plot_font_size_pt

my_config = PlotConfig(
    font_family="Times New Roman",
    final_publication_font_pt=8.0,
    source_figure_width_mm=180.0,
    output_dir="figures",
    color_palette_name="macaron",
    final_subplot_width_mm_by_mode={
        LayoutMode.ONE_PER_ROW: 92.0,
        LayoutMode.TWO_PER_ROW: 88.0,
        LayoutMode.THREE_PER_ROW: 58.0,
    },
    default_font_size_policy=FontSizePolicy.FIXED_SOURCE_WIDTH,
)

pt = get_plot_font_size_pt(LayoutMode.THREE_PER_ROW, config=my_config, rounded=True)
print(pt)
```

### 2) 自定义策略（新增算法）

你可以实现自己的策略类，并注册到策略映射中：

```python
from config import STRATEGY_BY_POLICY, LayoutMode, PlotConfig


class ConservativeStrategy:
    """示例：在固定缩放基础上再乘以 0.95。"""

    def calc_plot_font_size_pt(self, config: PlotConfig, layout_mode: LayoutMode) -> float:
        final_width_mm = config.final_subplot_width_mm_by_mode[layout_mode]
        base = config.final_publication_font_pt * config.source_figure_width_mm / final_width_mm
        return base * 0.95
```

如果你希望把该策略接入 `get_plot_font_size_pt` 的统一入口，建议新增一个策略枚举值并在 `config/defaults.py` 的 `STRATEGY_BY_POLICY` 中注册，确保调用路径一致。

### 3) 目录结构说明

- `config/models/layout_mode.py`: 布局枚举
- `config/models/font_size_policy.py`: 策略枚举
- `config/models/plot_config.py`: 不可变配置对象
- `config/models/color_palette.py`: 色盘数据对象
- `config/strategies/base.py`: 字号策略协议
- `config/strategies/fixed_width.py`: 固定原始宽度策略
- `config/strategies/direct.py`: 直接最终宽度策略
- `config/strategies/registry.py`: 策略注册表
- `config/colors/presets.py`: 内置色盘预设
- `config/colors/registry.py`: 色盘注册与查询
- `config/api.py`: 统一调用入口
- `config/__init__.py`: 对外导出与兼容常量
- `draw/strategies/base.py`: 绘图策略基类
- `draw/strategies/line.py`: 单图策略
- `draw/strategies/grid.py`: 网格图策略
- `draw/strategies/registry.py`: 图类型到策略的注册表
- `draw/plotter.py`: 绘图上下文与对外便捷函数
- `draw/draw_interface.py`: 文件输入约束接口

## Draw 使用（强制文件输入）

为培养“先保存数据再绘图”的习惯，绘图接口只接收已存在的 `.csv` 文件：

- 输入必须是文件路径，不接受内存数组
- 文件后缀必须为 `.csv`
- 文件必须真实存在
- 所有图像默认保存到同一个输出文件夹（当前默认是 `figures/`）
- 即使手动传入 `save_path`，也必须落在这个输出文件夹下，允许 `figures/` 内的嵌套子目录

当前 `draw/` 目录还采用了策略模式，不同图类型由不同策略处理：

- `line`：单图策略
- `grid`：网格图策略

后续如果你要增加 `bar`、`scatter`、`heatmap` 等图形，只需要新增对应策略类并注册到策略表里。

### 1) 单图绘制

```python
from draw import draw_line_chart

fig, ax = draw_line_chart(
    source_file="data/line.csv",
    title="Demo Line",
    xlabel="X",
    ylabel="Y",
    save_path="figures/2026/line.png",
)
```

### 2) 多图绘制

```python
from draw import draw_grid_chart

fig, axes = draw_grid_chart(
    source_files=["data/a.csv", "data/b.csv"],
    save_path="figures/grid.png",
)
```

### 3) CSV 数据格式

- 单列：视为 `y`，`x` 自动使用 `0..n-1`
- 双列及以上：默认使用前两列作为 `x, y`
- 允许首行表头（非数字行会自动跳过）

## 许可证

本项目采用 [MIT License](LICENSE) 开源协议。
