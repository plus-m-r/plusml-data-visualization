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
