# draw 模块 API 说明

本模块为 plusml-data-visualization 的核心绘图与可视化接口，支持多种图表类型和高信息密度图神经网络可视化。

---

## 1. 主要接口

### 1.1. 通用接口

- `draw_interface.py`  
  通用绘图接口定义，所有绘图策略需实现该接口。
  - `DrawInterface` (抽象基类)
    - `draw(data, **kwargs)`：主绘图方法，返回 matplotlib Figure。

### 1.2. 策略注册与分发

- `plotter.py`  
  策略分发与统一入口。
  - `draw_grid_chart(data, **kwargs)`：网格类图表（如热力图、表格）
  - `draw_line_chart(data, **kwargs)`：折线/曲线图
  - `MatplotlibDrawer`：底层渲染器

- `strategies/`  
  各类绘图策略与高级可视化（见下）

---

## 2. 高级图可视化接口

- `strategies/graph_viz.py`  
  高信息密度图可视化主类
  - `GraphVizStrategy`
    - `load_from_dict(graph_dict)`：加载 dict 格式图数据
    - `load_from_pyg_data(data)`：加载 PyG Data 对象
    - `load_from_networkx(G)`：加载 NetworkX 图
    - `compute_layout(layout_type, **kwargs)`：计算节点布局
    - `encode_node_size(encoding_type, scale)`：节点大小编码
    - `encode_node_color(encoding_type, cmap)`：节点颜色编码
    - `encode_edge_width(encoding_type, scale)`：边宽度编码
    - `encode_edge_color(encoding_type, cmap)`：边颜色编码
    - `draw(...)`：绘制图形，返回 (fig, ax)
    - `save(fig, output_path, dpi)`：保存图片
    - `show()`：显示图片

- `strategies/encodings.py`  
  视觉编码策略类
  - `NodeSizeEncoding`、`NodeColorEncoding`、`EdgeWidthEncoding`、`EdgeColorEncoding`

- `strategies/layout_helpers.py`  
  布局算法辅助类
  - `LayoutHelper`：spring、kamada_kawai、circular、spectral、shell 等

---

## 3. 快速使用示例

```python
from draw.strategies import GraphVizStrategy
from tests.data_pipeline import RawGraphStreamDataset

ds = RawGraphStreamDataset(data_root="tests/data/ogbg_ppa", split="train")
sample = next(iter(ds))

viz = GraphVizStrategy()
viz.load_from_dict(sample)
viz.compute_layout(layout_type="spring")
viz.encode_node_size("degree")
viz.encode_node_color("degree")
viz.encode_edge_width("weight")
fig, ax = viz.draw(title="OGBG-PPA Graph")
viz.save(fig, "output.png")
```

---

## 4. 主要导出对象

- `draw_interface.DrawInterface`
- `plotter.MatplotlibDrawer, draw_grid_chart, draw_line_chart`
- `strategies.GraphVizStrategy, NodeSizeEncoding, NodeColorEncoding, EdgeWidthEncoding, EdgeColorEncoding, LayoutHelper`

---

## 5. 依赖

- matplotlib
- networkx
- numpy
- (可选) torch, torch_geometric

---

## 6. 简明配置与一站式接口（推荐）

- `simple.py`  
  提供统一的全局绘图配置获取与色板管理，便于策略/可视化/脚本快速调用。
  - `get_default_plot_config()`：返回 dict，包含字体、色板、输出目录等全局配置
  - `get_color_palette_by_name(name)`：按名称获取色板（ColorPalette 对象）
  - `ensure_output_dir_exists()`：确保输出目录存在
  - 快捷别名：`default_config`、`get_palette`、`ensure_output_dir`

### 示例：

```python
from draw.simple import get_default_plot_config, get_palette, ensure_output_dir

cfg = get_default_plot_config()
print(cfg["font_family"], cfg["color_palette"])

palette = get_palette("classic_academic_blue")
print(palette.colors)

ensure_output_dir()  # 自动创建输出目录
```

---

详细 API 见 `draw/strategies/GRAPH_VIZ_README.md`。
