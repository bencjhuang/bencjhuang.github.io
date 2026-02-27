"""
echem_plots/plots/eis.py
Electrochemical Impedance Spectroscopy (EIS) plots:
  - Nyquist plot (-Z'' vs. Z')
  - Bode plot (|Z| and phase vs. frequency)
"""

import numpy as np
import matplotlib.pyplot as plt
from ..style import (
    COLORS, FIG_SIZE_SQUARE, FIG_SIZE_DUAL, COLOR_EIS,
    LINE_WIDTH, MARKER_SIZE,
)
from ._helpers import get_axes, fmt_axes, to_list


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
        Real part of impedance (Ω).
    z_imag : array-like or list of array-like
        Imaginary part of impedance (Ω). Pass as **positive** values;
        the function negates automatically to plot -Z'' on the y-axis.
    label : str or list of str, optional
    color : str or list of str, optional
    fit_z_real, fit_z_imag : array-like, optional
        Equivalent-circuit fit data, plotted as a solid line over the points.
    xlabel, ylabel : str
    equal_aspect : bool
        Forces equal x/y scaling so semicircles are not distorted.
    ax : matplotlib Axes, optional
    figsize : tuple

    Returns
    -------
    fig, ax

    Examples
    --------
    Single cell::

        fig, ax = plot_eis_nyquist(z_real, z_imag, label="Before cycling")

    Compare two cells::

        fig, ax = plot_eis_nyquist(
            [zr_a, zr_b], [zi_a, zi_b], label=["Cell A", "Cell B"]
        )

    With equivalent-circuit fit::

        fig, ax = plot_eis_nyquist(z_real, z_imag,
                                   fit_z_real=fit_zr, fit_z_imag=fit_zi)
    """
    fig, ax = get_axes(ax, figsize)

    zr_list = to_list(z_real)
    zi_list = to_list(z_imag)
    labels  = to_list(label, n=len(zr_list))
    colors  = to_list(color, n=len(zr_list))

    for i, (zr, zi, lbl, clr) in enumerate(zip(zr_list, zi_list, labels, colors)):
        clr = clr or (COLOR_EIS if len(zr_list) == 1 else COLORS[i % len(COLORS)])
        ax.plot(np.asarray(zr), np.asarray(zi),
                marker="o", linestyle="none",
                markersize=MARKER_SIZE, color=clr, label=lbl)

    if fit_z_real is not None and fit_z_imag is not None:
        ax.plot(np.asarray(fit_z_real), np.asarray(fit_z_imag),
                color="black", linewidth=LINE_WIDTH * 0.9,
                linestyle="-", label="Fit")

    fmt_axes(ax, xlabel, ylabel)
    if equal_aspect:
        ax.set_aspect("equal", adjustable="box")
    if any(l is not None for l in labels):
        ax.legend()

    return fig, ax


def plot_eis_bode(
    frequency,
    z_magnitude,
    z_phase,
    label=None,
    color=None,
    figsize=FIG_SIZE_DUAL,
):
    """
    Plot EIS data as a Bode plot: |Z| and phase angle vs. frequency.
    Creates two side-by-side panels automatically.

    Parameters
    ----------
    frequency : array-like or list of array-like
        Frequency in Hz.
    z_magnitude : array-like or list of array-like
        |Z| in Ω.
    z_phase : array-like or list of array-like
        Phase angle in degrees. Pass raw values (typically negative
        for capacitive systems).
    label : str or list of str, optional
    color : str or list of str, optional
    figsize : tuple
        Total figure size for both panels combined.

    Returns
    -------
    fig : matplotlib Figure
    axes : tuple of (ax_magnitude, ax_phase)

    Examples
    --------
    ::

        z_mag   = np.abs(z)
        z_phase = np.angle(z, deg=True)
        fig, (ax_mag, ax_phase) = plot_eis_bode(freq, z_mag, z_phase)
    """
    fig, (ax_mag, ax_phase) = plt.subplots(1, 2, figsize=figsize)

    freqs  = to_list(frequency)
    zmags  = to_list(z_magnitude)
    zphas  = to_list(z_phase)
    labels = to_list(label, n=len(freqs))
    colors = to_list(color, n=len(freqs))

    for i, (f, zm, zp, lbl, clr) in enumerate(zip(freqs, zmags, zphas, labels, colors)):
        clr = clr or (COLOR_EIS if len(freqs) == 1 else COLORS[i % len(COLORS)])
        f = np.asarray(f)
        ax_mag.loglog(f, np.asarray(zm),
                      marker="o", markersize=MARKER_SIZE,
                      linestyle="-", color=clr, label=lbl)
        ax_phase.semilogx(f, np.asarray(zp),
                          marker="o", markersize=MARKER_SIZE,
                          linestyle="-", color=clr, label=lbl)

    # Label axes; skip minor locator on log axes (it causes a matplotlib warning)
    ax_mag.set_xlabel("Frequency (Hz)")
    ax_mag.set_ylabel("|Z| (Ω)")
    ax_phase.set_xlabel("Frequency (Hz)")
    ax_phase.set_ylabel("Phase angle (°)")

    if any(l is not None for l in labels):
        ax_mag.legend()

    fig.tight_layout()
    return fig, (ax_mag, ax_phase)
