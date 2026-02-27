"""
echem_plots
===========
Electrochemistry plotting library for battery research.
Provides consistent, publication-quality figures for the group.

Quick start
-----------
    from echem_plots.style import apply_style
    from echem_plots.plots import (
        plot_cv,
        plot_lsv,
        plot_eis_nyquist,
        plot_eis_bode,
        plot_charge_discharge,
        plot_coulombic_eff,
        plot_rate_capability,
        plot_dqdv,
    )

    apply_style()   # call once per script or notebook

Available plots
---------------
  plot_cv               Cyclic Voltammetry
  plot_lsv              Linear Sweep Voltammetry
  plot_eis_nyquist      EIS Nyquist plot
  plot_eis_bode         EIS Bode plot
  plot_charge_discharge Galvanostatic charge-discharge profiles
  plot_coulombic_eff    Coulombic efficiency + capacity vs. cycle
  plot_rate_capability  Rate capability
  plot_dqdv             Differential capacity dQ/dV

Edit style
----------
  All formatting constants (font, line width, colors, DPI, figure size)
  live in echem_plots/style.py.  Change them there and every plot updates.
"""

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
