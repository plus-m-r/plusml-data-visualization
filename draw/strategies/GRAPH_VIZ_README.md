# Graph Visualization Strategies

高信息密度的图神经网络数据可视化模块。支持多种数据源和灵活的视觉编码方式。

## 核心概念

### 信息密度视觉编码

本模块遵循**信息可视化**的设计原则，将数据属性映射到视觉属性：

| 数据属性 | 视觉编码 | 对应类/方法 |
|---------|---------|----------|
| 节点重要性（度数、中心性） | 节点大小 | `NodeSizeEncoding` |
| 节点分类/标签 | 节点颜色 | `NodeColorEncoding` |
| 边的权重/强度 | 边宽度 | `EdgeWidthEncoding` |
| 边的类型/属性 | 边颜色 | `EdgeColorEncoding` |
| 空间关系 | 布局算法 | `LayoutHelper` |

### 模块结构

```
draw/strategies/
├── graph_viz.py          # 核心可视化引擎 (GraphVizStrategy)
├── encodings.py          # 节点/边编码策略
├── layout_helpers.py     # 布局算法辅助
├── graph_viz_demo.py     # 实际演示脚本
└── README.md             # 本文档
```

## API 使用

### 1. 最小示例（dict 数据）

```python
from draw.strategies import GraphVizStrategy

# 从 RawGraphStreamDataset 获取样本
sample = {
    "edge_index": [[0,1,1,2], [1,0,2,1]],
    "num_nodes": 3,
    "edge_feat": [[0.5], [0.7], [0.3], [0.8]],
}

viz = GraphVizStrategy()
viz.load_from_dict(sample)
viz.compute_layout(layout_type="spring")
viz.encode_node_size(encoding_type="degree")
viz.encode_node_color(encoding_type="degree")
viz.encode_edge_width(encoding_type="weight")

fig, ax = viz.draw(title="My Graph")
viz.save(fig, "output.png")
```

### 2. PyG Data 示例

```python
from draw.strategies import GraphVizStrategy

# 从 PyGGraphStreamDataset 获取样本
data = PyGGraphStreamDataset(data_root="...", split="train", max_graphs=1)
sample = next(iter(data))

viz = GraphVizStrategy()
viz.load_from_pyg_data(sample)
viz.compute_layout(layout_type="kamada_kawai")
viz.encode_node_size(encoding_type="degree", scale=25)
viz.encode_node_color(encoding_type="feature", cmap="plasma")
viz.encode_edge_width(encoding_type="weight")

fig, ax = viz.draw(show_labels=True)
viz.show()
```

### 3. NetworkX 图

```python
import networkx as nx
from draw.strategies import GraphVizStrategy

G = nx.karate_club_graph()

viz = GraphVizStrategy()
viz.load_from_networkx(G)
viz.compute_layout(layout_type="spring")
viz.encode_node_size(encoding_type="degree")
viz.encode_node_color(encoding_type="degree", cmap="cool")

fig, ax = viz.draw()
```

## 类 API 文档

### GraphVizStrategy

主要的可视化管理类。支持链式调用。

#### 数据加载

- `load_from_dict(graph_dict)` - 加载来自 RawGraphStreamDataset 的 dict
- `load_from_pyg_data(data)` - 加载来自 PyGGraphStreamDataset 的 PyG Data
- `load_from_networkx(G)` - 加载 NetworkX 图

#### 布局

- `compute_layout(layout_type='spring', **kwargs)` 
  - `'spring'` - Fruchterman-Reingold (默认)
  - `'kamada_kawai'` - Kamada-Kawai (更整洁)
  - `'circular'` - 圆形排列
  - `'spectral'` - 谱分解
  - `'hierarchy'` - 层级树形

#### 节点编码

- `encode_node_size(encoding_type='degree', scale=30)` - 控制节点大小
  - `'degree'` - 按度数缩放
  - `'fixed'` - 固定大小
  
- `encode_node_color(encoding_type='degree', cmap='viridis')` - 控制节点颜色
  - `'degree'` - 按度数着色
  - `'label'` - 按标签类别着色
  - `'feature'` - 按节点特征着色

#### 边编码

- `encode_edge_width(encoding_type='weight', scale=2)` - 控制边宽度
  - `'weight'` - 按权重缩放
  - `'fixed'` - 固定宽度
  
- `encode_edge_color(encoding_type='fixed', cmap='gray')` - 控制边颜色
  - `'weight'` - 按权重着色
  - `'fixed'` - 单一颜色

#### 绘制与保存

- `draw(figsize=(12,8), title='...', show_labels=False, dpi=100)` - 绘制图
- `save(fig, output_path, dpi=300)` - 保存为文件
- `show()` - 在屏幕上显示

### 编码类

#### NodeSizeEncoding

```python
NodeSizeEncoding.by_degree(degree_dict, scale=30)
NodeSizeEncoding.by_centrality(centrality_dict, scale=1000)
NodeSizeEncoding.by_values(values_dict, scale=100)
NodeSizeEncoding.fixed(nodes, size=100)
```

#### NodeColorEncoding

```python
NodeColorEncoding.by_label(labels_dict, cmap="viridis")
NodeColorEncoding.by_continuous_values(values_dict, cmap="coolwarm")
NodeColorEncoding.by_community(communities_list, cmap="tab10")
NodeColorEncoding.by_feature_pca(features_array, use_first_dim=True)
```

#### EdgeWidthEncoding

```python
EdgeWidthEncoding.by_weight(edge_list, G, scale=2.0)
EdgeWidthEncoding.by_custom_attribute(edge_list, attr_dict, scale=1.0)
EdgeWidthEncoding.fixed(edge_list, width=1.0)
```

#### EdgeColorEncoding

```python
EdgeColorEncoding.by_weight(edge_list, G, cmap="plasma")
EdgeColorEncoding.by_community_crossing(edge_list, node_community)
EdgeColorEncoding.fixed(edge_list, color="gray")
```

### LayoutHelper

```python
LayoutHelper.spring_layout(G, seed=42, k=1.5, iterations=50)
LayoutHelper.kamada_kawai_layout(G)
LayoutHelper.circular_layout(G)
LayoutHelper.spectral_layout(G)
LayoutHelper.shell_layout(G, communities)
LayoutHelper.spring_with_community_seeds(G, communities, seed=42, k=1.5)
```

## 实践建议

### 1. 选择合适的编码

**原则**：一张图最多编码 3 种数据属性（否则过载）

- **关键信息**（最重要）→ 用显著的编码（如节点大小、颜色）
- **辅助信息** → 用细微的编码（如边宽、透明度）
- **装饰信息** → 用标签或图例

### 2. 适配数据规模

| 节点数 | 推荐方案 |
|-------|---------|
| <100 | spring layout + 显示所有标签 |
| 100-1k | kamada-kawai + 只显示高度数节点标签 |
| >1k | spectral layout + 没有标签，用颜色编码 |

### 3. 调整参数

```python
# 对于稠密图，增加排斥力（k 越大，节点离得越远）
viz.compute_layout(layout_type="spring", k=2.0)

# 对于稀疏图，增加弹簧常数，让布局更紧凑
viz.compute_layout(layout_type="spring", k=0.5)

# 对于权重图，增加边宽度尺度，凸显权重差异
viz.encode_edge_width(encoding_type="weight", scale=5.0)
```

## 运行演示

```bash
# 从项目根目录
python -m draw.strategies.graph_viz_demo
```

这会：
1. 使用 `RawGraphStreamDataset` 加载第一个 OGBG-PPA 图样本
2. 使用 `PyGGraphStreamDataset` 加载第一个 PyG Data 样本（如果 PyG 已安装）
3. 生成两张高信息密度的可视化图
4. 保存到 `draw/strategies/outputs/`

## 常见问题

**Q: 节点标签太密集，无法看清？**  
A: 设置 `show_labels=True, label_high_degree_only=True`，只标注高度数的重要节点。

**Q: 图太分散，节点看不清？**  
A: 增加 spring layout 的 `k` 参数 → `compute_layout(layout_type="spring", k=0.5)`

**Q: 颜色看不出差异？**  
A: 改用更对比的 colormap，如 `"tab10"`、`"Set1"`、`"Paired"`。

**Q: 边太多，看起来一团糟？**  
A: 
1. 减小边宽度 → `encode_edge_width(scale=0.5)`
2. 增加边透明度 → 在 draw() 中调整
3. 只显示权重上的边

## 扩展建议

- **社区检测**：集成 `networkx.algorithms.community` 中的算法
- **DGL 支持**：添加 `load_from_dgl_graph()`
- **交互式可视化**：集成 Plotly 或 Bokeh
- **节点注释**：在节点旁显示统计摘要

