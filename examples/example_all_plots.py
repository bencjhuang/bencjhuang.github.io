"""
example_all_plots.py
====================
Demonstration of every echem_plots function using synthetic data.
Run this script to verify the library is working and to see what
each plot looks like before using your real data.

Usage
-----
    python examples/example_all_plots.py

Figures are saved as PDF files in the current directory.
"""

import numpy as np
import sys
import os

# Allow running from the examples/ folder without installing the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

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

# Apply the group style once at the top
apply_style()

# ===========================================================================
# Synthetic data helpers
# ===========================================================================

def make_cv_data(scan_rate=5e-3, v_min=-0.5, v_max=0.5, n=400):
    """Simulate a simple redox CV with a gaussian peak pair."""
    v = np.concatenate([
        np.linspace(v_min, v_max, n // 2),
        np.linspace(v_max, v_min, n // 2),
    ])
    # Gaussian anodic peak at +0.2 V, cathodic peak at -0.2 V
    i_anodic  = 0.5 * np.exp(-((v - 0.2) ** 2) / (2 * 0.04 ** 2))
    i_cathodic = -0.5 * np.exp(-((v + 0.2) ** 2) / (2 * 0.04 ** 2))
    i_cap = 0.05  # capacitive background
    current = (i_anodic + i_cathodic + i_cap) * scan_rate / 5e-3  # scale with rate
    return v, current


def make_eis_data(r_ohm=5, r_ct=80, c_dl=1e-4, n=50):
    """Simulate a Randles circuit: R_ohm + (R_ct || C_dl) + Warburg."""
    freq = np.logspace(5, -2, n)
    omega = 2 * np.pi * freq
    z_rc = r_ct / (1 + 1j * omega * r_ct * c_dl)
    z_warburg = 30 * (1 - 1j) / np.sqrt(omega)
    z = r_ohm + z_rc + z_warburg
    return freq, z.real, -z.imag  # return Z', -Z'' (positive imaginary)


def make_cd_data(n_cycles=3, q_max=160, v_low=2.5, v_high=4.2):
    """Simulate charge–discharge voltage profiles."""
    caps, volts = [], []
    for k in range(n_cycles):
        fade = 1 - 0.03 * k  # 3 % capacity fade per cycle
        q = np.linspace(0, q_max * fade, 200)
        # Charge: sigmoid-ish curve
        v_chg = v_low + (v_high - v_low) * (q / (q_max * fade)) ** 0.4
        # Discharge
        v_dis = v_high - (v_high - v_low) * (q / (q_max * fade)) ** 0.6
        caps.extend([q, q[::-1]])
        volts.extend([v_chg, v_dis])
    return caps, volts


# ===========================================================================
# 1. CV — single scan
# ===========================================================================
print("Plotting CV (single scan)...")
v, i = make_cv_data(scan_rate=5e-3)
fig, ax = plot_cv(v, i * 1000, label="5 mV/s", scan_rate="5 mV/s",
                  ylabel="Current (mA)")
fig.savefig("cv_single.pdf")
print("  → cv_single.pdf")

# ===========================================================================
# 2. CV — multiple scan rates overlaid
# ===========================================================================
print("Plotting CV (multiple scan rates)...")
rates = [1, 2, 5, 10, 20]  # mV/s
v_list, i_list, lbl_list = [], [], []
for r in rates:
    v, i = make_cv_data(scan_rate=r * 1e-3)
    v_list.append(v)
    i_list.append(i * 1000)
    lbl_list.append(f"{r} mV/s")

fig, ax = plot_cv(v_list, i_list, label=lbl_list)
fig.savefig("cv_multi.pdf")
print("  → cv_multi.pdf")

# ===========================================================================
# 3. LSV
# ===========================================================================
print("Plotting LSV...")
v_lsv = np.linspace(-0.1, -0.7, 300)
# Simulate OER-like Tafel behavior
j_lsv = -0.02 * np.exp(10 * (v_lsv + 0.35))
j_lsv = np.clip(j_lsv, -50, 0)

fig, ax = plot_lsv(v_lsv, j_lsv,
                   label="Catalyst A",
                   onset_potential=-0.35,
                   xlabel="Voltage (V vs. RHE)",
                   ylabel="Current density (mA cm$^{-2}$)")
fig.savefig("lsv.pdf")
print("  → lsv.pdf")

# ===========================================================================
# 4. EIS — Nyquist
# ===========================================================================
print("Plotting EIS Nyquist...")
freq, zr, zi = make_eis_data()
fig, ax = plot_eis_nyquist(zr, zi, label="Fresh cell")
fig.savefig("eis_nyquist.pdf")
print("  → eis_nyquist.pdf")

# ===========================================================================
# 5. EIS — Bode
# ===========================================================================
print("Plotting EIS Bode...")
freq, zr, zi = make_eis_data()
z_mag   = np.sqrt(zr ** 2 + zi ** 2)
z_phase = -np.degrees(np.arctan2(zi, zr))  # sign convention: capacitive is negative
fig, axes = plot_eis_bode(freq, z_mag, z_phase, label="Fresh cell")
fig.savefig("eis_bode.pdf")
print("  → eis_bode.pdf")

# ===========================================================================
# 6. Charge–Discharge
# ===========================================================================
print("Plotting Charge–Discharge...")
caps, volts = make_cd_data(n_cycles=3)
cycle_labels = []
for k in range(3):
    cycle_labels.extend([k + 1, None])   # label charge half-cycle only

fig, ax = plot_charge_discharge(caps, volts, cycle_numbers=cycle_labels)
fig.savefig("charge_discharge.pdf")
print("  → charge_discharge.pdf")

# ===========================================================================
# 7. Coulombic Efficiency
# ===========================================================================
print("Plotting Coulombic Efficiency...")
cycles = np.arange(1, 101)
q_chg  = 160 * np.exp(-0.002 * cycles)
q_dis  = q_chg * (0.7 + 0.295 * (1 - np.exp(-0.1 * cycles)))  # ramps to ~99.5 %
q_dis  = np.clip(q_dis, 0, q_chg)

fig, axes = plot_coulombic_eff(cycles, q_chg, q_dis)
fig.savefig("coulombic_efficiency.pdf")
print("  → coulombic_efficiency.pdf")

# ===========================================================================
# 8. Rate Capability
# ===========================================================================
print("Plotting Rate Capability...")
c_rates_str = ["0.1C", "0.2C", "0.5C", "1C", "2C", "0.1C"]
base_caps   = [155, 148, 138, 120, 95, 153]
segs_cyc, segs_cap = [], []
start = 1
for bc in base_caps:
    n = 5
    cyc = np.arange(start, start + n)
    cap = bc + np.random.normal(0, 1.5, n)
    segs_cyc.append(cyc)
    segs_cap.append(cap)
    start += n

fig, ax = plot_rate_capability(segs_cyc, segs_cap, c_rates=c_rates_str)
fig.savefig("rate_capability.pdf")
print("  → rate_capability.pdf")

# ===========================================================================
# 9. dQ/dV
# ===========================================================================
print("Plotting dQ/dV...")
v_dqdv = np.linspace(2.5, 4.2, 500)
# Simulate peaks at 3.4 V (charge) and 3.3 V (discharge)
dqdv_chg = (300 * np.exp(-((v_dqdv - 3.4) ** 2) / (2 * 0.05 ** 2))
           + 80  * np.exp(-((v_dqdv - 3.8) ** 2) / (2 * 0.04 ** 2)))
dqdv_dis = -(300 * np.exp(-((v_dqdv - 3.3) ** 2) / (2 * 0.05 ** 2))
            + 80  * np.exp(-((v_dqdv - 3.75) ** 2) / (2 * 0.04 ** 2)))
dqdv_total = dqdv_chg + dqdv_dis

fig, ax = plot_dqdv(
    [v_dqdv, v_dqdv],
    [dqdv_chg, dqdv_dis],
    label=["Charge", "Discharge"],
)
fig.savefig("dqdv.pdf")
print("  → dqdv.pdf")

print("\nAll plots saved successfully.")
