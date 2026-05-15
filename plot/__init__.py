"""PlusML Plotting Interface.

Usage:
    from plot import Plotter, config
    
    p = Plotter()
    p.line("data.csv", title="My Chart")
"""

from .core import Plotter

# Re-export config module for convenience
import config

__all__ = ["Plotter", "config"]
