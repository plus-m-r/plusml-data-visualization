"""Core graph visualization strategies.

Supports multiple data sources (dict, PyG Data, NetworkX) and enables
high-information-density visualization with flexible encoding strategies.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

if TYPE_CHECKING:
	from matplotlib.figure import Figure
	from matplotlib.axes import Axes

from .encodings import EdgeColorEncoding, EdgeWidthEncoding, NodeColorEncoding, NodeSizeEncoding
from .layout_helpers import LayoutHelper


class GraphVizStrategy:
	"""High-information-density graph visualization strategy.
	
	Flexibly maps node/edge attributes to visual properties and supports
	multiple data source formats.
	"""

	def __init__(self):
		self.G: Optional[nx.Graph] = None
		self.pos: Optional[dict] = None
		self.node_encodings: dict[str, Any] = {}
		self.edge_encodings: dict[str, Any] = {}

	def load_from_dict(self, graph_dict: dict) -> "GraphVizStrategy":
		"""Load graph from dict format (with 'edge_index', 'edge_feat', etc)."""
		edge_index = graph_dict.get("edge_index", [[], []])
		if isinstance(edge_index, list):
			sources, targets = edge_index
		else:
			sources = edge_index[0].tolist()
			targets = edge_index[1].tolist()

		self.G = nx.Graph()
		num_nodes = graph_dict.get("num_nodes", max(max(sources), max(targets)) + 1 if sources else 0)
		self.G.add_nodes_from(range(num_nodes))
		self.G.add_edges_from(zip(sources, targets))

		# Store edge features if available
		if "edge_feat" in graph_dict:
			edge_feat = graph_dict["edge_feat"]
			for idx, (u, v) in enumerate(zip(sources, targets)):
				# Handle both torch tensors and numpy arrays
				feat_val = edge_feat[idx]
				if hasattr(feat_val, 'numpy'):  # torch tensor
					feat_val = feat_val.numpy()
				if hasattr(feat_val, '__len__'):  # is array-like
					self.G[u][v]["weight"] = float(np.mean(feat_val))
				else:
					self.G[u][v]["weight"] = float(feat_val)

		return self

	def load_from_pyg_data(self, data) -> "GraphVizStrategy":
		"""Load graph from PyTorch Geometric Data object."""
		edge_index = data.edge_index
		if hasattr(edge_index, "numpy"):
			sources = edge_index[0].numpy()
			targets = edge_index[1].numpy()
		else:
			sources, targets = edge_index

		self.G = nx.Graph()
		num_nodes = data.num_nodes
		self.G.add_nodes_from(range(num_nodes))
		self.G.add_edges_from(zip(sources, targets))

		# Store edge features if available
		if hasattr(data, "edge_attr") and data.edge_attr is not None:
			edge_attr = data.edge_attr
			if hasattr(edge_attr, "numpy"):
				edge_attr = edge_attr.numpy()
			for idx, (u, v) in enumerate(zip(sources, targets)):
				w = float(np.mean(edge_attr[idx])) if edge_attr[idx].shape[0] > 0 else 1.0
				self.G[u][v]["weight"] = w

		# Store node features for visualization
		if hasattr(data, "x") and data.x is not None:
			node_features = data.x
			if hasattr(node_features, "numpy"):
				node_features = node_features.numpy()
			self.node_encodings["features"] = node_features

		# Store labels
		if hasattr(data, "y") and data.y is not None:
			self.node_encodings["label"] = data.y

		return self

	def load_from_networkx(self, G: nx.Graph) -> "GraphVizStrategy":
		"""Load directly from NetworkX graph."""
		self.G = G
		return self

	def compute_layout(
		self,
		layout_type: str = "spring",
		**kwargs,
	) -> "GraphVizStrategy":
		"""Compute node positions using specified layout algorithm.
		
		Args:
		    layout_type: 'spring', 'kamada_kawai', 'circular', 'spectral', etc.
		    **kwargs: arguments passed to layout function
		"""
		if self.G is None:
			raise ValueError("Graph not loaded. Call load_from_* first.")

		if layout_type == "spring":
			self.pos = LayoutHelper.spring_layout(self.G, **kwargs)
		elif layout_type == "kamada_kawai":
			self.pos = LayoutHelper.kamada_kawai_layout(self.G)
		elif layout_type == "circular":
			self.pos = LayoutHelper.circular_layout(self.G)
		elif layout_type == "spectral":
			self.pos = LayoutHelper.spectral_layout(self.G)
		else:
			raise ValueError(f"Unknown layout type: {layout_type}")

		return self

	def encode_node_size(
		self, encoding_type: str = "degree", scale: float = 30.0
	) -> "GraphVizStrategy":
		"""Encode node size.
		
		Args:
		    encoding_type: 'degree', 'centrality', 'fixed'
		    scale: scaling factor
		"""
		if self.G is None:
			raise ValueError("Graph not loaded.")

		if encoding_type == "degree":
			degree_dict = dict(self.G.degree())
			self.node_encodings["size"] = NodeSizeEncoding.by_degree(degree_dict, scale)
		elif encoding_type == "fixed":
			self.node_encodings["size"] = NodeSizeEncoding.fixed(list(self.G.nodes()), scale)
		else:
			raise ValueError(f"Unknown encoding type: {encoding_type}")

		return self

	def encode_node_color(
		self, encoding_type: str = "degree", cmap: str = "viridis"
	) -> "GraphVizStrategy":
		"""Encode node color.
		
		Args:
		    encoding_type: 'degree', 'label', 'feature', 'fixed'
		    cmap: colormap name
		"""
		if self.G is None:
			raise ValueError("Graph not loaded.")

		if encoding_type == "degree":
			degree_dict = dict(self.G.degree())
			colors, cmap_name = NodeColorEncoding.by_continuous_values(degree_dict, cmap)
			self.node_encodings["color"] = colors
			self.node_encodings["cmap"] = cmap_name
		elif encoding_type == "label":
			if "label" in self.node_encodings:
				labels_dict = {i: int(self.node_encodings["label"][i]) for i in range(self.G.number_of_nodes())}
				colors, cmap_name = NodeColorEncoding.by_label(labels_dict, cmap)
				self.node_encodings["color"] = colors
				self.node_encodings["cmap"] = cmap_name
		elif encoding_type == "feature":
			if "features" in self.node_encodings:
				colors = NodeColorEncoding.by_feature_pca(self.node_encodings["features"])
				self.node_encodings["color"] = colors
				self.node_encodings["cmap"] = cmap
		else:
			raise ValueError(f"Unknown encoding type: {encoding_type}")

		return self

	def encode_edge_width(
		self, encoding_type: str = "weight", scale: float = 2.0
	) -> "GraphVizStrategy":
		"""Encode edge width.
		
		Args:
		    encoding_type: 'weight', 'fixed'
		    scale: scaling factor
		"""
		if self.G is None:
			raise ValueError("Graph not loaded.")

		edge_list = list(self.G.edges())
		if encoding_type == "weight":
			self.edge_encodings["width"] = EdgeWidthEncoding.by_weight(edge_list, self.G, scale)
		elif encoding_type == "fixed":
			self.edge_encodings["width"] = EdgeWidthEncoding.fixed(edge_list, scale)
		else:
			raise ValueError(f"Unknown encoding type: {encoding_type}")

		return self

	def encode_edge_color(
		self, encoding_type: str = "fixed", cmap: str = "gray"
	) -> "GraphVizStrategy":
		"""Encode edge color.
		
		Args:
		    encoding_type: 'weight', 'fixed'
		    cmap: colormap name or color string
		"""
		if self.G is None:
			raise ValueError("Graph not loaded.")

		edge_list = list(self.G.edges())
		if encoding_type == "weight":
			colors, cmap_name = EdgeColorEncoding.by_weight(edge_list, self.G, cmap)
			self.edge_encodings["color"] = colors
			self.edge_encodings["cmap"] = cmap_name
		elif encoding_type == "fixed":
			self.edge_encodings["color"] = EdgeColorEncoding.fixed(edge_list, cmap)
		else:
			raise ValueError(f"Unknown encoding type: {encoding_type}")

		return self

	def draw(
		self,
		figsize: tuple[float, float] = (12, 8),
		title: str = "Graph Visualization",
		show_labels: bool = False,
		label_high_degree_only: bool = True,
		dpi: int = 100,
	) -> tuple[Figure, Axes]:
		"""Draw the graph with encoded properties.
		
		Args:
		    figsize: figure size (width, height)
		    title: plot title
		    show_labels: whether to show node labels
		    label_high_degree_only: if True, only label high-degree nodes
		    dpi: dots per inch
		
		Returns:
		    (Figure, Axes)
		"""
		if self.G is None or self.pos is None:
			raise ValueError("Graph not loaded or layout not computed.")

		fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

		# Draw edges
		edge_list = list(self.G.edges())
		edge_colors = self.edge_encodings.get("color", "gray")
		edge_widths = self.edge_encodings.get("width", 1.0)

		if isinstance(edge_colors, list) and len(edge_colors) > 0 and isinstance(edge_colors[0], str):
			# Discrete colors (strings)
			nx.draw_networkx_edges(
				self.G,
				self.pos,
				edge_color=edge_colors,
				width=edge_widths,
				alpha=0.6,
				ax=ax,
			)
		else:
			# Continuous colors (numeric)
			if "cmap" in self.edge_encodings:
				nx.draw_networkx_edges(
					self.G,
					self.pos,
					edge_color=edge_colors,
					edge_cmap=plt.get_cmap(self.edge_encodings["cmap"]),
					width=edge_widths,
					alpha=0.6,
					ax=ax,
				)
			else:
				nx.draw_networkx_edges(
					self.G,
					self.pos,
					edge_color=edge_colors,
					width=edge_widths,
					alpha=0.6,
					ax=ax,
				)

		# Draw nodes
		node_colors = self.node_encodings.get("color", "lightblue")
		node_sizes = self.node_encodings.get("size", 300)

		nodes = nx.draw_networkx_nodes(
			self.G,
			self.pos,
			node_color=node_colors,
			node_size=node_sizes,
			cmap=self.node_encodings.get("cmap", "viridis"),
			alpha=0.9,
			ax=ax,
		)

		# Draw labels
		if show_labels:
			if label_high_degree_only:
				degree_dict = dict(self.G.degree())
				threshold = np.median(list(degree_dict.values()))
				labels = {n: str(n) for n, d in degree_dict.items() if d >= threshold}
			else:
				labels = {n: str(n) for n in self.G.nodes()}

			nx.draw_networkx_labels(self.G, self.pos, labels=labels, font_size=8, ax=ax)

		ax.set_title(title, fontsize=14)
		ax.axis("off")
		fig.tight_layout()

		return fig, ax

	def save(self, fig: Figure, output_path: str, dpi: int = 300):
		"""Save figure to file."""
		fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
		print(f"Saved to {output_path}")

	def show(self):
		"""Display the figure."""
		plt.show()
