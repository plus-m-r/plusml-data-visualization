from __future__ import annotations

from typing import Mapping

from ..models.font_size_policy import FontSizePolicy
from .base import FontSizeStrategy
from .direct import FinalWidthDirectStrategy
from .fixed_width import FixedSourceWidthStrategy


STRATEGY_BY_POLICY: Mapping[FontSizePolicy, FontSizeStrategy] = {
    FontSizePolicy.FIXED_SOURCE_WIDTH: FixedSourceWidthStrategy(),
    FontSizePolicy.FINAL_WIDTH_DIRECT: FinalWidthDirectStrategy(),
}
