"""
echem_plots
===========
Publication-quality electrochemistry plots for battery research.
Provides consistent formatting (font, line width, colors, DPI) across
the entire group so every figure looks the same.

Quick start
-----------
    from echem_plots.style import apply_style
    from echem_plots.plots import plot_cv, plot_charge_discharge

    apply_style()   # call ONCE per script or notebook

    fig, ax = plot_cv(voltage, current, label="5 mV/s")
    fig.savefig("cv.pdf")

Available plots
---------------
    plot_cv               Cyclic Voltammetry
    plot_lsv              Linear Sweep Voltammetry
    plot_eis_nyquist      EIS Nyquist plot
    plot_eis_bode         EIS Bode plot
    plot_charge_discharge Galvanostatic charge-discharge profiles
    plot_coulombic_eff    Coulombic efficiency + capacity vs. cycle
    plot_rate_capability  Rate capability across C-rates
    plot_dqdv             Differential capacity (dQ/dV)

Style
-----
All formatting constants live in echem_plots/style.py.
Edit that file to change font, line width, colors, or DPI for every plot.
"""

__version__ = "0.1.0"

from .style import apply_style
from .plots import (
    plot_cv,
    plot_lsv,
    plot_eis_nyquist,
    plot_eis_bode,
    plot_charge_discharge,
    plot_coulombic_eff,
    plot_rate_capability,
    plot_dqdv,
)

__all__ = [
    "apply_style",
    "plot_cv",
    "plot_lsv",
    "plot_eis_nyquist",
    "plot_eis_bode",
    "plot_charge_discharge",
    "plot_coulombic_eff",
    "plot_rate_capability",
    "plot_dqdv",
]
