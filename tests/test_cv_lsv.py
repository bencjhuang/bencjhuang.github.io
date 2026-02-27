"""Tests for CV and LSV plotting functions."""

import numpy as np
import matplotlib
matplotlib.use("Agg")   # non-interactive backend for testing
import matplotlib.pyplot as plt
import pytest

from echem_plots.style import apply_style
from echem_plots.plots import plot_cv, plot_lsv

apply_style()

# Minimal synthetic data
V = np.linspace(-0.5, 0.5, 100)
I = np.sin(2 * np.pi * V)


class TestPlotCV:
    def test_returns_fig_ax(self):
        fig, ax = plot_cv(V, I)
        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)
        plt.close(fig)

    def test_single_label_creates_legend(self):
        fig, ax = plot_cv(V, I, label="5 mV/s")
        assert ax.get_legend() is not None
        plt.close(fig)

    def test_no_label_no_legend(self):
        fig, ax = plot_cv(V, I)
        assert ax.get_legend() is None
        plt.close(fig)

    def test_multiple_scans(self):
        fig, ax = plot_cv([V, V * 0.9], [I, I * 1.1],
                          label=["1 mV/s", "5 mV/s"])
        assert len(ax.lines) >= 2
        plt.close(fig)

    def test_axis_labels(self):
        fig, ax = plot_cv(V, I, xlabel="My X", ylabel="My Y")
        assert ax.get_xlabel() == "My X"
        assert ax.get_ylabel() == "My Y"
        plt.close(fig)

    def test_scan_rate_annotation(self):
        fig, ax = plot_cv(V, I, scan_rate="5 mV/s")
        texts = [t.get_text() for t in ax.texts]
        assert "5 mV/s" in texts
        plt.close(fig)

    def test_inject_existing_ax(self):
        fig_ext, ax_ext = plt.subplots()
        fig, ax = plot_cv(V, I, ax=ax_ext)
        assert ax is ax_ext
        plt.close(fig)


class TestPlotLSV:
    def test_returns_fig_ax(self):
        fig, ax = plot_lsv(V, I)
        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)
        plt.close(fig)

    def test_onset_line_added(self):
        fig, ax = plot_lsv(V, I, onset_potential=0.1)
        # axvline adds a Line2D
        vlines = [l for l in ax.lines if len(l.get_xdata()) == 2
                  and l.get_xdata()[0] == l.get_xdata()[1]]
        assert len(vlines) >= 1
        plt.close(fig)

    def test_multiple_curves(self):
        fig, ax = plot_lsv([V, V * 0.8], [I, I * 0.5],
                           label=["Cat A", "Cat B"])
        assert len(ax.lines) >= 2
        plt.close(fig)
