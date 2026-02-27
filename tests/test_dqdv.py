"""Tests for differential capacity (dQ/dV) plotting function."""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from echem_plots.style import apply_style
from echem_plots.plots import plot_dqdv

apply_style()

V = np.linspace(2.5, 4.2, 300)
DQDV = (300 * np.exp(-((V - 3.4) ** 2) / (2 * 0.05 ** 2))
        - 300 * np.exp(-((V - 3.3) ** 2) / (2 * 0.05 ** 2)))


class TestDQDV:
    def test_returns_fig_ax(self):
        fig, ax = plot_dqdv(V, DQDV)
        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)
        plt.close(fig)

    def test_zero_line_present(self):
        fig, ax = plot_dqdv(V, DQDV)
        # axhline at 0 + the data curve = at least 2 lines total
        assert len(ax.lines) >= 2
        plt.close(fig)

    def test_multiple_curves_with_labels(self):
        fig, ax = plot_dqdv(
            [V, V], [DQDV, DQDV * 0.9],
            label=["Cycle 1", "Cycle 50"],
        )
        assert ax.get_legend() is not None
        assert len([l for l in ax.lines if not np.all(l.get_ydata() == 0)]) >= 2
        plt.close(fig)

    def test_axis_labels(self):
        fig, ax = plot_dqdv(V, DQDV)
        assert "V" in ax.get_xlabel() or "Voltage" in ax.get_xlabel()
        assert "dQ" in ax.get_ylabel() or "Q" in ax.get_ylabel()
        plt.close(fig)

    def test_custom_color(self):
        fig, ax = plot_dqdv(V, DQDV, color="#FF0000")
        data_lines = [l for l in ax.lines if not np.all(l.get_ydata() == 0)]
        assert data_lines[0].get_color() == "#FF0000"
        plt.close(fig)
