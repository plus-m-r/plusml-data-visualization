"""PlusML Plotting Interface.

Usage:
    from plot import Plotter, config
    
    p = Plotter()
    p.line("data.csv", title="My Chart")
    p.scatter("data.csv", title="Scatter Plot")
    p.heatmap("matrix.csv", title="Heatmap")
"""

from .core import Plotter

# Re-export config module for convenience
import config

__all__ = ["Plotter", "config"]
