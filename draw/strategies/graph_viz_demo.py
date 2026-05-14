"""Demo: High-information-density graph visualization for ogbg-ppa.

Shows how to use GraphVizStrategy with real data from the data_pipeline module.
"""

from pathlib import Path

from tests.data_pipeline import PyGGraphStreamDataset, RawGraphStreamDataset

from .graph_viz import GraphVizStrategy


def visualize_raw_dict_graph(sample_dict: dict, output_dir: str = "/tmp"):
	"""Visualize a graph from dict format (RawGraphStreamDataset output).
	
	Args:
	    sample_dict: dict with keys 'edge_index', 'num_nodes', 'edge_feat', etc.
	    output_dir: directory to save output
	"""
	viz = GraphVizStrategy()
	viz.load_from_dict(sample_dict)
	viz.compute_layout(layout_type="spring", k=1.5, seed=42)
	viz.encode_node_size(encoding_type="degree", scale=30.0)
	viz.encode_node_color(encoding_type="degree", cmap="coolwarm")
	viz.encode_edge_width(encoding_type="weight", scale=2.0)
	viz.encode_edge_color(encoding_type="fixed", cmap="gray")

	fig, ax = viz.draw(
		figsize=(14, 10),
		title=f"OGBG-PPA Graph (nodes={sample_dict['num_nodes']})",
		show_labels=True,
		label_high_degree_only=True,
	)

	output_path = Path(output_dir) / "ogbg_ppa_dict_viz.png"
	output_path.parent.mkdir(parents=True, exist_ok=True)
	viz.save(fig, str(output_path))
	print(f"Visualization saved to {output_path}")


def visualize_pyg_data_graph(data, output_dir: str = "/tmp"):
	"""Visualize a graph from PyTorch Geometric Data object.
	
	Args:
	    data: torch_geometric.data.Data object
	    output_dir: directory to save output
	"""
	viz = GraphVizStrategy()
	viz.load_from_pyg_data(data)
	viz.compute_layout(layout_type="kamada_kawai")
	viz.encode_node_size(encoding_type="degree", scale=25.0)

	# If node features available, use them for color
	if "features" in viz.node_encodings:
		viz.encode_node_color(encoding_type="feature", cmap="plasma")
	else:
		viz.encode_node_color(encoding_type="degree", cmap="viridis")

	viz.encode_edge_width(encoding_type="weight", scale=1.5)
	viz.encode_edge_color(encoding_type="fixed", cmap="lightgray")

	fig, ax = viz.draw(
		figsize=(14, 10),
		title=f"OGBG-PPA PyG Data (nodes={data.num_nodes}, edges={data.edge_index.shape[1]})",
		show_labels=True,
		label_high_degree_only=True,
	)

	output_path = Path(output_dir) / "ogbg_ppa_pyg_viz.png"
	output_path.parent.mkdir(parents=True, exist_ok=True)
	viz.save(fig, str(output_path))
	print(f"Visualization saved to {output_path}")


def main():
	"""Demo: visualize ogbg-ppa graphs using both APIs."""
	import sys

	# Determine data root (from draw/strategies to project root is 2 levels up)
	data_root = Path(__file__).resolve().parent.parent.parent / "tests" / "data" / "ogbg_ppa"

	if not data_root.exists():
		print(f"Data not found at {data_root}")
		sys.exit(1)

	output_dir = Path(__file__).resolve().parent / "outputs"

	print("=" * 60)
	print("OGBG-PPA Graph Visualization Demo")
	print("=" * 60)

	# 1. Visualize using dict API
	print("\n[1] Loading via RawGraphStreamDataset (dict format)...")
	raw_ds = RawGraphStreamDataset(data_root=data_root, split="train", max_graphs=1)
	raw_sample = next(iter(raw_ds))
	print(f"    Loaded: {raw_sample['num_nodes']} nodes, {raw_sample['edge_index'].shape[1]} edges")
	print("    Visualizing...")
	visualize_raw_dict_graph(raw_sample, output_dir=str(output_dir))

	# 2. Visualize using PyG API
	print("\n[2] Loading via PyGGraphStreamDataset (PyG Data format)...")
	try:
		pyg_ds = PyGGraphStreamDataset(data_root=data_root, split="train", max_graphs=1)
		pyg_sample = next(iter(pyg_ds))
		print(f"    Loaded: {pyg_sample.num_nodes} nodes, {pyg_sample.edge_index.shape[1]} edges")
		print("    Visualizing...")
		visualize_pyg_data_graph(pyg_sample, output_dir=str(output_dir))
	except ImportError as e:
		print(f"    Skipped PyG visualization: {e}")

	print("\n" + "=" * 60)
	print("Demo complete!")
	print(f"Outputs saved to: {output_dir}")
	print("=" * 60)


if __name__ == "__main__":
	main()
