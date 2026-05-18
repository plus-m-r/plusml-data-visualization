# PlusML 数据可视化库 - Nature-Figure 优化计划

## 📋 文档概述

本文档基于 **nature-figure skill** 的设计规范，详细规划了 PlusML 数据可视化库需要补充和完善的功能模块。通过系统性的优化，使本库达到 Nature 系列期刊的出版级标准。

**参考标准**：
- nature-figure skill (GitHub: Yuan1z0825/nature-skills)
- figures4papers (发表于 Nature Machine Intelligence)
- Nature Portfolio 作者指南

**最后更新**：2026-05-18  
**版本**：v0.2.0 规划

---

## 🎯 优化目标

### 核心目标
将 PlusML 从"基础绘图工具库"升级为"**Nature 级科研绘图流水线**"，实现：

1. ✅ **语义化配色系统** - 符合学术规范的智能配色
2. ✅ **专业图表细节** - 柱状图、折线图、热力图的精细化控制
3. ✅ **动态布局优化** - 自适应数据范围的智能缩放
4. ✅ **统计标注自动化** - 显著性检验与自动标注
5. ✅ **质量控制体系** - 自动检测与验证机制

### 设计原则
- **先定义结论，再生成代码** - 每个图表都服务于明确的科学主张
- **证据链思维** - 每个面板都有独特的证据价值，避免冗余
- **期刊规范优先** - 尺寸、字体、分辨率符合 Nature 要求
- **可复用工程化** - 代码结构化，配置集中管理

---

## 📊 当前状态评估

### ✅ 已实现功能

| 功能模块 | 状态 | 说明 |
|---------|------|------|
| 基础图表类型 | ✅ | 折线图、散点图、热力图、雷达图 |
| DPI 配置 | ✅ | 默认 600 DPI（Nature 标准） |
| 字体配置 | ✅ | Arial sans-serif 家族 |
| 线宽优化 | ✅ | 默认 1.5pt |
| 极简坐标轴 | ✅ | 移除顶部和右侧边框 |
| 无框图例 | ✅ | legend.frameon = False |
| SVG 可编辑文本 | ✅ | svg.fonttype = 'none' |
| PDF TrueType 嵌入 | ✅ | pdf.fonttype = 42 |
| 中文字体自动检测 | ✅ | 优先宋体/黑体 |
| 策略模式架构 | ✅ | 可扩展的绘图策略系统 |
| 布局模式 | ✅ | 1x1, 1x2, 1x3 |

### ❌ 缺失功能（按优先级排序）

| 优先级 | 功能模块 | 影响范围 | 实施难度 |
|--------|---------|---------|---------|
| 🔥 P0 | 语义化配色系统 | 所有图表 | ⭐⭐ |
| 🔥 P0 | 柱状图细节规范 | 柱状图 | ⭐⭐ |
| 🔥 P0 | 动态 Y 轴缩放 | 所有图表 | ⭐ |
| 🔥 P0 | 字体大小层级细化 | 所有图表 | ⭐⭐ |
| ⭐ P1 | 专用图例面板 | 多面板图 | ⭐⭐⭐ |
| ⭐ P1 | 热力图细节规范 | 热力图 | ⭐⭐ |
| ⭐ P1 | X 轴刻度抑制 | 柱状图 | ⭐ |
| ⭐ P1 | 统计标注自动化 | 所有图表 | ⭐⭐⭐ |
| 📈 P2 | 三层信息架构 | API 设计 | ⭐⭐⭐⭐ |
| 📈 P2 | 新图表类型扩展 | 功能扩展 | ⭐⭐⭐ |
| 📈 P2 | GridSpec 多面板布局 | 布局系统 | ⭐⭐⭐ |
| 📈 P2 | 质量控制检查 | 质量保障 | ⭐⭐⭐⭐ |

---

## 🚀 Phase 1: 高优先级优化（立即实施）

### 1.1 语义化配色系统（Semantic Color Palette）

**现状问题**：
- 当前色盘缺乏语义规则
- 同一方法在不同图中可能使用不同颜色
- 缺少 NMI Pastel 等专业调色板

**实施方案**：

#### a) 创建语义化色盘配置文件

```python
# config/colors/semantic_palette.py

SEMANTIC_PALETTE = {
    # 核心方法/实验组
    "blue_main":      "#0F4D92",   # 深蓝色 - 主要方法
    "blue_secondary": "#3775BA",   # 中蓝色 - 次要方法
    
    # 阳性/改进变体（浅→深）
    "green_1": "#DDF3DE",
    "green_2": "#AADCA9", 
    "green_3": "#8BCF8B",
    
    # 基线/对照（浅→深）
    "red_1":      "#F6CFCB",
    "red_2":      "#E9A6A1",
    "red_strong": "#B64342",
    
    # 中性支持色
    "neutral_light": "#CFCECE",
    "neutral_mid":   "#767676",
    "neutral_dark":  "#4D4D4D",
    "neutral_black": "#272727",
    
    # 强调色（谨慎使用）
    "gold":   "#FFD700",
    "teal":   "#42949E",
    "violet": "#9A4D8E",
}

# NMI Pastel 调色板（推荐用于密集多面板图）
NMI_PASTEL_PALETTE = {
    "baseline_dark": "#484878",
    "baseline_mid":  "#7884B4",
    "baseline_soft": "#B4C0E4",
    "ours_tiny":     "#E4E4F0",
    "ours_base":     "#E4CCD8",
    "ours_large":    "#F0C0CC",
    "delta_up":      "#2E9E44",  # 增益箭头
    "delta_down":    "#E53935",  # 下降箭头
}

# 默认颜色顺序
DEFAULT_COLOR_ORDER = [
    "#0F4D92",   # blue_main
    "#8BCF8B",   # green_3
    "#B64342",   # red_strong
    "#42949E",   # teal
    "#9A4D8E",   # violet
]
```

#### b) 统一色系规则引擎

```python
# config/colors/color_rules.py

class ColorRuleEngine:
    """语义化配色规则引擎"""
    
    @staticmethod
    def assign_colors(methods: list, palette_type: str = "semantic") -> dict:
        """
        为方法分配颜色，确保同一方法始终使用相同色系
        
        Rules:
        1. 基线方法使用冷色系（blue/purple）
        2. 提出的方法使用暖色系（red/orange）
        3. 消融实验使用单一颜色 + 不同透明度
        4. 禁止在不同面板中为同一方法映射不同色相
        """
        pass
    
    @staticmethod
    def get_ablation_colors(base_color: tuple, n_variants: int) -> list:
        """生成消融实验的颜色序列（单色 + 不同透明度）"""
        alphas = np.linspace(0.2, 1.0, n_variants)
        return [(base_color[0], base_color[1], base_color[2], a) for a in alphas]
```

#### c) 集成到 PlotConfig

```python
# config/models/plot_config.py

@dataclass(frozen=True)
class PlotConfig:
    # ... 现有字段 ...
    
    # 新增：配色规则
    color_palette_type: str = "semantic"  # "semantic" | "nmi_pastel" | "classic"
    enforce_unified_family: bool = True   # 强制统一色系
```

**验收标准**：
- ✅ 提供至少 3 套专业调色板（Semantic, NMI Pastel, Classic）
- ✅ 实现统一色系规则引擎
- ✅ 支持消融实验的透明度编码
- ✅ 在 README 中提供配色使用指南

**预计工作量**：2-3 天

---

### 1.2 柱状图细节规范（Bar Chart Enhancement）

**现状问题**：
- 缺少黑色边框（edgecolor）
- 无柱内数值标注
- 误差棒样式不统一
- 缺少打印安全的阴影编码

**实施方案**：

#### a) 增强柱状图策略

```python
# plot/strategies/bar.py

class BarChartStrategy(DrawStrategy):
    def draw_bar(
        self,
        data_files: list,
        title: str = "",
        layout: str = "1x1",
        save_path: str = None,
        # 新增参数
        show_values: bool = True,           # 显示柱内数值
        value_fontsize: int = 32,           # 数值字体大小
        edge_color: str = "black",          # 边框颜色
        edge_width: float = 1.5,            # 边框宽度
        error_capsize: int = 5,             # 误差棒帽大小
        use_hatch: bool = False,            # 使用阴影（打印安全）
        hatch_patterns: list = None,        # 阴影图案
        suppress_xticks: bool = False,      # 抑制 x 轴刻度
    ):
        """绘制符合 Nature 标准的柱状图"""
        
        # 1. 应用基础样式
        self._apply_style()
        
        # 2. 创建图形
        fig, ax = self._create_figure(layout)
        
        # 3. 绘制柱状图
        bars = ax.bar(
            x_positions,
            values,
            yerr=std_values if has_error else None,
            capsize=error_capsize,
            color=colors,
            label=method_names,
            edgecolor=edge_color,      # ✅ 锐利分离
            linewidth=edge_width,
        )
        
        # 4. 添加阴影（打印安全）
        if use_hatch:
            hatches = hatch_patterns or ['/', '\\', '.', 'x', 'o']
            for bar, hatch in zip(bars, hatches):
                bar.set_hatch(hatch)
        
        # 5. 柱内数值标注
        if show_values:
            self._annotate_bars(ax, bars, values, value_fontsize)
        
        # 6. 抑制 x 轴刻度（如果图例已命名）
        if suppress_xticks:
            ax.set_xticks([])
        
        # 7. 保存
        self._save_figure(fig, save_path, title)
        
        return fig, ax
    
    def _annotate_bars(self, ax, bars, values, fontsize):
        """在柱内标注数值，自动选择文本颜色"""
        for bar, value in zip(bars, values):
            # 计算背景色亮度
            bar_color = bar.get_facecolor()
            luminance = 0.299 * bar_color[0] + 0.587 * bar_color[1] + 0.114 * bar_color[2]
            
            # 根据亮度选择文本颜色
            textcolor = 'white' if luminance < 0.5 else 'black'
            
            # 标注位置：柱顶下方 10%
            ax.text(
                bar.get_x() + bar.get_width()/2,
                bar.get_height() - (bar.get_height() * 0.10),
                f'{value:.2f}',
                ha='center',
                va='bottom',
                fontsize=fontsize,
                color=textcolor,
                fontweight='bold'
            )
```

#### b) 误差棒样式标准化

```python
# config/constants.py

# 误差棒样式
ERROR_BAR_STYLE = {
    'elinewidth': 2,      # 误差线宽度
    'capthick': 2,        # 帽厚度
    'capsize': 15,        # 帽大小
}
```

**验收标准**：
- ✅ 支持柱内数值标注（自动黑白对比）
- ✅ 默认添加黑色边框（1.5pt）
- ✅ 统一的误差棒样式
- ✅ 可选的阴影编码（打印安全）
- ✅ 可选的 x 轴刻度抑制

**预计工作量**：2 天

---

### 1.3 动态 Y 轴缩放（Dynamic Y-axis Scaling）

**现状问题**：
- 可能使用固定的 0-100 范围
- 当数据在窄范围内时，浪费垂直空间

**实施方案**：

#### a) 自动计算最优 Y 轴范围

```python
# plot/core.py

class Plotter:
    def _optimize_y_limits(self, ax, data_values, margin_ratio=0.1):
        """
        动态优化 Y 轴范围
        
        Args:
            ax: matplotlib axes 对象
            data_values: 数据值数组
            margin_ratio: 边距比例（默认 10%）
        """
        data_min = np.min(data_values)
        data_max = np.max(data_values)
        data_range = data_max - data_min
        
        # 计算边距
        margin = data_range * margin_ratio
        
        # 设置范围（确保包含 0 如果数据都为正）
        y_min = min(0, data_min - margin) if np.all(data_values >= 0) else data_min - margin
        y_max = data_max + margin
        
        ax.set_ylim([y_min, y_max])
```

#### b) 在各绘图策略中集成

```python
# 在 line.py, scatter.py, bar.py 等策略中调用
self._optimize_y_limits(ax, y_values, margin_ratio=0.1)
```

**验收标准**：
- ✅ 自动收紧 Y 轴范围到数据区间
- ✅ 保留 10% 边距避免贴边
- ✅ 对全正数据保持从 0 开始
- ✅ 可通过参数自定义边距比例

**预计工作量**：0.5 天

---

### 1.4 字体大小层级细化（Font Size Hierarchy）

**现状问题**：
- 当前使用统一的字号策略（基于布局模式）
- 缺少针对不同元素的精细控制

**实施方案**：

#### a) 定义字体大小层级常量

```python
# config/constants.py

# Nature 风格字体大小层级（针对最终出版宽度）
FONT_SIZE_HIERARCHY = {
    # 基础字号（密集多面板图）
    "base": 7,              # 正文文本
    
    # 元素特定字号
    "axis_label": 9,        # 轴标签
    "tick_label": 8,        # 刻度标签
    "title": 10,            # 标题
    "legend": 8,            # 图例文本
    "annotation": 9,        # 注释文本
    
    # 大面板覆盖值（figsize > 28in）
    "large_panel": {
        "base": 24,
        "axis_label": 32,
        "tick_label": 20,
        "title": 36,
        "legend": 28,
        "annotation": 32,
    },
    
    # 紧凑子图覆盖值
    "compact_panel": {
        "base": 15,
        "axis_label": 16,
        "tick_label": 14,
        "title": 18,
        "legend": 14,
        "annotation": 16,
    },
}

# 坐标轴线宽对应关系
AXES_LINEWIDTH_BY_CONTEXT = {
    "journal_final": 0.8,   # 期刊最终图
    "large_panel": 3,       # 大面板
    "compact_panel": 2,     # 紧凑图
}
```

#### b) 增强 PlotConfig

```python
# config/models/plot_config.py

@dataclass(frozen=True)
class PlotConfig:
    # ... 现有字段 ...
    
    # 新增：字体大小层级
    font_size_context: str = "journal_final"  # "journal_final" | "large_panel" | "compact_panel"
    custom_font_sizes: dict = None            # 自定义覆盖值
```

#### c) 在绘图策略中应用

```python
# plot/strategies/base.py

class DrawStrategy:
    def _apply_font_hierarchy(self, ax, context="journal_final"):
        """应用字体大小层级"""
        hierarchy = FONT_SIZE_HIERARCHY.get(context, FONT_SIZE_HIERARCHY["journal_final"])
        
        # 设置轴标签
        ax.xaxis.label.set_size(hierarchy["axis_label"])
        ax.yaxis.label.set_size(hierarchy["axis_label"])
        
        # 设置刻度标签
        ax.tick_params(axis='both', which='major', labelsize=hierarchy["tick_label"])
        
        # 设置标题
        if ax.get_title():
            ax.title.set_size(hierarchy["title"])
        
        # 设置图例
        legend = ax.get_legend()
        if legend:
            for text in legend.get_texts():
                text.set_fontsize(hierarchy["legend"])
```

**验收标准**：
- ✅ 提供 3 种预设上下文（journal_final, large_panel, compact_panel）
- ✅ 支持自定义字体大小覆盖
- ✅ 自动应用到所有文本元素
- ✅ 与 axes.linewidth 联动

**预计工作量**：1.5 天

---

## 🌟 Phase 2: 中优先级优化（近期实施）

### 2.1 专用图例面板（Dedicated Legend Panel）

**现状问题**：
- 每个子图都重复图例，占用空间
- 多图时视觉混乱

**实施方案**：

#### a) 创建图例面板工具函数

```python
# plot/utils/legend_panel.py

def create_legend_panel(fig, handles, labels, position="right", fontsize=8):
    """
    创建专用的图例面板
    
    Args:
        fig: matplotlib figure
        handles: 图例句柄列表
        labels: 图例标签列表
        position: 位置 ("right" | "top" | "bottom")
        fontsize: 字体大小
    
    Returns:
        ax_legend: 图例轴的引用
    """
    if position == "right":
        # 在右侧添加图例面板
        ax_legend = fig.add_axes([0.92, 0.1, 0.06, 0.8])
    elif position == "top":
        # 在顶部添加图例面板
        ax_legend = fig.add_axes([0.1, 0.92, 0.8, 0.06])
    
    # 添加图例
    legend = ax_legend.legend(
        handles, labels,
        fontsize=fontsize,
        loc='center',
        frameon=False  # 无框
    )
    
    # 关闭坐标轴
    ax_legend.set_axis_off()
    
    return ax_legend
```

#### b) 在多面板绘图中集成

```python
# 修改 Plotter 的多曲线 API
def line(self, data_files: list, ..., show_shared_legend: bool = True):
    """
    绘制多曲线图
    
    Args:
        show_shared_legend: 是否使用共享图例面板
    """
    if show_shared_legend and len(data_files) > 1:
        # 创建 n+1 个子图，最后一个用于图例
        n_curves = len(data_files)
        gs = gridspec.GridSpec(1, n_curves + 1, width_ratios=[1]*n_curves + [0.3])
        
        # 绘制各曲线
        for i, data_file in enumerate(data_files):
            ax = fig.add_subplot(gs[0, i])
            # ... 绘制逻辑 ...
        
        # 创建图例面板
        ax_legend = fig.add_subplot(gs[0, n_curves])
        ax_legend.legend(all_handles, all_labels, frameon=False)
        ax_legend.set_axis_off()
```

**验收标准**：
- ✅ 支持右侧、顶部、底部图例面板
- ✅ 自动收集所有曲线的句柄和标签
- ✅ 图例无框，视觉上更安静
- ✅ 兼容现有的单图例模式

**预计工作量**：2 天

---

### 2.2 热力图细节规范（Heatmap Enhancement）

**现状问题**：
- 缺少发散色图的按列归一化
- NaN 单元格处理不完善
- 缺少框架和刻度优化

**实施方案**：

#### a) 增强热力图策略

```python
# plot/strategies/heatmap.py

class HeatmapDrawStrategy(DrawStrategy):
    def draw_heatmap(
        self,
        data_file: str,
        title: str = "",
        layout: str = "1x1",
        save_path: str = None,
        # 新增参数
        cmap_type: str = "diverging",     # "sequential" | "diverging"
        normalize_per_column: bool = True, # 按列归一化
        show_nan_as_white: bool = True,    # NaN 显示为白色
        remove_frame: bool = True,         # 移除框架
        suppress_ticks: bool = True,       # 抑制刻度线
        annotate_cells: bool = False,      # 标注单元格数值
        auto_text_color: bool = True,      # 自动文本颜色
    ):
        """绘制符合 Nature 标准的热力图"""
        
        # 1. 加载数据
        data = self._load_data(data_file)
        
        # 2. 处理 NaN
        if show_nan_as_white:
            cmap = plt.cm.RdBu_r if cmap_type == "diverging" else plt.cm.viridis
            cmap.set_bad(color='white')
        
        # 3. 归一化
        if normalize_per_column:
            # 按列计算最小最大值
            col_mins = data.min(axis=0)
            col_maxs = data.max(axis=0)
            norm = mpl.colors.Normalize(vmin=col_mins.min(), vmax=col_maxs.max())
        else:
            norm = mpl.colors.Normalize(vmin=data.min(), vmax=data.max())
        
        # 4. 绘制热力图
        im = ax.imshow(data, cmap=cmap, norm=norm, aspect='auto')
        
        # 5. 移除框架
        if remove_frame:
            ax.set_frame_on(False)
        
        # 6. 抑制刻度线（保留标签）
        if suppress_ticks:
            ax.tick_params(axis='x', which='both', bottom=False, top=False, length=0)
            ax.tick_params(axis='y', which='both', left=False, right=False, length=0)
        
        # 7. 标注单元格
        if annotate_cells:
            self._annotate_heatmap_cells(ax, data, cmap, norm, auto_text_color)
        
        # 8. 添加颜色条
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.ax.tick_params(labelsize=7)
        
        # 9. 保存
        self._save_figure(fig, save_path, title)
        
        return fig, ax
    
    def _annotate_heatmap_cells(self, ax, data, cmap, norm, auto_color):
        """标注热力图单元格，自动选择文本颜色"""
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                value = data[i, j]
                if np.isnan(value):
                    continue
                
                # 获取单元格颜色
                rgba = cmap(norm(value))
                
                # 计算亮度
                luminance = 0.299 * rgba[0] + 0.587 * rgba[1] + 0.114 * rgba[2]
                text_color = 'white' if luminance < 0.5 else 'black'
                
                # 标注
                ax.text(j, i, f'{value:.2f}',
                       ha='center', va='center',
                       fontsize=6, color=text_color)
```

**验收标准**：
- ✅ 支持按列归一化
- ✅ NaN 单元格显示为白色
- ✅ 可选移除框架和刻度线
- ✅ 智能单元格标注（自动黑白对比）
- ✅ 支持发散色图和顺序色图

**预计工作量**：1.5 天

---

### 2.3 X 轴刻度抑制（X-tick Suppression）

**现状问题**：
- 当图例已命名方法时，x 轴刻度冗余

**实施方案**：

#### a) 在柱状图中添加参数

```python
# plot/strategies/bar.py

def draw_bar(self, ..., suppress_xticks: bool = False):
    """
    Args:
        suppress_xticks: 是否抑制 x 轴刻度（当图例已命名时）
    """
    # ... 绘制逻辑 ...
    
    if suppress_xticks:
        ax.set_xticks([])
        # 可选：添加面板标题代替
        if title:
            ax.set_title(title, fontsize=9, pad=10)
```

**验收标准**：
- ✅ 可选抑制 x 轴刻度
- ✅ 与图例配合使用
- ✅ 保持面板标题清晰

**预计工作量**：0.5 天

---

### 2.4 统计标注自动化（Statistical Annotation）

**现状问题**：
- 缺少自动显著性检验
- 手动添加 *, **, *** 标记繁琐

**实施方案**：

#### a) 创建统计工具模块

```python
# plot/utils/statistics.py

from scipy import stats

class StatisticalAnnotator:
    """统计标注器"""
    
    @staticmethod
    def compute_significance(group1, group2, test_type="ttest"):
        """
        计算两组数据的显著性
        
        Args:
            group1, group2: 数据数组
            test_type: 检验类型 ("ttest" | "anova" | "mannwhitney")
        
        Returns:
            p_value: p 值
            annotation: 标注字符串 ("***" | "**" | "*" | "ns")
        """
        if test_type == "ttest":
            _, p_value = stats.ttest_ind(group1, group2, nan_policy='omit')
        elif test_type == "mannwhitney":
            _, p_value = stats.mannwhitneyu(group1, group2, nan_policy='omit')
        
        # 确定标注
        if p_value < 0.001:
            annotation = '***'
        elif p_value < 0.01:
            annotation = '**'
        elif p_value < 0.05:
            annotation = '*'
        else:
            annotation = 'ns'  # not significant
        
        return p_value, annotation
    
    @staticmethod
    def add_bracket_annotation(ax, x1, x2, y, annotation, height=0.05):
        """
        添加括号标注
        
        Args:
            ax: matplotlib axes
            x1, x2: 括号两端 x 坐标
            y: 括号高度位置
            annotation: 标注文本
            height: 括号高度
        """
        # 绘制括号
        ax.plot([x1, x1, x2, x2], [y, y+height, y+height, y], 
               color='black', linewidth=1)
        
        # 添加文本
        ax.text((x1 + x2) / 2, y + height + 0.02, annotation,
               ha='center', va='bottom', fontsize=8, fontweight='bold')
```

#### b) 集成到柱状图策略

```python
# plot/strategies/bar.py

def draw_bar(self, ..., add_significance: bool = False, significance_pairs: list = None):
    """
    Args:
        add_significance: 是否添加显著性标注
        significance_pairs: 需要检验的数据对 [(group1_idx, group2_idx), ...]
    """
    # ... 绘制柱状图 ...
    
    if add_significance and significance_pairs:
        annotator = StatisticalAnnotator()
        
        for idx1, idx2 in significance_pairs:
            # 提取数据
            group1 = data[idx1]
            group2 = data[idx2]
            
            # 计算显著性
            p_value, annotation = annotator.compute_significance(group1, group2)
            
            # 添加括号标注
            x1, x2 = idx1, idx2
            y = max(values[idx1], values[idx2]) + 0.1
            annotator.add_bracket_annotation(ax, x1, x2, y, annotation)
```

**验收标准**：
- ✅ 支持 t-test 和 Mann-Whitney U 检验
- ✅ 自动计算 p 值和标注（*, **, ***, ns）
- ✅ 绘制括号标注线
- ✅ 可指定需要检验的数据对

**预计工作量**：2-3 天

---

## 📈 Phase 3: 低优先级优化（长期规划）

### 3.1 三层信息架构面板设计

**概念**：将多面板图分为三个层次
- **概览层**：展示数据全貌
- **偏差层**：解释每组特征
- **关系层**：展示变量关联

**实施难点**：需要重构 API 以支持面板级别的语义定义

**建议方案**：
```python
# 未来的 API 设计（概念性）
p.multi_panel(
    panels=[
        {"type": "overview", "data": "...", "chart": "bar"},
        {"type": "deviation", "data": "...", "chart": "box"},
        {"type": "relationship", "data": "...", "chart": "scatter"},
    ],
    layout="1x3"
)
```

**预计工作量**：5-7 天（需 API 重构）

---

### 3.2 新图表类型扩展

**待添加的图表类型**：

1. **分布图（Distribution）**
   - 直方图（Histogram）
   - 小提琴图（Violin Plot）
   - 箱线图（Box Plot）

2. **森林图（Forest Plot）**
   - Meta 分析风格
   - 置信区间展示

3. **面积图（Area Plot）**
   - 堆叠面积图
   - 填充不确定性带

4. **图像板（Image Plate）**
   - 多图像拼接
   - 荧光通道叠加

5. **网络图（Network Plot）**
   - 节点-边图
   - 矩阵布局

**实施建议**：按需求优先级逐个实现，每个图表类型 2-3 天

---

### 3.3 GridSpec 多面板布局

**现状**：仅支持简单的 1x1, 1x2, 1x3 布局

**目标**：支持灵活的网格规格布局

**实施方案**：
```python
# 未来的 API
p.custom_layout(
    grid_spec=(2, 3),  # 2行3列
    width_ratios=[1, 1, 0.5],
    height_ratios=[1, 1],
    panels=[
        {"position": (0, :2), "chart": "line"},  # 跨越两列
        {"position": (0, 2), "chart": "legend"},  # 图例面板
        {"position": (1, :), "chart": "bar"},     # 跨越整行
    ]
)
```

**预计工作量**：3-4 天

---

### 3.4 质量控制检查系统

**功能清单**：

1. **字体嵌入检测**
   ```python
   def check_font_embedding(pdf_path):
       """检查 PDF 中字体是否正确嵌入"""
       pass
   ```

2. **颜色对比度验证（WCAG 标准）**
   ```python
   def check_color_contrast(color1, color2, level="AA"):
       """验证颜色对比度是否符合 WCAG 标准"""
       pass
   ```

3. **分辨率检查**
   ```python
   def check_resolution(image_path, min_dpi=600):
       """检查图像分辨率是否达标"""
       pass
   ```

4. **SVG 文本可编辑性检测**
   ```python
   def check_svg_editable(svg_path):
       """检查 SVG 中文本是否为 <text> 节点而非路径"""
       pass
   ```

5. **冗余面板检测**
   ```python
   def detect_redundant_panels(panels):
       """检测是否有两个面板回答相同的科学问题"""
       # 基于元数据分析
       pass
   ```

**实施建议**：作为独立的质量控制模块，在导出前自动运行

**预计工作量**：5-7 天

---

## 📅 实施时间表

### Phase 1: 高优先级（第 1-2 周）

| 任务 | 预计天数 | 负责人 | 状态 |
|------|---------|--------|------|
| 语义化配色系统 | 2-3 天 | - | ⏳ 待开始 |
| 柱状图细节规范 | 2 天 | - | ⏳ 待开始 |
| 动态 Y 轴缩放 | 0.5 天 | - | ⏳ 待开始 |
| 字体大小层级细化 | 1.5 天 | - | ⏳ 待开始 |
| **Phase 1 小计** | **6-7 天** | | |

### Phase 2: 中优先级（第 3-4 周）

| 任务 | 预计天数 | 负责人 | 状态 |
|------|---------|--------|------|
| 专用图例面板 | 2 天 | - | ⏳ 待开始 |
| 热力图细节规范 | 1.5 天 | - | ⏳ 待开始 |
| X 轴刻度抑制 | 0.5 天 | - | ⏳ 待开始 |
| 统计标注自动化 | 2-3 天 | - | ⏳ 待开始 |
| **Phase 2 小计** | **6-7 天** | | |

### Phase 3: 低优先级（第 5-8 周）

| 任务 | 预计天数 | 负责人 | 状态 |
|------|---------|--------|------|
| 三层信息架构 | 5-7 天 | - | ⏳ 待开始 |
| 新图表类型（5种） | 10-15 天 | - | ⏳ 待开始 |
| GridSpec 布局 | 3-4 天 | - | ⏳ 待开始 |
| 质量控制检查 | 5-7 天 | - | ⏳ 待开始 |
| **Phase 3 小计** | **23-33 天** | | |

**总计**：约 **35-47 个工作日**（7-9 周）

---

## ✅ 验收标准总览

### 功能性验收

- [ ] 提供至少 3 套专业调色板
- [ ] 实现统一色系规则引擎
- [ ] 柱状图支持数值标注、边框、阴影
- [ ] 所有图表支持动态 Y 轴缩放
- [ ] 提供 3 种字体大小层级预设
- [ ] 支持专用图例面板
- [ ] 热力图支持按列归一化和智能标注
- [ ] 支持统计显著性自动标注
- [ ] 新增至少 2 种图表类型

### 质量验收

- [ ] 所有输出符合 Nature 期刊标准
- [ ] SVG 文本可编辑（非路径化）
- [ ] PDF 字体正确嵌入
- [ ] 默认 600 DPI 高分辨率
- [ ] 通过质量控制检查套件

### 文档验收

- [ ] 更新 README 包含新功能说明
- [ ] 提供配色使用指南
- [ ] 提供图表类型选择指南
- [ ] 提供 Nature 风格最佳实践文档
- [ ] 每个新功能都有示例代码

### 测试验收

- [ ] 单元测试覆盖率 > 80%
- [ ] 集成测试覆盖所有图表类型
- [ ] 视觉回归测试（对比参考图）
- [ ] 性能测试（批量生成效率）

---

## 📚 参考资料

1. **nature-figure skill**
   - GitHub: https://github.com/Yuan1z0825/nature-skills
   - SKILL.md: `skills/nature-figure/SKILL.md`
   - Design Theory: `skills/nature-figure/references/design-theory.md`
   - API Reference: `skills/nature-figure/references/api.md`

2. **figures4papers**
   - GitHub: https://github.com/ChenLiu-1996/figures4papers
   - 发表于 Nature Machine Intelligence

3. **Nature Portfolio 作者指南**
   - https://www.nature.com/nature-portfolio/editorial-policies/formatting-guide

4. **Matplotlib 文档**
   - rcParams: https://matplotlib.org/stable/tutorials/introductory/customizing.html
   - savefig: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html

5. **WCAG 颜色对比度标准**
   - https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html

---

## 🔄 更新日志

| 日期 | 版本 | 更新内容 | 作者 |
|------|------|---------|------|
| 2026-05-18 | v0.1.0 | 初始版本，基于 nature-figure skill 分析 | Lingma |

---

## 💡 后续建议

1. **渐进式实施**：按优先级分阶段实施，每完成一个 Phase 就发布一个版本
2. **用户反馈**：在每个 Phase 完成后收集用户反馈，调整后续计划
3. **社区贡献**：开放部分模块供社区贡献（如新图表类型）
4. **持续对标**：定期查看 Nature 最新发表论文，更新设计规范
5. **自动化测试**：建立视觉回归测试系统，确保优化不破坏现有功能

---

**结语**：本优化计划旨在将 PlusML 数据可视化库打造成真正的 Nature 级科研绘图工具。通过系统性的功能补充和质量提升，帮助用户更高效地产出符合顶级期刊标准的学术图表。

**下一步行动**：从 Phase 1 的语义化配色系统开始实施。
