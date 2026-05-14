"""Graph visualization encodings for node attributes.

Maps graph data attributes (degree, centrality, labels, etc.) to visual properties
(color, size, alpha) following information visualization best practices.
"""

from typing import Callable

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np


class NodeSizeEncoding:
	"""Map node attributes to visual size."""

	@staticmethod
	def by_degree(degree_dict: dict[int, int], scale: float = 30.0) -> list[float]:
		"""Scale node size by degree."""
		return [degree_dict[n] * scale for n in sorted(degree_dict.keys())]

	@staticmethod
	def by_centrality(
		centrality_dict: dict[int, float], scale: float = 1000.0
	) -> list[float]:
		"""Scale node size by centrality (betweenness, closeness, etc)."""
		return [centrality_dict[n] * scale for n in sorted(centrality_dict.keys())]

	@staticmethod
	def by_values(values: dict[int, float], scale: float = 100.0) -> list[float]:
		"""Scale node size by arbitrary numeric attribute."""
		return [values[n] * scale for n in sorted(values.keys())]

	@staticmethod
	def fixed(nodes: list[int], size: float = 100.0) -> list[float]:
		"""Fixed size for all nodes."""
		return [size] * len(nodes)


class NodeColorEncoding:
	"""Map node attributes to color."""

	@staticmethod
	def by_label(
		labels: dict[int, int], cmap: str = "viridis"
	) -> tuple[list, str]:
		"""Encode categorical labels as discrete colors.
		
		Returns:
		    (color_list, cmap_name)
		"""
		node_list = sorted(labels.keys())
		colors = [labels[n] for n in node_list]
		return colors, cmap

	@staticmethod
	def by_continuous_values(
		values: dict[int, float], cmap: str = "coolwarm"
	) -> tuple[list, str]:
		"""Encode continuous values with color gradient."""
		node_list = sorted(values.keys())
		colors = [values[n] for n in node_list]
		return colors, cmap

	@staticmethod
	def by_community(
		communities: list[set[int]], cmap: str = "tab10"
	) -> tuple[dict[int, int], str]:
		"""Map community membership to color indices.
		
		Args:
		    communities: List of sets, each set contains node indices in a community.
		    cmap: Colormap name.
		
		Returns:
		    (node_to_community_dict, cmap_name)
		"""
		node_community = {}
		for comm_id, comm_nodes in enumerate(communities):
			for node in comm_nodes:
				node_community[node] = comm_id
		return node_community, cmap

	@staticmethod
	def by_feature_pca(features: np.ndarray, use_first_dim: bool = True) -> list[float]:
		"""Encode node features via PCA or single dimension.
		
		Args:
		    features: Shape [num_nodes, num_features]
		    use_first_dim: If True, use first dimension; else apply PCA to 1D.
		
		Returns:
		    list of color values
		"""
		if use_first_dim:
			return features[:, 0].tolist()
		else:
			# Simple PCA to 1D
			from sklearn.decomposition import PCA

			pca = PCA(n_components=1)
			return pca.fit_transform(features).flatten().tolist()


class NodeAlphaEncoding:
	"""Map node attributes to transparency."""

	@staticmethod
	def by_importance(values: dict[int, float], min_alpha: float = 0.3) -> list[float]:
		"""Higher values get higher opacity.
		
		Args:
		    values: dict mapping node to importance score [0, 1]
		    min_alpha: minimum alpha for low-valued nodes
		
		Returns:
		    list of alpha values
		"""
		if not values:
			return []
		val_list = [values[n] for n in sorted(values.keys())]
		val_array = np.array(val_list)
		if val_array.max() == val_array.min():
			return [0.8] * len(val_list)
		normalized = (val_array - val_array.min()) / (val_array.max() - val_array.min())
		return (min_alpha + normalized * (1.0 - min_alpha)).tolist()

	@staticmethod
	def fixed(nodes: list[int], alpha: float = 0.8) -> list[float]:
		"""Fixed alpha for all nodes."""
		return [alpha] * len(nodes)


class EdgeWidthEncoding:
	"""Map edge attributes to visual width."""

	@staticmethod
	def by_weight(
		edge_list: list[tuple[int, int]], G, scale: float = 2.0
	) -> list[float]:
		"""Scale edge width by edge weight attribute 'weight'.
		
		Args:
		    edge_list: list of (u, v) tuples
		    G: NetworkX graph with weights on edges
		    scale: multiplier for width
		
		Returns:
		    list of widths
		"""
		widths = []
		for u, v in edge_list:
			w = G[u][v].get("weight", 1.0)
			widths.append(w * scale)
		return widths

	@staticmethod
	def by_custom_attribute(
		edge_list: list[tuple[int, int]], attr_dict: dict[tuple, float], scale: float = 1.0
	) -> list[float]:
		"""Scale by custom edge attribute from external dict.
		
		Args:
		    edge_list: list of (u, v) tuples
		    attr_dict: dict mapping (u, v) to numeric value
		    scale: multiplier
		
		Returns:
		    list of widths
		"""
		return [attr_dict.get((u, v), attr_dict.get((v, u), 1.0)) * scale for u, v in edge_list]

	@staticmethod
	def fixed(edge_list: list[tuple[int, int]], width: float = 1.0) -> list[float]:
		"""Fixed width for all edges."""
		return [width] * len(edge_list)


class EdgeColorEncoding:
	"""Map edge attributes to color."""

	@staticmethod
	def by_weight(
		edge_list: list[tuple[int, int]], G, cmap: str = "plasma"
	) -> tuple[list, str]:
		"""Encode edge weight with color gradient.
		
		Args:
		    edge_list: list of (u, v) tuples
		    G: NetworkX graph with weights
		    cmap: colormap name
		
		Returns:
		    (color_values, cmap_name)
		"""
		colors = [G[u][v].get("weight", 1.0) for u, v in edge_list]
		return colors, cmap

	@staticmethod
	def by_community_crossing(
		edge_list: list[tuple[int, int]], node_community: dict[int, int]
	) -> list[str]:
		"""Color edges: same community (intra) vs different community (inter).
		
		Args:
		    edge_list: list of (u, v) tuples
		    node_community: dict mapping node to community id
		
		Returns:
		    list of color strings
		"""
		colors = []
		for u, v in edge_list:
			if node_community.get(u) == node_community.get(v):
				colors.append("lightgray")
			else:
				colors.append("red")
		return colors

	@staticmethod
	def fixed(edge_list: list[tuple[int, int]], color: str = "gray") -> list[str]:
		"""Fixed color for all edges."""
		return [color] * len(edge_list)
