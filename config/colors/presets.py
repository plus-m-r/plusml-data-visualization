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
