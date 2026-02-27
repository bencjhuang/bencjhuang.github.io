"""
echem_plots/plots/_helpers.py
Shared internal utilities used by all technique modules.
Not part of the public API.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def get_axes(ax, figsize):
    """Return (fig, ax), creating a new figure if ax is None."""
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()
    return fig, ax


def fmt_axes(ax, xlabel, ylabel):
    """Apply standard axis labels and auto minor ticks."""
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())


def to_list(x, n=None):
    """
    Normalize input to a list of length n.

    Rules
    -----
    - None              → [None, None, ...]
    - str / scalar      → [x, x, ...]   repeated n times
    - 1-D np.ndarray    → [x]           single curve
    - 2-D np.ndarray    → list of rows
    - list of arrays    → returned as-is (multiple curves)
    - flat list, n given  → returned as-is (list of labels/colors)
    - flat list, n absent → [x]           single data curve
    """
    if x is None:
        return [None] * (n or 1)
    if isinstance(x, (str, int, float)):
        return [x] * (n or 1)
    if isinstance(x, np.ndarray):
        if x.ndim == 1:
            return [x]
        return list(x)
    if isinstance(x, list):
        if len(x) > 0 and isinstance(x[0], (np.ndarray, list)):
            return x          # list of data arrays → multiple curves
        if n is not None:
            return x          # flat list with n given → list of labels/colors
        return [x]            # flat list, no n → single data curve
    return [x]
