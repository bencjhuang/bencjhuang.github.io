"""
echem_plots/style.py
====================
Global style settings for all electrochemistry plots.
Edit this file to change the look of ALL plots across the group.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------
FONT_FAMILY = "Arial"          # Change to "Helvetica", "DejaVu Sans", etc.
FONT_SIZE_LABEL = 14           # Axis labels (e.g., "Voltage (V)")
FONT_SIZE_TICK = 12            # Tick mark numbers
FONT_SIZE_LEGEND = 11          # Legend text
FONT_SIZE_TITLE = 14           # Optional subplot titles

# ---------------------------------------------------------------------------
# Line & Marker
# ---------------------------------------------------------------------------
LINE_WIDTH = 1.8               # Main data lines
AXIS_LINE_WIDTH = 1.2          # Spine / frame line width
TICK_LENGTH_MAJOR = 5          # Major tick length (pt)
TICK_LENGTH_MINOR = 3          # Minor tick length (pt)
MARKER_SIZE = 5                # Default marker size

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
FIGURE_DPI = 300               # DPI for saved figures (publication quality)
FIGURE_FORMAT = "pdf"          # Default save format: "pdf", "svg", "png"

# Default figure sizes (width, height) in inches
FIG_SIZE_SINGLE  = (4.5, 3.5)  # Single-panel plot
FIG_SIZE_WIDE    = (6.5, 3.5)  # Wide single-panel (e.g., charge-discharge)
FIG_SIZE_DUAL    = (9.0, 3.5)  # Two-panel side by side
FIG_SIZE_SQUARE  = (4.0, 4.0)  # Square (e.g., Nyquist)

# ---------------------------------------------------------------------------
# Color palette  (publication-friendly, colorblind-safe)
# ---------------------------------------------------------------------------
# Primary palette — used when cycling through datasets
COLORS = [
    "#1B4F72",  # Deep navy blue
    "#C0392B",  # Brick red
    "#1E8449",  # Forest green
    "#D68910",  # Amber
    "#6C3483",  # Purple
    "#117A65",  # Teal
    "#BA4A00",  # Burnt orange
    "#2E86C1",  # Steel blue
    "#839192",  # Slate gray
    "#1A5276",  # Dark blue alt
]

# Named single-color aliases for common use cases
COLOR_CV    = "#1B4F72"   # Cyclic voltammetry curves
COLOR_LSV   = "#C0392B"   # LSV curves
COLOR_EIS   = "#1E8449"   # EIS data points
COLOR_CD_ODD  = "#1B4F72"   # Charge curves
COLOR_CD_EVEN = "#C0392B"   # Discharge curves
COLOR_CE    = "#C0392B"   # Coulombic efficiency markers
COLOR_CAP   = "#1B4F72"   # Capacity markers

# ---------------------------------------------------------------------------
# apply_style()  — call once at the top of any script
# ---------------------------------------------------------------------------

def apply_style():
    """
    Apply the group's global matplotlib style.
    Call this once at the start of your script or notebook.

    Example
    -------
    from echem_plots.style import apply_style
    apply_style()
    """
    mpl.rcParams.update({
        # Font
        "font.family":           FONT_FAMILY,
        "font.size":             FONT_SIZE_TICK,
        "axes.labelsize":        FONT_SIZE_LABEL,
        "axes.titlesize":        FONT_SIZE_TITLE,
        "xtick.labelsize":       FONT_SIZE_TICK,
        "ytick.labelsize":       FONT_SIZE_TICK,
        "legend.fontsize":       FONT_SIZE_LEGEND,

        # Lines
        "lines.linewidth":       LINE_WIDTH,
        "lines.markersize":      MARKER_SIZE,

        # Axes frame
        "axes.linewidth":        AXIS_LINE_WIDTH,
        "axes.spines.top":       False,
        "axes.spines.right":     False,

        # Ticks
        "xtick.direction":       "in",
        "ytick.direction":       "in",
        "xtick.major.size":      TICK_LENGTH_MAJOR,
        "ytick.major.size":      TICK_LENGTH_MAJOR,
        "xtick.minor.size":      TICK_LENGTH_MINOR,
        "ytick.minor.size":      TICK_LENGTH_MINOR,
        "xtick.major.width":     AXIS_LINE_WIDTH,
        "ytick.major.width":     AXIS_LINE_WIDTH,
        "xtick.minor.width":     AXIS_LINE_WIDTH * 0.8,
        "ytick.minor.width":     AXIS_LINE_WIDTH * 0.8,
        "xtick.top":             False,
        "ytick.right":           False,

        # Figure
        "figure.dpi":            100,          # screen DPI (savefig uses FIGURE_DPI)
        "savefig.dpi":           FIGURE_DPI,
        "savefig.bbox":          "tight",
        "savefig.format":        FIGURE_FORMAT,

        # Legend
        "legend.frameon":        False,
        "legend.loc":            "best",

        # Color cycle
        "axes.prop_cycle":       mpl.cycler(color=COLORS),
    })
