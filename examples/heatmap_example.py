#!/usr/bin/env python3
"""Example usage of the heatmap functionality."""

import sys
import os

# Add the project root to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from plot import Plotter

def example_heatmap_usage():
    """Demonstrate various ways to use the heatmap functionality."""
    
    print("PlusML Data Visualization - Heatmap Examples")
    print("=" * 50)
    
    # Create a plotter instance
    p = Plotter()
    
    # Example 1: Basic heatmap
    print("\n1. Creating a basic heatmap...")
    try:
        fig, ax = p.heatmap(
            "tests/data/test_heatmap.csv",
            title="Basic Heatmap Example",
            xlabel="Features",
            ylabel="Samples"
        )
        print("   ✓ Basic heatmap created: figures/Basic Heatmap Example.png")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
    
    # Example 2: Heatmap with custom colormap
    print("\n2. Creating heatmap with custom colormap...")
    try:
        fig, ax = p.heatmap(
            "tests/data/test_heatmap.csv",
            title="Custom Colormap",
            cmap="coolwarm",
            xlabel="Columns",
            ylabel="Rows"
        )
        print("   ✓ Custom colormap heatmap created: figures/Custom Colormap.png")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
    
    # Example 3: Heatmap with values displayed
    print("\n3. Creating heatmap with cell values...")
    try:
        fig, ax = p.heatmap(
            "tests/data/test_heatmap.csv",
            title="Heatmap with Values",
            show_values=True,
            value_format=".1f",
            cmap="viridis"
        )
        print("   ✓ Heatmap with values created: figures/Heatmap with Values.png")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
    
    # Example 4: Heatmap with different layout
    print("\n4. Creating heatmap with different layout...")
    try:
        fig, ax = p.heatmap(
            "tests/data/test_heatmap.csv",
            title="Wide Layout Heatmap",
            layout="1x2",
            cmap="plasma"
        )
        print("   ✓ Wide layout heatmap created: figures/Wide Layout Heatmap.png")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
    
    print("\n" + "=" * 50)
    print("All examples completed! Check the figures/ directory for output.")

if __name__ == "__main__":
    example_heatmap_usage()