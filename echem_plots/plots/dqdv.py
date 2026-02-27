"""
echem_plots/plots/dqdv.py
Differential capacity plot (dQ/dV vs. voltage).
"""

import numpy as np
from ..style import COLORS, FIG_SIZE_SINGLE
from ._helpers import get_axes, fmt_axes, to_list


def plot_dqdv(
    voltage,
    dqdv,
    label=None,
    color=None,
    xlabel="Voltage (V vs. Li/Li$^+$)",
    ylabel="d$Q$/d$V$ (mAh g$^{-1}$ V$^{-1}$)",
    ax=None,
    figsize=FIG_SIZE_SINGLE,
):
    """
    Plot differential capacity (dQ/dV) vs. voltage.

    Peaks in the dQ/dV curve correspond to electrochemical reactions
    and phase transitions. Useful for tracking peak shift/fade with cycling.

    Parameters
    ----------
    voltage : array-like or list of array-like
        Voltage data (V).
    dqdv : array-like or list of array-like
        Differential capacity (mAh g⁻¹ V⁻¹).
    label : str or list of str, optional
        Legend label(s), e.g. cycle numbers.
    color : str or list of str, optional
        Line color(s).
    xlabel, ylabel : str
    ax : matplotlib Axes, optional
    figsize : tuple

    Returns
    -------
    fig, ax

    Examples
    --------
    Overlay charge and discharge dQ/dV::

        fig, ax = plot_dqdv(
            [v_chg, v_dis],
            [dqdv_chg, dqdv_dis],
            label=["Charge", "Discharge"],
        )

    Evolution over cycling::

        fig, ax = plot_dqdv(
            [v_cyc1, v_cyc50, v_cyc100],
            [dqdv1,  dqdv50,  dqdv100],
            label=["Cycle 1", "Cycle 50", "Cycle 100"],
        )
    """
    fig, ax = get_axes(ax, figsize)

    volts  = to_list(voltage)
    dqdvs  = to_list(dqdv)
    labels = to_list(label, n=len(volts))
    colors = to_list(color, n=len(volts))

    for i, (v, d, lbl, clr) in enumerate(zip(volts, dqdvs, labels, colors)):
        clr = clr or COLORS[i % len(COLORS)]
        ax.plot(np.asarray(v), np.asarray(d), color=clr, label=lbl)

    ax.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.4)
    fmt_axes(ax, xlabel, ylabel)
    if any(l is not None for l in labels):
        ax.legend()

    return fig, ax
