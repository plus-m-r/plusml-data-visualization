# PlusML Data Visualization

**⚠️ 开发测试阶段：当前版本仅用于内部验证，暂不可用于生产或正式科研流程。**

## 项目简介

本小型 Python 代码库的目的在于构建一个画图框架，通过硬性规定字体及其大小与图片大小，以及图片生成方式，保证能够高质量的稳定产出优质图片，且从侧面辅助养成良好的科研习惯。

### ✨ 核心特性

- 📐 **标准化输出**：统一规定字体、字号和图片尺寸，确保输出一致性
- 🎨 **高质量绘图**：稳定的图片生成方式，保证科研级图像质量（300 DPI）
- 🔬 **科研友好**：辅助培养规范的科研绘图习惯
- 🚀 **简单易用**：轻量级框架，快速上手
- 🌏 **自动中文支持**：开箱即用的中文字体检测和切换（优先宋体/黑体）
- 🎯 **策略模式架构**：基于设计模式的可扩展架构，轻松添加新图表类型
- ♿ **无障碍配色**：内置色盲友好的配色方案，确保图表可读性

## 安装

### 本地安装（推荐）

```bash
# 开发模式安装（可编辑）
pip install -e .

# 或从分发包安装
pip install dist/plusml_data_visualization-0.1.0-py3-none-any.whl
```

### 依赖要求

安装包时会自动安装以下依赖：
- matplotlib
- ogb >= 1.3.6
- Python >= 3.7

## 快速开始

### 使用 Plotter 接口（推荐）

```python
from plot import Plotter

# 创建绘图器
p = Plotter()

# 绘制单曲线折线图
fig, ax = p.line([
    ("data/experiment.csv", "时间 (秒)", "温度 (°C)", "实验组")
], title="实验结果", save_path="figures/result.png")

# 绘制多曲线对比图
fig, ax = p.line([
    ("data/control.csv", "Time", "Value", "Control"),
    ("data/treatment.csv", "Time", "Value", "Treatment"),
], title="Comparison", save_path="figures/comparison.png")

# 绘制散点图
fig, ax = p.scatter([
    ("data/scatter.csv", "X Values", "Y Values", "Data Points")
], title="Scatter Plot", save_path="figures/scatter.png")
```

### 使用配置系统

```python
from config import FONT_FAMILY, COLOR_PALETTE_NAME, get_plot_font_size_pt

print(f"默认字体: {FONT_FAMILY}")  # Times New Roman
print(f"默认配色: {COLOR_PALETTE_NAME}")  # classic_academic_blue

# 获取不同布局模式的字号
font_pt_1x1 = get_plot_font_size_pt("1x1", rounded=True)
font_pt_1x2 = get_plot_font_size_pt("1x2", rounded=True)
font_pt_1x3 = get_plot_font_size_pt("1x3", rounded=True)

print(f"1x1 布局字号: {font_pt_1x1} pt")
print(f"1x2 布局字号: {font_pt_1x2} pt")
print(f"1x3 布局字号: {font_pt_1x3} pt")
```

## Config 配置系统

当前配置采用 `config/` 包结构（模型 + 策略 + 默认值 + API），建议统一从包入口导入。

### 色系配置

论文绘图没有绝对统一的官方色谱，但可以使用一些更稳妥的安全模板。当前库内置了这些色盘：

- `classic_academic_blue`: 经典学术蓝（默认）
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

### 4) 布局模式说明

- `1x1` (ONE_PER_ROW): 单图占满一行，适合重点展示
- `1x2` (TWO_PER_ROW): 两图并排，适合对比分析
- `1x3` (THREE_PER_ROW): 三图并排，适合系列展示

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

```
config/
├── models/              # 数据模型
│   ├── layout_mode.py       # 布局枚举
│   ├── font_size_policy.py  # 字号策略枚举
│   ├── aspect_ratio_policy.py  # 宽高比策略枚举
│   ├── plot_config.py       # 不可变配置对象
│   └── color_palette.py     # 色盘数据对象
├── strategies/          # 策略实现
│   ├── font_size/           # 字号计算策略
│   │   ├── fixed_width.py   # 固定原始宽度策略
│   │   └── direct.py        # 直接最终宽度策略
│   └── aspect_ratio/        # 宽高比计算策略
│       ├── four_to_three.py # 4:3 比例
│       ├── sixteen_to_nine.py  # 16:9 比例
│       ├── golden_ratio.py  # 黄金比例
│       └── square.py        # 正方形
├── factories/           # 工厂模式
│   ├── font_size_factory.py   # 字号策略工厂
│   └── aspect_ratio_factory.py  # 宽高比策略工厂
├── services/            # 服务层（高层 API）
│   ├── font_service.py      # 字号计算服务
│   └── figure_service.py    # 图形尺寸服务
├── colors/              # 配色系统
│   ├── presets.py           # 内置色盘预设
│   └── registry.py          # 色盘注册与查询
├── presets/             # 默认配置
│   └── default_presets.py   # 默认 PlotConfig
├── constants.py         # 常量定义
└── __init__.py          # 对外导出与兼容常量

plot/
├── strategies/          # 绘图策略
│   ├── base.py              # 绘图策略基类
│   ├── line.py              # 折线图策略
│   └── registry.py          # 策略注册表
├── core.py              # Plotter 核心类
└── __init__.py          # 模块导出
```

## Plot 绘图接口（强制文件输入）

为培养"先保存数据再绘图"的习惯，绘图接口只接收已存在的 `.csv` 文件：

- ✅ 输入必须是文件路径，不接受内存数组
- ✅ 文件后缀必须为 `.csv`
- ✅ 文件必须真实存在
- ✅ 所有图像默认保存到同一个输出文件夹（当前默认是 `figures/`）
- ✅ 即使手动传入 `save_path`，也必须落在这个输出文件夹下，允许 `figures/` 内的嵌套子目录

### 🌏 自动中文支持

**包会自动处理中文字体，无需手动配置！**

当检测到标题或标签中包含中文字符时：
1. 自动扫描系统中可用的中文字体
2. **优先使用宋体 (SimSun) 或黑体 (SimHei)**
3. 如果不可用，自动降级到其他中文字体（Noto CJK、WenQuanYi 等）
4. 发出友好警告提示用户
5. 继续正常绘图

```python
from plot import Plotter

p = Plotter()

# 直接使用中文 - 自动支持！
fig, ax = p.line([
    ("data/experiment.csv", "时间 (秒)", "温度 (°C)", "实验组")
], title="实验结果", save_path="figures/result.png")
```

**注意**：如果宋体/黑体无法使用，可能是 matplotlib 字体缓存问题。解决方法：

```python
import matplotlib
from pathlib import Path
import shutil

# 清除缓存
cache_dir = Path(matplotlib.get_cachedir())
if cache_dir.exists():
    shutil.rmtree(cache_dir)
    print("缓存已清除，请重新运行")
```

当前 `plot/` 目录采用了策略模式，不同图类型由不同策略处理：

- `line`：折线图策略
- `scatter`：散点图策略

后续如果你要增加 `bar`、`heatmap` 等图形，只需要新增对应策略类并注册到策略表里。

### 1) 折线图绘制

#### 单曲线

```python
from plot import Plotter

p = Plotter()

fig, ax = p.line([
    ("data/line.csv", "X", "Y", "Series 1")
], title="Single Line", save_path="figures/line.png")
```

#### 多曲线对比

```python
fig, ax = p.line([
    ("data/control.csv", "Time", "Value", "Control"),
    ("data/treatment.csv", "Time", "Value", "Treatment"),
    ("data/experimental.csv", "Time", "Value", "Experimental"),
], title="Multiple Lines Comparison", save_path="figures/multi_line.png")
```

#### 不同布局模式

```python
# 1x1 布局（单图占满）
fig, ax = p.line([
    ("data/data.csv", "X", "Y", "Data")
], title="Full Width", layout="1x1", save_path="figures/full.png")

# 1x2 布局（两图并排）
fig, ax = p.line([
    ("data/data.csv", "X", "Y", "Data")
], title="Half Width", layout="1x2", save_path="figures/half.png")

# 1x3 布局（三图并排）
fig, ax = p.line([
    ("data/data.csv", "X", "Y", "Data")
], title="Third Width", layout="1x3", save_path="figures/third.png")
```

### 2) 散点图绘制

```python
from plot import Plotter

p = Plotter()

# 单组散点
fig, ax = p.scatter([
    ("data/scatter.csv", "X Values", "Y Values", "Data Points")
], title="Scatter Plot", save_path="figures/scatter.png")

# 多组散点对比
fig, ax = p.scatter([
    ("data/group1.csv", "X", "Y", "Group 1"),
    ("data/group2.csv", "X", "Y", "Group 2"),
], title="Multiple Groups", save_path="figures/multi_scatter.png")
```

### 3) CSV 数据格式

- **单列**：视为 `y`，`x` 自动使用 `0..n-1`
- **双列及以上**：默认使用前两列作为 `x, y`
- **允许首行表头**：非数字行会自动跳过
- **编码**：支持 UTF-8 编码

示例 CSV 文件：

```csv
# 双列数据（x, y）
Time,Temperature
0,20.5
1,21.3
2,22.1
3,23.0
```

```csv
# 单列数据（自动生成 x）
Value
20.5
21.3
22.1
23.0
```

### 4) 高级用法

#### 自定义配置

```python
from plot import Plotter
from config import PlotConfig

# 使用自定义配置
custom_config = PlotConfig(
    font_family="Arial",
    color_palette_name="macaron",
    output_dir="custom_figures",
)

p = Plotter(config=custom_config, dpi=600)

fig, ax = p.line([
    ("data/data.csv", "X", "Y", "Data")
], title="High Quality Plot", save_path="custom_figures/hq.png")
```

#### 自定义字号策略

```python
from plot import Plotter
from config import FontSizePolicy

# 使用直接最终宽度策略
p = Plotter(policy=FontSizePolicy.FINAL_WIDTH_DIRECT)

fig, ax = p.line([
    ("data/data.csv", "X", "Y", "Data")
], title="Direct Policy Plot", save_path="figures/direct.png")
```

## 设计架构

本项目采用多种设计模式，确保代码的可扩展性和可维护性：

### 策略模式 (Strategy Pattern)

- **字号计算策略**：`FontSizePolicy` 支持多种字号计算方式
- **宽高比策略**：`AspectRatioPolicy` 支持多种图形比例
- **绘图策略**：不同图表类型（折线图、散点图等）由独立策略处理

### 工厂模式 (Factory Pattern)

- **策略工厂**：根据策略枚举自动创建对应的策略实例
- **简化配置**：用户只需指定策略名称，无需关心具体实现

### 服务层 (Service Layer)

- **高层 API**：提供简洁的函数接口，隐藏复杂实现细节
- **统一入口**：所有配置和计算通过统一的服务层访问

### 关注点分离 (Separation of Concerns)

- **models/**: 数据模型定义
- **strategies/**: 策略实现
- **factories/**: 对象创建
- **services/**: 业务逻辑
- **colors/**: 配色管理
- **presets/**: 默认配置

## 扩展指南

### 添加新的图表类型

1. 创建新的策略类（继承 `DrawStrategy`）
2. 实现 `draw_*` 方法
3. 在 `plot/strategies/registry.py` 中注册策略
4. 在 `Plotter` 类中添加便捷方法

示例：添加柱状图

```python
# plot/strategies/bar.py
from .base import DrawStrategy

class BarChartStrategy(DrawStrategy):
    def draw_bar(self, ...):
        # 实现柱状图绘制逻辑
        pass

# plot/strategies/registry.py
from .bar import BarChartStrategy
BAR_STRATEGY = BarChartStrategy()

# plot/core.py
class Plotter:
    def bar(self, ...):
        return BAR_STRATEGY.draw_bar(...)
```

### 添加新的配色方案

```python
# config/colors/presets.py
from ..models import ColorPalette

MY_CUSTOM_PALETTE = ColorPalette(
    name="my_custom",
    colors=("#FF0000", "#00FF00", "#0000FF"),
    description="我的自定义配色",
    use_case="特定场景使用",
)

# config/colors/registry.py
from .presets import MY_CUSTOM_PALETTE
COLOR_PALETTES["my_custom"] = MY_CUSTOM_PALETTE
```

### 添加新的字号策略

```python
# config/strategies/font_size/my_strategy.py
from ..base import FontSizeStrategy
from ...models import PlotConfig, LayoutMode

class MyFontSizeStrategy(FontSizeStrategy):
    def calc_plot_font_size_pt(self, config: PlotConfig, layout_mode: LayoutMode) -> float:
        # 实现自定义字号计算逻辑
        pass

# config/factories/font_size_factory.py
from ..strategies.font_size.my_strategy import MyFontSizeStrategy
from ...models import FontSizePolicy

STRATEGY_MAP[FontSizePolicy.MY_STRATEGY] = MyFontSizeStrategy()
```

## 常见问题

### Q: 如何修改默认输出目录？

```python
from config import PlotConfig

config = PlotConfig(output_dir="my_output")
```

### Q: 如何更改默认 DPI？

```python
from plot import Plotter

p = Plotter(dpi=600)  # 设置为 600 DPI
```

### Q: 中文显示为方块怎么办？

清除 matplotlib 字体缓存后重新运行：

```python
import matplotlib
from pathlib import Path
import shutil

cache_dir = Path(matplotlib.get_cachedir())
if cache_dir.exists():
    shutil.rmtree(cache_dir)
```

### Q: 如何查看当前配置？

```python
from config import DEFAULT_PLOT_CONFIG

print(DEFAULT_PLOT_CONFIG)
```

### Q: 支持哪些图片格式？

支持 matplotlib 支持的所有格式：
- PNG (`.png`)
- PDF (`.pdf`)
- SVG (`.svg`)
- EPS (`.eps`)
- JPG (`.jpg`, `.jpeg`)

只需在 `save_path` 中指定相应扩展名即可。

## 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 📊 Nature-Figure 风格图表

本库遵循 **nature-figure skill** 的理念和 Nature 期刊标准，提供出版级质量的图表输出。

### Nature-Figure 核心原则

1. **核心结论驱动设计**
   - 每个图表都从一个明确的科学主张开始
   - 用图证明某个科学主张，而非简单地"画个图"

2. **证据层次映射**
   - 雷达图：展示多维度证据，证明模型的全面优势
   - 柱状图：提供单一指标的清晰对比，支持主要结论

3. **出版级质量输出**
   - **SVG**: 文本可编辑，可在 Illustrator 中进一步修改
   - **PDF**: 符合期刊投稿要求，嵌入 TrueType 字体
   - **TIFF**: 600 DPI，满足印刷质量要求

4. **Nature 风格美学**
   - **字体**: Arial/Helvetica sans-serif 家族（默认 Arial）
   - **字号**: 7pt 正文，8pt 标题
   - **配色**: 克制的语义化调色板
   - **布局**: 单栏宽度（3.5 英寸 ≈ 89mm）
   - **线条**: 细线宽（0.5-1.5pt），减少视觉噪音

5. **极简坐标轴设计**
   - 移除顶部和右侧边框
   - 无框图例，减少视觉干扰
   - 轻量级网格线辅助阅读

### Nature-Figure 测试示例

项目包含完整的 Nature-Figure 风格测试，生成雷达图和柱状图示例：

```bash
# 运行 Nature-Figure 风格测试
python tests/unit/test_nature_figure.py

# 查看生成的图表
ls -lh figures/ | grep -E "radar|bar"
```

生成的示例图表包括：
- **雷达图** (`figures/radar_chart_model_comparison.*`): 多模型性能对比
- **柱状图** (`figures/bar_chart_accuracy.*`): 准确率对比

输出格式：
- `.svg` - 可编辑矢量图（~12K）
- `.pdf` - 打印就绪（~45K）
- `.tiff` - 600 DPI 高分辨率（~12-14M）

详细测试说明请参考：[tests/NATURE_FIGURE_TEST_README.md](tests/NATURE_FIGURE_TEST_README.md)

---

## ⚙️ 配置系统详解

### 默认配置优化总结

基于 **nature-figure skill** 的标准和 Nature 期刊要求，PlusML 数据可视化库的默认配置已进行全面优化：

#### ✅ 1. DPI 分辨率提升 (300 → 600)

**变更内容**：
```python
# 之前
dpi: int = 300

# 现在
dpi: int = 600  # Nature journal standard
```

**原因**：
- Nature/Science 等顶级期刊要求至少 600 DPI
- 提供更清晰的细节和更平滑的边缘
- 与 nature-figure skill 推荐标准对齐

**影响**：
- PNG/TIFF 文件大小约增加 2-4 倍
- SVG/PDF 文件大小基本不变（矢量格式）
- 生成时间略微增加（通常 < 1 秒）

**向后兼容**：完全向后兼容，可以显式指定不同的 DPI：
```python
from plot import Plotter

# 使用默认的 600 DPI（推荐用于出版）
p = Plotter()

# 使用较低的 DPI（快速预览）
p_preview = Plotter(dpi=150)

# 使用极高的 DPI（超高质量印刷）
p_print = Plotter(dpi=1200)
```

#### ✅ 2. 字体家族更改 (Times New Roman → Arial)

**变更内容**：
```python
# 之前
font_family="Times New Roman"

# 现在
font_family="Arial"  # Nature standard: sans-serif
```

**原因**：
- **Nature 标准**: 使用 sans-serif 字体（Arial/Helvetica）
- 更好的屏幕和印刷可读性
- 现代科学出版物的通用选择

#### ✅ 3. 线宽优化 (2 → 1.5)

**变更内容**：
```python
# 之前
DEFAULT_LINE_WIDTH = 2

# 现在
DEFAULT_LINE_WIDTH = 1.5  # Nature style: thinner lines for cleaner look
```

**原因**：
- 更细的线条符合 Nature 风格的简洁美学
- 减少视觉噪音，突出数据本身
- 在高分辨率（600 DPI）下仍然清晰可见

#### ✅ 4. matplotlib rcParams 增强

**新增配置**：
```python
plt.rcParams.update({
    # 字体栈（支持中文回退）
    "font.sans-serif": [actual_font, "Arial", "Helvetica", "DejaVu Sans"],
    
    # Nature 风格：极简坐标轴
    "axes.spines.right": False,      # 移除右侧边框
    "axes.spines.top": False,        # 移除顶部边框
    "axes.linewidth": 0.8,           # 细边框
    
    # 图例样式
    "legend.frameon": False,         # 无框图例
    
    # 矢量输出设置
    "svg.fonttype": "none",          # SVG 中保持文本可编辑
    "pdf.fonttype": 42,              # PDF 中嵌入 TrueType 字体
})
```

**原因**：
1. **字体栈**: 确保中文支持的同时优先使用 Arial
2. **极简坐标轴**: Nature 风格要求只保留左侧和底部边框
3. **无框图例**: 减少视觉干扰
4. **可编辑文本**: SVG/PDF 输出可在 Illustrator 中后期编辑

### 📊 配置对比表

| 配置项 | 之前 | 现在 | 说明 |
|--------|------|------|------|
| **DPI** | 300 | **600** | Nature 期刊标准 |
| **字体** | Times New Roman | **Arial** | Nature 标准 sans-serif |
| **线宽** | 2.0 | **1.5** | 更简洁的视觉效果 |
| **坐标轴边框** | 四边都有 | **仅左+底** | Nature 极简风格 |
| **边框宽度** | 默认 | **0.8** | 细线条 |
| **图例边框** | 有框 | **无框** | 减少干扰 |
| **SVG 文本** | 路径化 | **可编辑** | 后期可修改 |
| **PDF 字体** | 默认 | **TrueType** | 嵌入可编辑字体 |

### 🎯 符合的标准

#### Nature Portfolio 要求
✅ 分辨率 ≥ 600 DPI  
✅ Sans-serif 字体（Arial/Helvetica）  
✅ 极简坐标轴设计  
✅ 可编辑的矢量输出  

#### nature-figure skill 推荐
✅ 字体大小 7pt（最终出版）  
✅ 细线宽（0.8-1.2）  
✅ 无顶部/右侧边框  
✅ 无框图例  
✅ SVG/PDF 文本可编辑  

### 💡 DPI 使用建议

| 用途 | 推荐 DPI | 说明 |
|------|---------|------|
| **Nature/Science 投稿** | 600 | 期刊标准要求 |
| **一般学术出版** | 600 | 高质量印刷 |
| **会议海报** | 300-600 | 根据海报尺寸调整 |
| **屏幕展示/PPT** | 150-300 | 平衡质量和文件大小 |
| **快速预览/调试** | 72-150 | 最小文件，最快速度 |

### 🔍 验证配置

```bash
# 检查默认配置
$ python -c "from plot import Plotter; p = Plotter(); print(f'Font: {p.config.font_family}'); print(f'DPI: {p.dpi}')"
Font: Arial
DPI: 600

# 运行测试
$ python tests/unit/test_heatmap.py
✓ Basic heatmap created successfully
✓ Heatmap with values created successfully
All tests passed!
```

### 📝 相关配置文件

- [config/presets/default_presets.py](config/presets/default_presets.py) - 默认配置预设
- [config/constants.py](config/constants.py) - 常量定义
- [plot/core.py](plot/core.py) - Plotter 主类
- [plot/strategies/line.py](plot/strategies/line.py) - 折线图策略
- [plot/strategies/scatter.py](plot/strategies/scatter.py) - 散点图策略
- [plot/strategies/heatmap.py](plot/strategies/heatmap.py) - 热力图策略

### 🚀 后续优化方向

可以考虑的进一步优化：

1. **配色方案优化**
   - 采用 nature-figure 推荐的 NMI pastel 调色板
   - 为不同图表类型提供专用配色

2. **布局模板**
   - 添加 Nature 单栏/双栏尺寸预设
   - 提供多面板组合模板

3. **统计标注自动化**
   - 自动添加显著性标记（*, **, ***）
   - 集成统计检验功能

4. **质量控制检查**
   - 自动检测字体嵌入
   - 验证颜色对比度
   - 检查分辨率是否达标

5. **批量处理优化**
   - 并行生成多张图表
   - 统一的图例和标注风格
   - 自动化命名规则

---

## 📦 打包与发布

### 清理旧文件

```bash
rm -rf build/ dist/ *.egg-info
```

### 重新打包

```bash
# 使用 setup.py
python setup.py sdist bdist_wheel

# 或使用现代构建工具
python -m build
```

生成的文件位于 `dist/` 目录：
- `plusml-data-visualization-0.1.0.tar.gz` (源码分发包)
- `plusml_data_visualization-0.1.0-py3-none-any.whl` (Wheel 包)

### 验证安装

```python
python -c "from config import FONT_FAMILY; print('Config:', FONT_FAMILY)"
python -c "from plot import Plotter; print('Plot module OK')"
```

预期输出：
```
Config: Times New Roman
Plot module OK
```

### 上传到 PyPI（可选）

```bash
# 安装 twine
pip install twine

# 上传
twine upload dist/*
```

## 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/plusml/plusml-data-visualization.git
cd plusml-data-visualization

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/
```

### 代码规范

- 遵循 PEP 8 代码风格
- 使用 Black 格式化代码
- 添加必要的类型注解
- 编写单元测试

## 致谢

感谢所有为本项目做出贡献的开发者和使用者！

---

**版本**: 0.1.0  
**最后更新**: 2026-05-16
