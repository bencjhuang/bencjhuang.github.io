"""
echem_plots/plots/cv_lsv.py
Cyclic Voltammetry (CV) and Linear Sweep Voltammetry (LSV) plots.
"""

import numpy as np
from ..style import (
    COLORS, FIG_SIZE_SINGLE, COLOR_CV, COLOR_LSV,
)
from ._helpers import get_axes, fmt_axes, to_list


def plot_cv(
    voltage,
    current,
    label=None,
    color=None,
    xlabel="Voltage (V vs. Li/Li$^+$)",
    ylabel="Current (mA)",
    normalize=False,
    scan_rate=None,
    ax=None,
    figsize=FIG_SIZE_SINGLE,
):
    """
    Plot one or more cyclic voltammetry (CV) curves.

    Parameters
    ----------
    voltage : array-like or list of array-like
        Voltage data. Pass a list to overlay multiple scans.
    current : array-like or list of array-like
        Current data (mA). Must match shape of `voltage`.
    label : str or list of str, optional
        Legend label(s).
    color : str or list of str, optional
        Line color(s). Cycles through the group palette if None.
    xlabel, ylabel : str
        Axis labels. Defaults assume Li/Li⁺ reference and mA units.
    normalize : bool
        Convenience flag — when True, ylabel is updated to mA g⁻¹ to
        remind you that you are passing mass-normalized current.
    scan_rate : str, optional
        Annotates the scan rate in the top-right corner, e.g. "5 mV/s".
    ax : matplotlib Axes, optional
        Plot into an existing Axes object; creates a new figure if None.
    figsize : tuple
        Figure size in inches (width, height).

    Returns
    -------
    fig : matplotlib Figure
    ax  : matplotlib Axes

    Examples
    --------
    Single scan::

        fig, ax = plot_cv(voltage, current, label="5 mV/s")

    Multiple scan rates::

        fig, ax = plot_cv(
            [v1, v2, v3],
            [i1, i2, i3],
            label=["1 mV/s", "5 mV/s", "10 mV/s"],
        )
    """
    fig, ax = get_axes(ax, figsize)

    voltages = to_list(voltage)
    currents = to_list(current)
    labels   = to_list(label, n=len(voltages))
    colors   = to_list(color, n=len(voltages))

    for i, (v, c, lbl, clr) in enumerate(zip(voltages, currents, labels, colors)):
        clr = clr or (COLOR_CV if len(voltages) == 1 else COLORS[i % len(COLORS)])
        ax.plot(np.asarray(v), np.asarray(c), color=clr, label=lbl)

    if normalize:
        ylabel = ylabel.replace("(mA)", "(mA g$^{-1}$)")

    fmt_axes(ax, xlabel, ylabel)
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.4)

    if scan_rate:
        ax.text(0.97, 0.97, scan_rate, transform=ax.transAxes,
                ha="right", va="top", fontsize=10)
    if any(l is not None for l in labels):
        ax.legend()

    return fig, ax


def plot_lsv(
    voltage,
    current,
    label=None,
    color=None,
    xlabel="Voltage (V vs. RHE)",
    ylabel="Current density (mA cm$^{-2}$)",
    onset_potential=None,
    ax=None,
    figsize=FIG_SIZE_SINGLE,
):
    """
    Plot one or more linear sweep voltammetry (LSV) curves.

    Parameters
    ----------
    voltage : array-like or list of array-like
    current : array-like or list of array-like
        Current density (mA cm⁻²).
    label : str or list of str, optional
    color : str or list of str, optional
    xlabel, ylabel : str
        Axis labels. Defaults assume RHE reference and mA cm⁻² units.
    onset_potential : float, optional
        Draws a vertical dashed line at this potential to mark the onset.
    ax : matplotlib Axes, optional
    figsize : tuple

    Returns
    -------
    fig, ax

    Examples
    --------
    ::

        fig, ax = plot_lsv(voltage, current,
                           onset_potential=-0.35,
                           label="Catalyst A")
    """
    fig, ax = get_axes(ax, figsize)

    voltages = to_list(voltage)
    currents = to_list(current)
    labels   = to_list(label, n=len(voltages))
    colors   = to_list(color, n=len(voltages))

    for i, (v, c, lbl, clr) in enumerate(zip(voltages, currents, labels, colors)):
        clr = clr or (COLOR_LSV if len(voltages) == 1 else COLORS[i % len(COLORS)])
        ax.plot(np.asarray(v), np.asarray(c), color=clr, label=lbl)

    if onset_potential is not None:
        ax.axvline(onset_potential, color="gray", linewidth=1.0,
                   linestyle="--", label=f"Onset: {onset_potential} V")

    fmt_axes(ax, xlabel, ylabel)
    if any(l is not None for l in labels):
        ax.legend()

    return fig, ax
