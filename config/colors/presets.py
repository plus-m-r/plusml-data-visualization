from __future__ import annotations

from ..models import ColorPalette


CLASSIC_ACADEMIC_BLUE = ColorPalette(
    name="classic_academic_blue",
    colors=("#0077BB", "#33BBEE", "#CC3311", "#009988", "#EE7733"),
    description="稳妥的学术蓝系，适合大多数论文图表。",
    use_case="柱状图、折线图、散点图等通用图表。",
)

NATURAL_FRIENDLY = ColorPalette(
    name="natural_friendly",
    colors=("#7A947E", "#738BA8", "#C8B9A7", "#444444"),
    description="温和、不刺眼的自然系配色。",
    use_case="分子结构、网络关系、工程示意图。",
)

DISTINCT_QUALITATIVE = ColorPalette(
    name="distinct_qualitative",
    colors=("#F8DE40", "#ABAEAE", "#68C3F0", "#1057D1"),
    description="区分度高的定性色板。",
    use_case="多组数据对比、多组学联合分析。",
)

MACARON = ColorPalette(
    name="macaron",
    colors=("#A1C9F4", "#FFB482", "#8DE5A1", "#B39FDB"),
    description="低饱和的马卡龙风格配色。",
    use_case="系统框架图、概念模型图、流程示意图。",
)

BLUE_ORANGE_SAFE = ColorPalette(
    name="blue_orange_safe",
    colors=("#DECA38", "#D09BBF"),
    description="双色安全模板，避免红绿冲突。",
    use_case="两组数据对比。",
)

BLUE_YELLOW_SAFE = ColorPalette(
    name="blue_yellow_safe",
    colors=("#0077BB", "#EE7733", "#F8DE40"),
    description="蓝黄橙安全组合，兼顾可读性与辨识度。",
    use_case="中等复杂度的对比图。",
)

BLUE_PURPLE_SAFE = ColorPalette(
    name="blue_purple_safe",
    colors=("#C586DA", "#5A5AB6", "#9C81E5"),
    description="高区分度的蓝紫系组合。",
    use_case="三组对比数据。",
)

TWO_COLOR = ColorPalette(
    name="two_color",
    colors=("#DECA38", "#D09BBF"),
    description="简洁双色方案。",
    use_case="两组数据或双通道可视化。",
)

TRI_COLOR = ColorPalette(
    name="tri_color",
    colors=("#C586DA", "#5A5AB6", "#9C81E5"),
    description="三色参考方案。",
    use_case="三组数据或三阶段展示。",
)

# ============================================================================
# Nature-Figure Semantic Color Palettes (Phase 1 Optimization)
# Based on nature-figure skill and figures4papers design standards
# ============================================================================

SEMANTIC_NATURE = ColorPalette(
    name="semantic_nature",
    colors=(
        "#0F4D92",   # blue_main - 核心方法/实验组（深蓝色）
        "#8BCF8B",   # green_3 - 阳性/改进变体（绿色）
        "#B64342",   # red_strong - 基线/对照（红色）
        "#42949E",   # teal - 强调色（青色）
        "#9A4D8E",   # violet - 强调色（紫色）
        "#CFCECE",   # neutral_light - 中性支持色（浅灰）
    ),
    description="Nature 风格语义化配色系统。蓝色=主要方法，绿色=阳性变体，红色=基线对照。遵循统一色系规则，同一方法在不同面板中保持相同色相。",
    use_case="多方法对比、消融实验、基线与改进方法对比。适用于 Nature/Science 等顶级期刊投稿。",
)

NMI_PASTEL = ColorPalette(
    name="nmi_pastel",
    colors=(
        "#484878",   # baseline_dark - 基线深色
        "#7884B4",   # baseline_mid - 基线中色
        "#B4C0E4",   # baseline_soft - 基线浅色
        "#E4E4F0",   # ours_tiny - 提出的方法（微小变体）
        "#E4CCD8",   # ours_base - 提出的方法（基础版本）
        "#F0C0CC",   # ours_large - 提出的方法（大型变体）
    ),
    description="Nature Machine Intelligence 风格的柔和 pastel 调色板。冷色系用于基线，暖色系用于提出的方法。适合密集多面板图，保持视觉一致性。",
    use_case="密集多面板复合图、多指标对比、消融实验系列图。推荐用于 NMI 风格页面。",
)

ABLATION_SINGLE = ColorPalette(
    name="ablation_single",
    colors=(
        "#0F4D92",   # 单一蓝色，通过透明度变化区分变体
    ),
    description="单色消融实验配色。使用单一颜色配合不同透明度（alpha 0.2-1.0）表示方法的各个组件变体。alpha=1.0 为完整方法，alpha=0.2 为最小变体。",
    use_case="消融实验、组件分析、参数敏感性研究。需要在代码中手动设置 alpha 值。",
)
