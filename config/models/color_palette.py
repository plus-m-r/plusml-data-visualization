from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ColorPalette:
    """Named color palette for scientific plotting."""

    name: str
    colors: Tuple[str, ...]
    description: str = ""
    use_case: str = ""
