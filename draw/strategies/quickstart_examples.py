"""Quick start examples for graph visualization.

Run this file to see various usage patterns of GraphVizStrategy.
"""

from pathlib import Path
from draw.strategies import GraphVizStrategy
from tests.data_pipeline import RawGraphStreamDataset, PyGGraphStreamDataset
import networkx as nx


def example_1_basic_dict():
	"""Example 1: Basic visualization from dict."""
	print("\n" + "="*60)
	print("Example 1: Basic Dict Visualization")
	print("="*60)
	
	data_root = Path(__file__).parent.parent.parent / "tests" / "data" / "ogbg_ppa"
	ds = RawGraphStreamDataset(data_root=data_root, split="train", max_graphs=1)
	sample = next(iter(ds))
	
	viz = GraphVizStrategy()
	viz.load_from_dict(sample)
	viz.compute_layout(layout_type="spring", k=1.5)
	viz.encode_node_size(encoding_type="degree", scale=30)
	viz.encode_node_color(encoding_type="degree", cmap="cool")
	viz.encode_edge_width(encoding_type="weight", scale=2)
	
	fig, ax = viz.draw(
		figsize=(12, 10),
		title=f"OGBG-PPA (nodes={sample['num_nodes']}, edges={len(sample['edge_index'][0])})",
		show_labels=False
	)
	output = Path(__file__).parent / "outputs" / "example1_basic.png"
	output.parent.mkdir(exist_ok=True, parents=True)
	viz.save(fig, str(output))
	print(f"✓ Saved to {output}")


def example_2_pyg_data():
	"""Example 2: PyG Data visualization."""
	print("\n" + "="*60)
	print("Example 2: PyG Data Visualization")
	print("="*60)
	
	try:
		data_root = Path(__file__).parent.parent.parent / "tests" / "data" / "ogbg_ppa"
		ds = PyGGraphStreamDataset(data_root=data_root, split="valid", max_graphs=1)
		sample = next(iter(ds))
		
		viz = GraphVizStrategy()
		viz.load_from_pyg_data(sample)
		viz.compute_layout(layout_type="kamada_kawai")
		viz.encode_node_size(encoding_type="degree", scale=35)
		viz.encode_node_color(encoding_type="degree", cmap="plasma")
		viz.encode_edge_width(encoding_type="fixed", scale=1)
		
		fig, ax = viz.draw(
			figsize=(13, 11),
			title=f"PyG OGBG-PPA (nodes={sample.num_nodes}, edges={sample.edge_index.shape[1]})",
			show_labels=True,
			label_high_degree_only=True
		)
		output = Path(__file__).parent / "outputs" / "example2_pyg.png"
		output.parent.mkdir(exist_ok=True, parents=True)
		viz.save(fig, str(output))
		print(f"✓ Saved to {output}")
	except ImportError as e:
		print(f"⊘ Skipped (PyG not available): {e}")


def example_3_networkx():
	"""Example 3: NetworkX graph visualization."""
	print("\n" + "="*60)
	print("Example 3: NetworkX Graph Visualization")
	print("="*60)
	
	# Create a demo network
	G = nx.karate_club_graph()
	
	viz = GraphVizStrategy()
	viz.load_from_networkx(G)
	viz.compute_layout(layout_type="spring", seed=42, k=0.3)
	viz.encode_node_size(encoding_type="degree", scale=400)
	viz.encode_node_color(encoding_type="degree", cmap="viridis")
	viz.encode_edge_width(encoding_type="fixed", scale=2)
	
	fig, ax = viz.draw(
		figsize=(11, 9),
		title=f"Karate Club Network (nodes={G.number_of_nodes()}, edges={G.number_of_edges()})",
		show_labels=True
	)
	output = Path(__file__).parent / "outputs" / "example3_networkx.png"
	output.parent.mkdir(exist_ok=True, parents=True)
	viz.save(fig, str(output))
	print(f"✓ Saved to {output}")


def example_4_different_layouts():
	"""Example 4: Compare different layout algorithms."""
	print("\n" + "="*60)
	print("Example 4: Layout Algorithm Comparison")
	print("="*60)
	
	data_root = Path(__file__).parent.parent.parent / "tests" / "data" / "ogbg_ppa"
	ds = RawGraphStreamDataset(data_root=data_root, split="train", max_graphs=1)
	sample = next(iter(ds))
	
	layouts = ["spring", "kamada_kawai", "circular"]
	
	for layout in layouts:
		print(f"  Generating {layout} layout...")
		viz = GraphVizStrategy()
		viz.load_from_dict(sample)
		viz.compute_layout(layout_type=layout)
		viz.encode_node_size(encoding_type="degree", scale=25)
		viz.encode_node_color(encoding_type="degree", cmap="coolwarm")
		
		fig, ax = viz.draw(
			figsize=(10, 8),
			title=f"Layout: {layout.upper()}",
			show_labels=False
		)
		output = Path(__file__).parent / "outputs" / f"example4_{layout}.png"
		output.parent.mkdir(exist_ok=True, parents=True)
		viz.save(fig, str(output))
		print(f"  ✓ Saved to {output.name}")


def example_5_encoding_options():
	"""Example 5: Different encoding combinations."""
	print("\n" + "="*60)
	print("Example 5: Encoding Strategy Combinations")
	print("="*60)
	
	data_root = Path(__file__).parent.parent.parent / "tests" / "data" / "ogbg_ppa"
	ds = RawGraphStreamDataset(data_root=data_root, split="train", max_graphs=1)
	sample = next(iter(ds))
	
	# Strategy 1: Size + Color + Width
	print("  Strategy 1: Degree -> Size + Color + Width")
	viz = GraphVizStrategy()
	viz.load_from_dict(sample)
	viz.compute_layout(layout_type="spring")
	viz.encode_node_size(encoding_type="degree", scale=40)
	viz.encode_node_color(encoding_type="degree", cmap="turbo")
	viz.encode_edge_width(encoding_type="weight", scale=3)
	
	fig, ax = viz.draw(figsize=(12, 10), title="Strategy 1: Degree-based Encoding")
	output = Path(__file__).parent / "outputs" / "example5_strategy1.png"
	output.parent.mkdir(exist_ok=True, parents=True)
	viz.save(fig, str(output))
	print(f"  ✓ Saved to {output.name}")


def main():
	"""Run all examples."""
	print("\n" + "="*60)
	print("GRAPH VISUALIZATION QUICK START EXAMPLES")
	print("="*60)
	
	try:
		example_1_basic_dict()
		example_2_pyg_data()
		example_3_networkx()
		example_4_different_layouts()
		example_5_encoding_options()
		
		print("\n" + "="*60)
		print("✓ ALL EXAMPLES COMPLETED SUCCESSFULLY!")
		print("="*60)
		print(f"All outputs saved to: {Path(__file__).parent / 'outputs'}")
		
	except Exception as e:
		print(f"\n✗ Error: {e}")
		import traceback
		traceback.print_exc()


if __name__ == "__main__":
	main()
