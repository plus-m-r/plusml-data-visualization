"""Aspect ratio strategy factory."""

from __future__ import annotations

from ..models.aspect_ratio_policy import AspectRatioPolicy
from ..strategies import (
    FourToThreeStrategy,
    SixteenToNineStrategy,
    GoldenRatioStrategy,
    SquareStrategy,
    AspectRatioStrategy,
)


# Strategy registry (created once at module load)
_STRATEGY_REGISTRY: dict[AspectRatioPolicy, AspectRatioStrategy] = {
    AspectRatioPolicy.FOUR_TO_THREE: FourToThreeStrategy(),
    AspectRatioPolicy.SIXTEEN_TO_NINE: SixteenToNineStrategy(),
    AspectRatioPolicy.GOLDEN_RATIO: GoldenRatioStrategy(),
    AspectRatioPolicy.SQUARE: SquareStrategy(),
}


def get_aspect_ratio_strategy(policy: AspectRatioPolicy) -> AspectRatioStrategy:
    """Get aspect ratio strategy instance by policy.
    
    Args:
        policy: The aspect ratio policy to use.
        
    Returns:
        The corresponding strategy instance.
        
    Raises:
        KeyError: If policy is not registered.
    """
    return _STRATEGY_REGISTRY[policy]
