"""Direct font size strategy (WYSIWYG)."""

from __future__ import annotations

from ...models.layout_mode import LayoutMode
from ...models.plot_config import PlotConfig


class FinalWidthDirectStrategy:
    """Use final publication font size directly (WYSIWYG canvas setup).
    
    This strategy uses the exact font size specified in the config,
    suitable for WYSIWYG workflows where the canvas matches final output.
    """

    def calc_plot_font_size_pt(self, config: PlotConfig, layout_mode: LayoutMode) -> float:
        _ = layout_mode
        return config.final_publication_font_pt
