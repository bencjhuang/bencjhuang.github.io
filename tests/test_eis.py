"""Tests for EIS Nyquist and Bode plotting functions."""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from echem_plots.style import apply_style
from echem_plots.plots import plot_eis_nyquist, plot_eis_bode

apply_style()

# Minimal Randles circuit data
FREQ = np.logspace(4, -2, 40)
OMEGA = 2 * np.pi * FREQ
Z = 10 + 80 / (1 + 1j * OMEGA * 80 * 1e-4)
ZR = Z.real
ZI = -Z.imag          # positive imaginary (convention)
ZMAG = np.abs(Z)
ZPHASE = np.angle(Z, deg=True)


class TestNyquist:
    def test_returns_fig_ax(self):
        fig, ax = plot_eis_nyquist(ZR, ZI)
        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)
        plt.close(fig)

    def test_equal_aspect_default(self):
        fig, ax = plot_eis_nyquist(ZR, ZI)
        # matplotlib returns "equal" or 1.0 depending on version
        assert ax.get_aspect() in ("equal", 1.0)
        plt.close(fig)

    def test_fit_overlay_adds_line(self):
        fit_zr = np.linspace(ZR.min(), ZR.max(), 100)
        fit_zi = np.interp(fit_zr, ZR, ZI)
        fig, ax = plot_eis_nyquist(ZR, ZI, fit_z_real=fit_zr, fit_z_imag=fit_zi)
        # Two artists: data points + fit line
        assert len(ax.lines) >= 2
        plt.close(fig)

    def test_multiple_datasets(self):
        fig, ax = plot_eis_nyquist([ZR, ZR * 1.2], [ZI, ZI * 1.1],
                                   label=["Cell 1", "Cell 2"])
        assert ax.get_legend() is not None
        plt.close(fig)

    def test_axis_labels(self):
        fig, ax = plot_eis_nyquist(ZR, ZI)
        assert "Z" in ax.get_xlabel()
        assert "Z" in ax.get_ylabel()
        plt.close(fig)


class TestBode:
    def test_returns_fig_and_two_axes(self):
        fig, axes = plot_eis_bode(FREQ, ZMAG, ZPHASE)
        assert isinstance(fig, plt.Figure)
        assert len(axes) == 2
        plt.close(fig)

    def test_axes_labels(self):
        fig, (ax_mag, ax_phase) = plot_eis_bode(FREQ, ZMAG, ZPHASE)
        assert "Frequency" in ax_mag.get_xlabel()
        assert "|Z|" in ax_mag.get_ylabel()
        assert "Phase" in ax_phase.get_ylabel()
        plt.close(fig)

    def test_multiple_datasets(self):
        fig, (ax_mag, _) = plot_eis_bode(
            [FREQ, FREQ], [ZMAG, ZMAG * 1.1], [ZPHASE, ZPHASE - 5],
            label=["Before", "After"]
        )
        assert ax_mag.get_legend() is not None
        plt.close(fig)
