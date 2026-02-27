# echem_plots

Publication-quality electrochemistry plots for battery research.
Every student uses the same fonts, line widths, colors, and figure sizes.

---

## Setup (one-time, per computer)

```bash
# 1. Clone the repo (or pull the latest version)
git clone https://github.com/bencjhuang/bencjhuang.github.io.git
cd bencjhuang.github.io

# 2. Install dependencies
pip install -r echem_plots/requirements.txt
```

> **Tip:** use a virtual environment or conda environment to keep dependencies clean.

---

## How to use in your script

```python
# --- at the top of every script ---
from echem_plots.style import apply_style
from echem_plots.plots import plot_cv, plot_charge_discharge  # import what you need

apply_style()   # call ONCE — applies the group style to all subsequent plots
```

### Cyclic Voltammetry (CV)

```python
import numpy as np
from echem_plots.style import apply_style
from echem_plots.plots import plot_cv

apply_style()

voltage = np.loadtxt("my_cv.txt", usecols=0)
current = np.loadtxt("my_cv.txt", usecols=1)   # mA

fig, ax = plot_cv(voltage, current, label="5 mV/s", scan_rate="5 mV/s")
fig.savefig("cv.pdf")
```

**Overlay multiple scan rates:**

```python
fig, ax = plot_cv(
    [v1, v2, v3],
    [i1, i2, i3],
    label=["1 mV/s", "5 mV/s", "10 mV/s"],
)
```

---

### Linear Sweep Voltammetry (LSV)

```python
from echem_plots.plots import plot_lsv

fig, ax = plot_lsv(voltage, current,
                   onset_potential=-0.35,
                   xlabel="Voltage (V vs. RHE)",
                   ylabel="Current density (mA cm$^{-2}$)")
fig.savefig("lsv.pdf")
```

---

### EIS — Nyquist Plot

```python
from echem_plots.plots import plot_eis_nyquist

# z_real and z_imag are in Ω; pass z_imag as positive values
fig, ax = plot_eis_nyquist(z_real, z_imag, label="Before cycling")
fig.savefig("eis_nyquist.pdf")
```

**Compare two cells:**

```python
fig, ax = plot_eis_nyquist(
    [zr_cell1, zr_cell2],
    [zi_cell1, zi_cell2],
    label=["Cell A", "Cell B"],
)
```

---

### EIS — Bode Plot

```python
from echem_plots.plots import plot_eis_bode

z_mag   = abs(z)          # |Z| in Ω
z_phase = np.angle(z, deg=True)

fig, (ax_mag, ax_phase) = plot_eis_bode(frequency, z_mag, z_phase)
fig.savefig("eis_bode.pdf")
```

---

### Charge–Discharge Profiles

```python
from echem_plots.plots import plot_charge_discharge

# Pass alternating charge/discharge half-cycles as lists
# cycle_numbers labels the charge half-cycle of each pair
fig, ax = plot_charge_discharge(
    capacity=[q_chg1, q_dis1, q_chg2, q_dis2, q_chg50, q_dis50],
    voltage =[v_chg1, v_dis1, v_chg2, v_dis2, v_chg50, v_dis50],
    cycle_numbers=[1, None, 2, None, 50, None],
)
fig.savefig("charge_discharge.pdf")
```

---

### Coulombic Efficiency

```python
from echem_plots.plots import plot_coulombic_eff

fig, (ax_cap, ax_ce) = plot_coulombic_eff(
    cycle_number      = cycles,
    charge_capacity   = q_charge,
    discharge_capacity= q_discharge,
)
fig.savefig("coulombic_efficiency.pdf")
```

---

### Rate Capability

```python
from echem_plots.plots import plot_rate_capability

fig, ax = plot_rate_capability(
    cycle_number = [cyc_01c, cyc_02c, cyc_05c, cyc_1c, cyc_01c_recovery],
    capacity     = [cap_01c, cap_02c, cap_05c, cap_1c, cap_01c_recovery],
    c_rates      = ["0.1C", "0.2C", "0.5C", "1C", "0.1C (recovery)"],
)
fig.savefig("rate_capability.pdf")
```

---

### Differential Capacity (dQ/dV)

```python
from echem_plots.plots import plot_dqdv

fig, ax = plot_dqdv(voltage, dqdv, label="Cycle 1")
fig.savefig("dqdv.pdf")
```

---

## Changing the group style

Open **`echem_plots/style.py`** and edit the constants at the top.
All plots will automatically update — no changes to plot functions needed.

| Variable | What it controls |
|---|---|
| `FONT_FAMILY` | Font (Arial, Helvetica, etc.) |
| `FONT_SIZE_LABEL` | Axis label font size |
| `FONT_SIZE_TICK` | Tick number font size |
| `LINE_WIDTH` | Data line thickness |
| `FIGURE_DPI` | Resolution for saved figures |
| `FIGURE_FORMAT` | Default save format (pdf / svg / png) |
| `COLORS` | Ordered color palette |
| `FIG_SIZE_SINGLE` etc. | Figure dimensions |

---

## Run the example

```bash
cd bencjhuang.github.io
python echem_plots/examples/example_all_plots.py
```

This generates PDF files for all 8 plot types using synthetic data.

---

## File structure

```
echem_plots/
├── __init__.py        # Entry point — imports everything
├── style.py           # ALL style settings (edit this to change look)
├── plots.py           # All plotting functions
├── requirements.txt   # Python dependencies
├── README.md          # This file
└── examples/
    └── example_all_plots.py   # Full demo with synthetic data
```

---

## Does this affect the website?

**No.** GitHub Pages (which hosts bencjhuang.github.io) only reads `.html`, `.css`,
and `.js` files from the root of the repository.  Python files in a subfolder
are completely ignored by the web server.
