# 🍽️ Norovirus Restaurant Outbreak Modeling

## Overview

This project explores how norovirus spreads inside a restaurant using a stochastic simulation model built to feel as close to real life as possible. We use real outbreak sizes from the CDC's NORS database and validate our model through K-fold cross-validation and full-dataset calibration. This helps us make sure our simulated outbreaks truly reflect ground-truth behavior before testing any interventions.

## What We Test

Once the model is calibrated, we evaluate three major public-health strategies:

- ✨ **Excluding symptomatic food handlers**
- ✨ **Improving hygiene to lower transmission**
- ✨ **Combining exclusion + hygiene**

Each policy is tested across different compliance levels to see how much it can reduce outbreak size. The result is a clear picture of which interventions make the biggest impact in controlling norovirus in restaurant settings.

---

## 📊 Key Features

- **Stochastic SEIR-inspired model** tailored to restaurant dynamics
- **Real data validation** against CDC NORS database
- **Cross-validation framework** for robust parameter estimation
- **Policy evaluation** across multiple compliance scenarios
- **Intervention impact analysis** with clear quantitative results

## 🚀 Getting Started

### Installation 
```bash
git clone https://github.com/nkodgi/Quantifying_Norovirus.git
cd Quantifying_Norovirus
pip install -r requirements.txt
```

### Running the Code
```bash
cd src
python3 main.py
```
---

## 📁 Project Structure

```
.
├── README.md
├── requirements.txt
│
├── src/                           # All modeling + simulation code
│   ├── main.py                    # Full pipeline: calibration → policy analysis
│   ├── simulation.py              # Baseline outbreak simulator (no policy)
│   ├── calibration.py             # Grid search calibration utilities
│   ├── validation.py              # K-fold + holdout + full calibration workflow
│   ├── plotting.py                # Calibration plots
│   ├── metrics.py                 # Validation metrics (KS, Wasserstein, etc.)
│   ├── policy_simulation.py       # Policy-enabled outbreak simulator
│   ├── policy_analysis.py         # 16-scenario analysis + Figures 1–5
│   └── NORS_JS1.csv               # Cleaned calibration dataset (outbreak sizes only)
│
├── results/                       # Auto-generated outputs (optional)
│   ├── Comprehensive_Policy_Summary.csv
│   ├── Figure1_Policy_Overview.png
│   ├── Figure2_Hygiene_Comparison.png
│   ├── Figure3_Policy_Interactions.png
│   ├── Figure4_Cost_Effectiveness.png
│   └── Figure5_Distribution_Comparisons.png
│
├── docs/                          # Website + documentation
│   ├── index.html                 # Website homepage
│   ├── images/                    # Site assets (figures, team photos, icons)
│   │     └── (... image files ...)
│   ├── Epi_Poster.pdf             # Final project poster
│   ├── Final_Report.pdf           # Full final written report
│   ├── NORS_20251007.csv          # Original downloaded NORS data
│   └── NORS_calibration_policy_final.ipynb   # Full calibration + policy notebook


```

