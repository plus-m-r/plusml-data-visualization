"""Layout algorithms and helpers for graph visualization."""

import networkx as nx
import numpy as np


class LayoutHelper:
	"""Provide various graph layouts optimized for information display."""

	@staticmethod
	def spring_layout(G, seed: int = 42, k: float = 1.5, iterations: int = 50):
		"""Force-directed layout (Fruchterman-Reingold).
		
		Good for general-purpose visualization, reveals community structure.
		"""
		return nx.spring_layout(G, seed=seed, k=k, iterations=iterations)

	@staticmethod
	def kamada_kawai_layout(G):
		"""Kamada-Kawai layout.
		
		Often produces cleaner, less tangled results than spring layout.
		"""
		try:
			return nx.kamada_kawai_layout(G)
		except ValueError:
			# Fallback for disconnected graphs
			return nx.spring_layout(G, seed=42)

	@staticmethod
	def circular_layout(G):
		"""Arrange nodes in a circle.
		
		Useful for comparing node properties around a ring.
		"""
		return nx.circular_layout(G)

	@staticmethod
	def shell_layout(G, communities: list[set[int]]):
		"""Arrange communities in concentric shells.
		
		Args:
		    G: NetworkX graph
		    communities: list of sets, each set is a community
		
		Returns:
		    position dict
		"""
		shells = [list(comm) for comm in communities]
		return nx.shell_layout(G, nlist=shells)

	@staticmethod
	def spring_with_community_seeds(
		G, communities: list[set[int]], seed: int = 42, k: float = 1.5
	):
		"""Spring layout with initial positions biased toward communities.
		
		Encourages communities to cluster together spatially.
		
		Args:
		    G: NetworkX graph
		    communities: list of sets
		    seed: random seed
		    k: spring constant
		
		Returns:
		    position dict
		"""
		# Place communities in a rough grid initially
		num_communities = len(communities)
		grid_size = int(np.ceil(np.sqrt(num_communities)))

		# Initial positions based on community grid placement
		pos_init = {}
		for comm_idx, comm_nodes in enumerate(communities):
			row = comm_idx // grid_size
			col = comm_idx % grid_size
			for node in comm_nodes:
				pos_init[node] = np.array([col * 2.0, row * 2.0]) + np.random.randn(2) * 0.3

		# Run spring layout with initial positions
		pos = nx.spring_layout(
			G, pos=pos_init, fixed=[], seed=seed, k=k, iterations=50
		)
		return pos

	@staticmethod
	def hierarchy_layout(G, root: int):
		"""Tree-like layout from a root node (BFS-based).
		
		Args:
		    G: NetworkX graph (should be tree-like)
		    root: root node id
		
		Returns:
		    position dict
		"""
		pos = {}
		visited = set()
		queue = [(root, 0, 0)]  # (node, layer, order_in_layer)
		layer_counts = {}

		while queue:
			node, layer, order = queue.pop(0)
			if node in visited:
				continue
			visited.add(node)

			layer_counts[layer] = layer_counts.get(layer, 0) + 1

			# Position based on layer and order
			x = order - layer_counts[layer] / 2
			y = -layer
			pos[node] = np.array([x, y], dtype=float)

			for neighbor in G.neighbors(node):
				if neighbor not in visited:
					queue.append((neighbor, layer + 1, layer_counts.get(layer + 1, 0)))

		return pos

	@staticmethod
	def spectral_layout(G):
		"""Spectral layout based on graph Laplacian.
		
		Can reveal subtle structural properties.
		"""
		try:
			return nx.spectral_layout(G)
		except ValueError:
			return nx.spring_layout(G, seed=42)
