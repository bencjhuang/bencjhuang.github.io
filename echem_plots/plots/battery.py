"""
echem_plots/plots/battery.py
Battery cycling plots:
  - Galvanostatic charge-discharge profiles
  - Coulombic efficiency + capacity vs. cycle number
  - Rate capability
"""

import numpy as np
from ..style import (
    COLORS, FIG_SIZE_WIDE,
    COLOR_CD_ODD, COLOR_CD_EVEN, COLOR_CE, COLOR_CAP,
    LINE_WIDTH, MARKER_SIZE,
)
from ._helpers import get_axes, fmt_axes, to_list


def plot_charge_discharge(
    capacity,
    voltage,
    cycle_numbers=None,
    x_is_time=False,
    color_charge=COLOR_CD_ODD,
    color_discharge=COLOR_CD_EVEN,
    use_cycle_colors=False,
    xlabel=None,
    ylabel="Voltage (V vs. Li/Li$^+$)",
    ax=None,
    figsize=FIG_SIZE_WIDE,
):
    """
    Plot galvanostatic charge-discharge voltage profiles.

    Parameters
    ----------
    capacity : array-like or list of array-like
        Specific capacity (mAh g⁻¹) or time (h) for each half-cycle.
        Pass a list to overlay multiple half-cycles or full cycles.
    voltage : array-like or list of array-like
        Voltage data matching `capacity`.
    cycle_numbers : list of int or str, optional
        Labels for each curve (e.g., [1, None, 2, None, 50, None]).
        Conventionally label the charge half-cycle and pass None for
        the corresponding discharge so the legend stays clean.
    x_is_time : bool
        If True, labels x-axis as "Time (h)" instead of capacity.
    color_charge : str
        Color for charge half-cycles (even-indexed curves: 0, 2, 4, …).
    color_discharge : str
        Color for discharge half-cycles (odd-indexed: 1, 3, 5, …).
    use_cycle_colors : bool
        If True each cycle pair gets a unique palette color instead of
        the alternating charge/discharge scheme.
    xlabel : str, optional
        Overrides the auto-generated x-axis label.
    ylabel : str
    ax : matplotlib Axes, optional
    figsize : tuple

    Returns
    -------
    fig, ax

    Examples
    --------
    Three cycles, alternating charge/discharge::

        fig, ax = plot_charge_discharge(
            capacity=[q_chg1, q_dis1, q_chg2, q_dis2, q_chg50, q_dis50],
            voltage =[v_chg1, v_dis1, v_chg2, v_dis2, v_chg50, v_dis50],
            cycle_numbers=[1, None, 2, None, 50, None],
        )
    """
    fig, ax = get_axes(ax, figsize)

    caps     = to_list(capacity)
    volts    = to_list(voltage)
    n_curves = len(caps)
    labels   = to_list(cycle_numbers, n=n_curves)

    if xlabel is None:
        xlabel = "Time (h)" if x_is_time else "Specific capacity (mAh g$^{-1}$)"

    for i, (cap, volt, lbl) in enumerate(zip(caps, volts, labels)):
        if use_cycle_colors:
            clr = COLORS[(i // 2) % len(COLORS)]
        else:
            clr = color_charge if (i % 2 == 0) else color_discharge

        lbl_str = f"Cycle {lbl}" if isinstance(lbl, int) else lbl
        ax.plot(np.asarray(cap), np.asarray(volt),
                color=clr,
                label=lbl_str if (i % 2 == 0 and lbl is not None) else None)

    fmt_axes(ax, xlabel, ylabel)
    if any(l is not None for l in labels):
        ax.legend()

    return fig, ax


def plot_coulombic_eff(
    cycle_number,
    charge_capacity,
    discharge_capacity,
    coulombic_efficiency=None,
    xlabel="Cycle number",
    ylabel_cap="Specific capacity (mAh g$^{-1}$)",
    ylabel_ce="Coulombic efficiency (%)",
    color_charge=COLOR_CAP,
    color_discharge=COLOR_CD_EVEN,
    color_ce=COLOR_CE,
    ce_ylim=(0, 110),
    ax=None,
    figsize=FIG_SIZE_WIDE,
):
    """
    Plot charge/discharge capacity and Coulombic efficiency vs. cycle number.
    Uses a dual y-axis: capacity on the left, CE% on the right.

    Parameters
    ----------
    cycle_number : array-like
        Cycle indices (1, 2, 3, …).
    charge_capacity : array-like
        Charge capacity at each cycle (mAh g⁻¹).
    discharge_capacity : array-like
        Discharge capacity at each cycle (mAh g⁻¹).
    coulombic_efficiency : array-like, optional
        CE values (%). If None, computed automatically as
        discharge_capacity / charge_capacity × 100.
    xlabel, ylabel_cap, ylabel_ce : str
        Axis labels.
    color_charge, color_discharge, color_ce : str
        Colors for the three data series.
    ce_ylim : tuple
        y-axis limits for CE panel (default: 0–110 %).
    ax : matplotlib Axes, optional
        Axes for the capacity panel; CE panel is added as a twin axis.
    figsize : tuple

    Returns
    -------
    fig : matplotlib Figure
    axes : tuple of (ax_capacity, ax_ce)
    """
    fig, ax_cap = get_axes(ax, figsize)

    cycles = np.asarray(cycle_number)
    q_chg  = np.asarray(charge_capacity)
    q_dis  = np.asarray(discharge_capacity)

    if coulombic_efficiency is None:
        ce = np.where(q_chg > 0, q_dis / q_chg * 100, np.nan)
    else:
        ce = np.asarray(coulombic_efficiency)

    ax_cap.plot(cycles, q_chg, marker="^", color=color_charge,
                linestyle="-", label="Charge capacity")
    ax_cap.plot(cycles, q_dis, marker="o", color=color_discharge,
                linestyle="-", label="Discharge capacity")
    fmt_axes(ax_cap, xlabel, ylabel_cap)

    ax_ce = ax_cap.twinx()
    ax_ce.plot(cycles, ce, marker="s", color=color_ce,
               linestyle="--", markersize=MARKER_SIZE * 0.8,
               label="Coulombic eff.")
    ax_ce.set_ylabel(ylabel_ce, fontsize=14)
    ax_ce.tick_params(axis="y", labelsize=12)
    ax_ce.set_ylim(ce_ylim)

    handles1, labels1 = ax_cap.get_legend_handles_labels()
    handles2, labels2 = ax_ce.get_legend_handles_labels()
    ax_cap.legend(handles1 + handles2, labels1 + labels2, loc="best")

    return fig, (ax_cap, ax_ce)


def plot_rate_capability(
    cycle_number,
    capacity,
    c_rates=None,
    xlabel="Cycle number",
    ylabel="Specific capacity (mAh g$^{-1}$)",
    ax=None,
    figsize=FIG_SIZE_WIDE,
):
    """
    Plot rate capability: capacity vs. cycle number across multiple C-rates.

    Parameters
    ----------
    cycle_number : array-like or list of array-like
        Cycle indices for each C-rate segment.
    capacity : array-like or list of array-like
        Capacity at each cycle for each segment.
    c_rates : list of str, optional
        C-rate label for each segment, e.g.
        ["0.1C", "0.2C", "0.5C", "1C", "0.1C (recovery)"].
        Length must equal the number of segments.
    xlabel, ylabel : str
    ax : matplotlib Axes, optional
    figsize : tuple

    Returns
    -------
    fig, ax

    Examples
    --------
    ::

        fig, ax = plot_rate_capability(
            cycle_number=[cyc_01c, cyc_1c, cyc_5c, cyc_01c],
            capacity    =[cap_01c, cap_1c, cap_5c, cap_01c],
            c_rates     =["0.1C", "1C", "5C", "0.1C (recovery)"],
        )
    """
    fig, ax = get_axes(ax, figsize)

    cycles_list = to_list(cycle_number)
    cap_list    = to_list(capacity)
    n_seg       = len(cycles_list)
    rate_labels = c_rates if c_rates is not None else [None] * n_seg

    for i, (cyc, cap, rate) in enumerate(zip(cycles_list, cap_list, rate_labels)):
        clr = COLORS[i % len(COLORS)]
        ax.plot(np.asarray(cyc), np.asarray(cap),
                marker="o", color=clr, linestyle="-", label=rate)

    fmt_axes(ax, xlabel, ylabel)
    if c_rates is not None:
        ax.legend(title="C-rate")

    return fig, ax
