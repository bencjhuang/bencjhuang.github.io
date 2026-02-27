# echem-plots

Publication-quality electrochemistry plots for battery research.
Every student in the group uses the same font, line widths, colors, and figure sizes —
change one file (`style.py`) and every plot updates automatically.

---

## Setup

### Option A — pip install (recommended)

```bash
git clone https://github.com/<your-group>/echem-plots.git
cd echem-plots
pip install -e .
```

The `-e` flag installs in "editable" mode: any time you `git pull` to get new plot types,
they are immediately available without reinstalling.

### Option B — run without installing

```bash
git clone https://github.com/<your-group>/echem-plots.git
```

Then at the top of your script:

```python
import sys
sys.path.insert(0, "/path/to/echem-plots")
```

---

## Quick start

```python
from echem_plots.style import apply_style
from echem_plots.plots import plot_cv, plot_charge_discharge

apply_style()   # call ONCE per script or notebook

fig, ax = plot_cv(voltage, current, label="5 mV/s")
fig.savefig("cv.pdf")
```

---

## Available plots

| Function | Description |
|---|---|
| `plot_cv` | Cyclic Voltammetry (I vs. V) |
| `plot_lsv` | Linear Sweep Voltammetry (I vs. V) |
| `plot_eis_nyquist` | EIS Nyquist plot (-Z'' vs. Z') |
| `plot_eis_bode` | EIS Bode plot (|Z| and phase vs. frequency) |
| `plot_charge_discharge` | Galvanostatic charge-discharge profiles |
| `plot_coulombic_eff` | Coulombic efficiency + capacity vs. cycle number |
| `plot_rate_capability` | Capacity at multiple C-rates |
| `plot_dqdv` | Differential capacity (dQ/dV vs. V) |

---

## Usage examples

### Cyclic Voltammetry (CV)

```python
from echem_plots.plots import plot_cv

# Single scan
fig, ax = plot_cv(voltage, current, label="5 mV/s", scan_rate="5 mV/s")
fig.savefig("cv.pdf")

# Multiple scan rates overlaid
fig, ax = plot_cv(
    [v1, v2, v3],
    [i1, i2, i3],
    label=["1 mV/s", "5 mV/s", "10 mV/s"],
)
```

### Linear Sweep Voltammetry (LSV)

```python
from echem_plots.plots import plot_lsv

fig, ax = plot_lsv(voltage, current,
                   onset_potential=-0.35,
                   xlabel="Voltage (V vs. RHE)",
                   ylabel="Current density (mA cm$^{-2}$)")
fig.savefig("lsv.pdf")
```

### EIS — Nyquist Plot

```python
from echem_plots.plots import plot_eis_nyquist

# Pass z_imag as positive values; the function plots -Z'' on the y-axis
fig, ax = plot_eis_nyquist(z_real, z_imag, label="Before cycling")

# Compare two cells
fig, ax = plot_eis_nyquist(
    [zr_a, zr_b], [zi_a, zi_b], label=["Cell A", "Cell B"]
)

# With equivalent-circuit fit overlay
fig, ax = plot_eis_nyquist(z_real, z_imag,
                           fit_z_real=fit_zr, fit_z_imag=fit_zi)
fig.savefig("eis_nyquist.pdf")
```

### EIS — Bode Plot

```python
from echem_plots.plots import plot_eis_bode

z_mag   = np.abs(z)
z_phase = np.angle(z, deg=True)

fig, (ax_mag, ax_phase) = plot_eis_bode(frequency, z_mag, z_phase)
fig.savefig("eis_bode.pdf")
```

### Charge–Discharge

```python
from echem_plots.plots import plot_charge_discharge

# Pass alternating charge / discharge half-cycles
# Label the charge half-cycle; pass None for discharge to keep legend clean
fig, ax = plot_charge_discharge(
    capacity=[q_chg1, q_dis1, q_chg2, q_dis2, q_chg50, q_dis50],
    voltage =[v_chg1, v_dis1, v_chg2, v_dis2, v_chg50, v_dis50],
    cycle_numbers=[1, None, 2, None, 50, None],
)
fig.savefig("charge_discharge.pdf")
```

### Coulombic Efficiency

```python
from echem_plots.plots import plot_coulombic_eff

# CE is auto-computed as discharge/charge × 100 if not provided
fig, (ax_cap, ax_ce) = plot_coulombic_eff(
    cycle_number=cycles,
    charge_capacity=q_charge,
    discharge_capacity=q_discharge,
)
fig.savefig("coulombic_efficiency.pdf")
```

### Rate Capability

```python
from echem_plots.plots import plot_rate_capability

fig, ax = plot_rate_capability(
    cycle_number=[cyc_01c, cyc_1c, cyc_5c, cyc_01c_recovery],
    capacity    =[cap_01c, cap_1c, cap_5c, cap_01c_recovery],
    c_rates     =["0.1C", "1C", "5C", "0.1C (recovery)"],
)
fig.savefig("rate_capability.pdf")
```

### Differential Capacity (dQ/dV)

```python
from echem_plots.plots import plot_dqdv

fig, ax = plot_dqdv(
    [v_chg, v_dis],
    [dqdv_chg, dqdv_dis],
    label=["Charge", "Discharge"],
)
fig.savefig("dqdv.pdf")
```

---

## Changing the group style

Open `echem_plots/style.py` and edit the constants at the top.
**All plots update automatically — no other file needs to be touched.**

| Constant | Controls |
|---|---|
| `FONT_FAMILY` | Font (Arial, Helvetica, etc.) |
| `FONT_SIZE_LABEL` | Axis label size |
| `FONT_SIZE_TICK` | Tick number size |
| `LINE_WIDTH` | Data line thickness |
| `FIGURE_DPI` | Resolution for saved figures |
| `FIGURE_FORMAT` | Default save format (`"pdf"`, `"svg"`, `"png"`) |
| `COLORS` | Ordered color palette (10 colors) |
| `FIG_SIZE_SINGLE` etc. | Figure dimensions in inches |

---

## Adding a new plot type

1. Put the function in the right technique file under `echem_plots/plots/`:
   - `cv_lsv.py` — CV, LSV, EQCM-CV
   - `eis.py` — any impedance plots
   - `battery.py` — GITT, cycling, rate
   - `dqdv.py` — differential capacity
2. Follow the pattern: `def plot_xxx(..., ax=None, figsize=FIG_SIZE_SINGLE): ... return fig, ax`
3. Export it in `echem_plots/plots/__init__.py` and `echem_plots/__init__.py`
4. Add an example block to `examples/example_all_plots.py`

---

## Run the demo

```bash
python examples/example_all_plots.py
```

Generates a PDF for every plot type using synthetic data.

---

## Run the tests

```bash
pip install pytest
pytest tests/ -v
```

---

## File structure

```
echem-plots/                        ← repo root
├── README.md
├── LICENSE                         ← MIT
├── pyproject.toml                  ← pip install config
├── .gitignore
├── echem_plots/                    ← the Python package
│   ├── __init__.py                 ← version + public API
│   ├── style.py                    ← ALL style constants (edit this)
│   └── plots/
│       ├── __init__.py             ← re-exports all public functions
│       ├── _helpers.py             ← internal shared utilities
│       ├── cv_lsv.py               ← plot_cv, plot_lsv
│       ├── eis.py                  ← plot_eis_nyquist, plot_eis_bode
│       ├── battery.py              ← plot_charge_discharge,
│       │                              plot_coulombic_eff, plot_rate_capability
│       └── dqdv.py                 ← plot_dqdv
├── examples/
│   └── example_all_plots.py
└── tests/
    ├── test_cv_lsv.py
    ├── test_eis.py
    ├── test_battery.py
    └── test_dqdv.py
```
