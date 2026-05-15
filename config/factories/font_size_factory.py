"""Font size strategy factory."""

from __future__ import annotations

from ..models.font_size_policy import FontSizePolicy
from ..strategies import FixedSourceWidthStrategy, FinalWidthDirectStrategy, FontSizeStrategy


# Strategy registry (created once at module load)
_STRATEGY_REGISTRY: dict[FontSizePolicy, FontSizeStrategy] = {
    FontSizePolicy.FIXED_SOURCE_WIDTH: FixedSourceWidthStrategy(),
    FontSizePolicy.FINAL_WIDTH_DIRECT: FinalWidthDirectStrategy(),
}


def get_font_size_strategy(policy: FontSizePolicy) -> FontSizeStrategy:
    """Get font size strategy instance by policy.
    
    Args:
        policy: The font size policy to use.
        
    Returns:
        The corresponding strategy instance.
        
    Raises:
        KeyError: If policy is not registered.
    """
    return _STRATEGY_REGISTRY[policy]
