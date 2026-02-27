"""Tests for battery cycling plotting functions."""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from echem_plots.style import apply_style
from echem_plots.plots import (
    plot_charge_discharge,
    plot_coulombic_eff,
    plot_rate_capability,
)

apply_style()

Q = np.linspace(0, 150, 100)
V_CHG = 3.0 + 1.2 * (Q / 150) ** 0.4
V_DIS = 4.2 - 1.2 * (Q / 150) ** 0.6
CYCLES = np.arange(1, 51)
Q_CHG = 150 * np.ones(50)
Q_DIS = 148 * np.ones(50)


class TestChargeDischargePlot:
    def test_returns_fig_ax(self):
        fig, ax = plot_charge_discharge(Q, V_CHG)
        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)
        plt.close(fig)

    def test_multiple_halfcycles(self):
        fig, ax = plot_charge_discharge(
            [Q, Q[::-1]], [V_CHG, V_DIS],
            cycle_numbers=[1, None]
        )
        assert len(ax.lines) == 2
        plt.close(fig)

    def test_xlabel_capacity(self):
        fig, ax = plot_charge_discharge(Q, V_CHG)
        assert "capacity" in ax.get_xlabel().lower()
        plt.close(fig)

    def test_xlabel_time(self):
        fig, ax = plot_charge_discharge(Q, V_CHG, x_is_time=True)
        assert "time" in ax.get_xlabel().lower()
        plt.close(fig)

    def test_cycle_colors_flag(self):
        fig, ax = plot_charge_discharge(
            [Q, Q[::-1], Q, Q[::-1]],
            [V_CHG, V_DIS, V_CHG * 0.98, V_DIS * 0.98],
            use_cycle_colors=True,
        )
        assert len(ax.lines) == 4
        plt.close(fig)


class TestCoulombicEff:
    def test_returns_fig_and_two_axes(self):
        fig, axes = plot_coulombic_eff(CYCLES, Q_CHG, Q_DIS)
        assert isinstance(fig, plt.Figure)
        assert len(axes) == 2
        plt.close(fig)

    def test_auto_ce_computation(self):
        fig, (ax_cap, ax_ce) = plot_coulombic_eff(CYCLES, Q_CHG, Q_DIS)
        # CE line should exist on twin axis
        assert len(ax_ce.lines) >= 1
        plt.close(fig)

    def test_explicit_ce(self):
        ce = Q_DIS / Q_CHG * 100
        fig, (ax_cap, ax_ce) = plot_coulombic_eff(
            CYCLES, Q_CHG, Q_DIS, coulombic_efficiency=ce
        )
        assert len(ax_ce.lines) >= 1
        plt.close(fig)

    def test_ce_ylim(self):
        fig, (_, ax_ce) = plot_coulombic_eff(CYCLES, Q_CHG, Q_DIS,
                                              ce_ylim=(80, 105))
        assert ax_ce.get_ylim() == (80, 105)
        plt.close(fig)


class TestRateCapability:
    def test_returns_fig_ax(self):
        fig, ax = plot_rate_capability(
            [np.arange(1, 6), np.arange(6, 11)],
            [Q_CHG[:5], Q_CHG[:5] * 0.8],
        )
        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)
        plt.close(fig)

    def test_legend_with_c_rates(self):
        fig, ax = plot_rate_capability(
            [np.arange(1, 6), np.arange(6, 11)],
            [Q_CHG[:5], Q_CHG[:5] * 0.8],
            c_rates=["0.1C", "1C"],
        )
        assert ax.get_legend() is not None
        plt.close(fig)
