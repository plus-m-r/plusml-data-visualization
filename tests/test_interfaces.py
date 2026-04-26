from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

from config import PlotConfig
from config import get_color_palette
from draw import MatplotlibDrawer
from draw.strategies.base import DrawStrategy


class ConfigAndInterfaceTests(unittest.TestCase):
    def test_get_color_palette_success(self) -> None:
        palette = get_color_palette("classic_academic_blue")
        self.assertEqual(palette.name, "classic_academic_blue")
        self.assertGreaterEqual(len(palette.colors), 3)

    def test_get_color_palette_failure(self) -> None:
        with self.assertRaises(ValueError):
            get_color_palette("not_exists")

    def test_resolve_output_path_allows_nested_inside_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = str(Path(tmpdir) / "figures")
            out = DrawStrategy.resolve_output_path(
                output_dir,
                "2026/line.png",
                fallback_name="line_chart",
            )
            self.assertTrue(str(out).startswith(str(Path(output_dir).resolve())))
            self.assertEqual(out.name, "line.png")

    def test_resolve_output_path_rejects_outside_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = str(Path(tmpdir) / "figures")
            outside = str(Path(tmpdir) / "outside.png")
            with self.assertRaises(ValueError):
                DrawStrategy.resolve_output_path(output_dir, outside, fallback_name="line_chart")

    def test_draw_line_saves_figure(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_file = Path(tmpdir) / "line.csv"
            data_file.write_text("x,y\n0,1\n1,2\n2,3\n", encoding="utf-8")

            output_dir = Path(tmpdir) / "figures"
            from config import LayoutMode

            config = PlotConfig(
                font_family="Times New Roman",
                final_publication_font_pt=7.0,
                source_figure_width_mm=190.0,
                final_subplot_width_mm_by_mode={
                    LayoutMode.ONE_PER_ROW: 90.0,
                    LayoutMode.TWO_PER_ROW: 90.0,
                    LayoutMode.THREE_PER_ROW: 60.0,
                },
                output_dir=str(output_dir),
                color_palette_name="classic_academic_blue",
            )

            drawer = MatplotlibDrawer(config=config)
            fig, _ = drawer.draw_line(source_file=str(data_file), save_path="2026/line.png")
            self.assertIsNotNone(fig)
            self.assertTrue((output_dir / "2026" / "line.png").exists())


if __name__ == "__main__":
    unittest.main()
