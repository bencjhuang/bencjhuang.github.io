"""
echem_plots/plots.py
====================
All electrochemistry plotting functions for battery research.

Available functions
-------------------
  plot_cv               -- Cyclic Voltammetry (I vs. V)
  plot_lsv              -- Linear Sweep Voltammetry (I vs. V)
  plot_eis_nyquist      -- EIS Nyquist plot (-Z'' vs. Z')
  plot_eis_bode         -- EIS Bode plot (|Z| and phase vs. frequency)
  plot_charge_discharge -- Voltage vs. specific capacity or time
  plot_coulombic_eff    -- Coulombic efficiency + capacity vs. cycle number
  plot_rate_capability  -- Capacity vs. cycle number at multiple C-rates
  plot_dqdv             -- Differential capacity (dQ/dV vs. V)

Each function returns (fig, ax) or (fig, axes) so you can further customize
or save with fig.savefig("name.pdf").

Quick start
-----------
    from echem_plots.style import apply_style
    from echem_plots.plots import plot_cv

    apply_style()          # call ONCE per script / notebook
    fig, ax = plot_cv(voltage, current, label="3 mV/s")
    fig.savefig("cv.pdf")
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from .style import (
    COLORS, FIG_SIZE_SINGLE, FIG_SIZE_WIDE, FIG_SIZE_DUAL, FIG_SIZE_SQUARE,
    COLOR_CV, COLOR_LSV, COLOR_EIS, COLOR_CD_ODD, COLOR_CD_EVEN,
    COLOR_CE, COLOR_CAP, LINE_WIDTH, MARKER_SIZE,
)


# ===========================================================================
# 1. Cyclic Voltammetry (CV)
# ===========================================================================

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
    Plot a single CV or overlay multiple CVs on one axes.

    Parameters
    ----------
    voltage : array-like or list of array-like
        Voltage data. Pass a list to overlay multiple scans.
    current : array-like or list of array-like
        Current data. Must match shape of `voltage`.
    label : str or list of str, optional
        Legend label(s).
    color : str or list of str, optional
        Line color(s). Cycles through group palette if None.
    xlabel, ylabel : str
        Axis labels.
    normalize : bool
        If True, divide current by electrode mass (you provide current as
        mA/g already) — just a labeling convenience flag.
    scan_rate : str, optional
        Annotates scan rate on plot, e.g. "5 mV/s".
    ax : matplotlib Axes, optional
        Plot into an existing Axes; creates a new figure if None.
    figsize : tuple
        Figure size in inches.

    Returns
    -------
    fig, ax
    """
    fig, ax = _get_axes(ax, figsize)

    voltages = _to_list(voltage)
    currents = _to_list(current)
    labels   = _to_list(label,  n=len(voltages))
    colors   = _to_list(color,  n=len(voltages))

    for i, (v, c, lbl, clr) in enumerate(zip(voltages, currents, labels, colors)):
        clr = clr or (COLOR_CV if len(voltages) == 1 else COLORS[i % len(COLORS)])
        ax.plot(np.asarray(v), np.asarray(c), color=clr, label=lbl)

    if normalize:
        ylabel = ylabel.replace("(mA)", "(mA g$^{-1}$)")

    _fmt_axes(ax, xlabel, ylabel)
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.4)

    if scan_rate:
        ax.text(0.97, 0.97, scan_rate, transform=ax.transAxes,
                ha="right", va="top", fontsize=10)
    if any(l is not None for l in labels):
        ax.legend()
    return fig, ax


# ===========================================================================
# 2. Linear Sweep Voltammetry (LSV)
# ===========================================================================

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
    Plot one or more LSV curves.

    Parameters
    ----------
    onset_potential : float, optional
        Draws a vertical dashed line at this potential to mark onset.
    (Other parameters same as plot_cv)

    Returns
    -------
    fig, ax
    """
    fig, ax = _get_axes(ax, figsize)

    voltages = _to_list(voltage)
    currents = _to_list(current)
    labels   = _to_list(label,  n=len(voltages))
    colors   = _to_list(color,  n=len(voltages))

    for i, (v, c, lbl, clr) in enumerate(zip(voltages, currents, labels, colors)):
        clr = clr or (COLOR_LSV if len(voltages) == 1 else COLORS[i % len(COLORS)])
        ax.plot(np.asarray(v), np.asarray(c), color=clr, label=lbl)

    if onset_potential is not None:
        ax.axvline(onset_potential, color="gray", linewidth=1.0,
                   linestyle="--", label=f"Onset: {onset_potential} V")

    _fmt_axes(ax, xlabel, ylabel)
    if any(l is not None for l in labels):
        ax.legend()
    return fig, ax


# ===========================================================================
# 3. EIS — Nyquist Plot
# ===========================================================================

def plot_eis_nyquist(
    z_real,
    z_imag,
    label=None,
    color=None,
    fit_z_real=None,
    fit_z_imag=None,
    xlabel="Z$'$ (Ω)",
    ylabel="-Z$''$ (Ω)",
    equal_aspect=True,
    ax=None,
    figsize=FIG_SIZE_SQUARE,
):
    """
    Plot EIS data as a Nyquist plot (-Z'' vs. Z').

    Parameters
    ----------
    z_real : array-like or list of array-like
        Real part of impedance (Ω). Positive values.
    z_imag : array-like or list of array-like
        Imaginary part of impedance (Ω). Pass as positive values;
        the function negates them automatically for convention.
    fit_z_real, fit_z_imag : array-like, optional
        Fitted impedance data plotted as a line over the data points.
    equal_aspect : bool
        If True, forces equal axis scaling so the semicircle is not distorted.

    Returns
    -------
    fig, ax
    """
    fig, ax = _get_axes(ax, figsize)

    zr_list  = _to_list(z_real)
    zi_list  = _to_list(z_imag)
    labels   = _to_list(label, n=len(zr_list))
    colors   = _to_list(color, n=len(zr_list))

    for i, (zr, zi, lbl, clr) in enumerate(zip(zr_list, zi_list, labels, colors)):
        clr = clr or (COLOR_EIS if len(zr_list) == 1 else COLORS[i % len(COLORS)])
        ax.plot(np.asarray(zr), np.asarray(zi),
                marker="o", linestyle="none",
                markersize=MARKER_SIZE, color=clr, label=lbl)

    if fit_z_real is not None and fit_z_imag is not None:
        ax.plot(np.asarray(fit_z_real), np.asarray(fit_z_imag),
                color="black", linewidth=LINE_WIDTH * 0.9,
                linestyle="-", label="Fit")

    _fmt_axes(ax, xlabel, ylabel)
    if equal_aspect:
        ax.set_aspect("equal", adjustable="box")
    if any(l is not None for l in labels):
        ax.legend()
    return fig, ax


# ===========================================================================
# 4. EIS — Bode Plot
# ===========================================================================

def plot_eis_bode(
    frequency,
    z_magnitude,
    z_phase,
    label=None,
    color=None,
    ax=None,
    figsize=FIG_SIZE_DUAL,
):
    """
    Plot EIS data as a Bode plot: |Z| and phase angle vs. frequency.
    Creates two side-by-side panels.

    Parameters
    ----------
    frequency : array-like or list of array-like
        Frequency in Hz.
    z_magnitude : array-like or list of array-like
        |Z| in Ω.
    z_phase : array-like or list of array-like
        Phase angle in degrees (typically negative for capacitive systems;
        pass raw values and the function plots as-is).
    label : str or list of str, optional
    color : str or list of str, optional

    Returns
    -------
    fig, (ax_mag, ax_phase)
    """
    if ax is None:
        fig, (ax_mag, ax_phase) = plt.subplots(1, 2, figsize=figsize)
    else:
        raise ValueError("For Bode plots, leave ax=None to auto-create two panels.")

    freqs  = _to_list(frequency)
    zmags  = _to_list(z_magnitude)
    zphas  = _to_list(z_phase)
    labels = _to_list(label, n=len(freqs))
    colors = _to_list(color, n=len(freqs))

    for i, (f, zm, zp, lbl, clr) in enumerate(zip(freqs, zmags, zphas, labels, colors)):
        clr = clr or (COLOR_EIS if len(freqs) == 1 else COLORS[i % len(COLORS)])
        f   = np.asarray(f)
        ax_mag.loglog(f, np.asarray(zm),
                      marker="o", markersize=MARKER_SIZE,
                      linestyle="-", color=clr, label=lbl)
        ax_phase.semilogx(f, np.asarray(zp),
                          marker="o", markersize=MARKER_SIZE,
                          linestyle="-", color=clr, label=lbl)

    _fmt_axes(ax_mag,   "Frequency (Hz)", "|Z| (Ω)")
    _fmt_axes(ax_phase, "Frequency (Hz)", "Phase angle (°)")

    if any(l is not None for l in labels):
        ax_mag.legend()

    fig.tight_layout()
    return fig, (ax_mag, ax_phase)


# ===========================================================================
# 5. Charge–Discharge (Galvanostatic Cycling)
# ===========================================================================

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
    Plot galvanostatic charge–discharge profiles.

    Parameters
    ----------
    capacity : array-like or list of array-like
        Specific capacity (mAh g⁻¹) or time (h). If a list, each element
        is one half-cycle or one full cycle.
    voltage : array-like or list of array-like
        Voltage data matching `capacity`.
    cycle_numbers : list of int or str, optional
        Labels for each curve (e.g., [1, 2, 10, 50, 100]).
        If None, no legend is shown.
    x_is_time : bool
        If True, labels x-axis as "Time (h)" instead of capacity.
    color_charge / color_discharge : str
        Colors for charge and discharge half-cycles when use_cycle_colors=False.
        Alternating curves are assigned these two colors.
    use_cycle_colors : bool
        If True, each cycle (pair of charge/discharge) uses a unique color
        from the group palette instead of alternating blue/red.
    xlabel : str, optional
        Overrides auto x-axis label.

    Returns
    -------
    fig, ax
    """
    fig, ax = _get_axes(ax, figsize)

    caps     = _to_list(capacity)
    volts    = _to_list(voltage)
    n_curves = len(caps)
    labels   = _to_list(cycle_numbers, n=n_curves)

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

    _fmt_axes(ax, xlabel, ylabel)
    if any(l is not None for l in labels):
        ax.legend()
    return fig, ax


# ===========================================================================
# 6. Coulombic Efficiency + Capacity vs. Cycle Number
# ===========================================================================

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
    Creates a dual y-axis plot: capacity on left, CE% on right.

    Parameters
    ----------
    cycle_number : array-like
        Cycle indices.
    charge_capacity : array-like
        Charge capacity at each cycle (mAh g⁻¹).
    discharge_capacity : array-like
        Discharge capacity at each cycle (mAh g⁻¹).
    coulombic_efficiency : array-like, optional
        CE values (%). Auto-computed as discharge/charge * 100 if None.
    ce_ylim : tuple
        y-axis limits for CE panel, default (0, 110).

    Returns
    -------
    fig, (ax_cap, ax_ce)
    """
    fig, ax_cap = _get_axes(ax, figsize)

    cycles   = np.asarray(cycle_number)
    q_chg    = np.asarray(charge_capacity)
    q_dis    = np.asarray(discharge_capacity)

    if coulombic_efficiency is None:
        ce = np.where(q_chg > 0, q_dis / q_chg * 100, np.nan)
    else:
        ce = np.asarray(coulombic_efficiency)

    # Capacity
    ax_cap.plot(cycles, q_chg, marker="^", color=color_charge,
                linestyle="-", label="Charge capacity")
    ax_cap.plot(cycles, q_dis, marker="o", color=color_discharge,
                linestyle="-", label="Discharge capacity")
    _fmt_axes(ax_cap, xlabel, ylabel_cap)

    # CE on secondary y-axis
    ax_ce = ax_cap.twinx()
    ax_ce.plot(cycles, ce, marker="s", color=color_ce,
               linestyle="--", markersize=MARKER_SIZE * 0.8,
               label="Coulombic eff.")
    ax_ce.set_ylabel(ylabel_ce, fontsize=14)
    ax_ce.tick_params(axis="y", labelsize=12)
    ax_ce.set_ylim(ce_ylim)

    # Combined legend
    handles1, labels1 = ax_cap.get_legend_handles_labels()
    handles2, labels2 = ax_ce.get_legend_handles_labels()
    ax_cap.legend(handles1 + handles2, labels1 + labels2, loc="best")

    return fig, (ax_cap, ax_ce)


# ===========================================================================
# 7. Rate Capability
# ===========================================================================

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
    Plot rate capability: capacity vs. cycle number with C-rate annotations.

    Parameters
    ----------
    cycle_number : array-like or list of array-like
        Cycle indices. Pass a list to plot multiple C-rate segments separately.
    capacity : array-like or list of array-like
        Capacity at each cycle.
    c_rates : list of str, optional
        C-rate labels for each segment, e.g. ["0.1C", "0.2C", "0.5C", "1C", "0.1C"].
        Length must match number of segments.

    Returns
    -------
    fig, ax
    """
    fig, ax = _get_axes(ax, figsize)

    cycles_list = _to_list(cycle_number)
    cap_list    = _to_list(capacity)
    n_seg       = len(cycles_list)
    rate_labels = c_rates if c_rates is not None else [None] * n_seg

    for i, (cyc, cap, rate) in enumerate(zip(cycles_list, cap_list, rate_labels)):
        clr = COLORS[i % len(COLORS)]
        ax.plot(np.asarray(cyc), np.asarray(cap),
                marker="o", color=clr, linestyle="-", label=rate)

    _fmt_axes(ax, xlabel, ylabel)
    if c_rates is not None:
        ax.legend(title="C-rate")
    return fig, ax


# ===========================================================================
# 8. Differential Capacity (dQ/dV)
# ===========================================================================

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
    Peaks correspond to electrochemical reactions / phase transitions.

    Parameters
    ----------
    voltage : array-like or list of array-like
    dqdv : array-like or list of array-like
        dQ/dV values (mAh g⁻¹ V⁻¹).
    label : str or list of str, optional
    color : str or list of str, optional

    Returns
    -------
    fig, ax
    """
    fig, ax = _get_axes(ax, figsize)

    volts  = _to_list(voltage)
    dqdvs  = _to_list(dqdv)
    labels = _to_list(label, n=len(volts))
    colors = _to_list(color, n=len(volts))

    for i, (v, d, lbl, clr) in enumerate(zip(volts, dqdvs, labels, colors)):
        clr = clr or COLORS[i % len(COLORS)]
        ax.plot(np.asarray(v), np.asarray(d), color=clr, label=lbl)

    ax.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.4)
    _fmt_axes(ax, xlabel, ylabel)
    if any(l is not None for l in labels):
        ax.legend()
    return fig, ax


# ===========================================================================
# Internal helpers (not part of public API)
# ===========================================================================

def _get_axes(ax, figsize):
    """Return (fig, ax), creating a new figure if ax is None."""
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()
    return fig, ax


def _fmt_axes(ax, xlabel, ylabel):
    """Apply standard axis labels and minor ticks."""
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())


def _to_list(x, n=None):
    """
    Normalize input to a list of length n.
    - None  → [None, None, ...]
    - str / scalar → [x, x, ...]  (repeated n times)
    - list  → return as-is (or padded with None to length n)
    - array → [x]
    """
    if x is None:
        return [None] * (n or 1)
    if isinstance(x, (str, int, float)):
        return [x] * (n or 1)
    if isinstance(x, np.ndarray):
        # Single array — is it 1-D data or a list of arrays?
        if x.ndim == 1:
            return [x]
        return list(x)  # 2-D: treat rows as separate curves
    if isinstance(x, list):
        # Check if it's a list of arrays vs. a flat list of numbers
        if len(x) > 0 and isinstance(x[0], (np.ndarray, list)):
            return x  # already a list of curves
        # It's a flat list → one curve
        return [x]
    return [x]
