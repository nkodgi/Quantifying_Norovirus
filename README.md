# 🍽️ Norovirus Restaurant Outbreak Modeling

> Simulating real outbreaks, validating with data, and testing what actually works.

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

### Prerequisites

- Python 3.8+

```bash
pip install -r requirements.txt
```

### Installation

```bash
git clone <your-repo-url>
cd src
pip install -r requirements.txt
```

### Running the Model

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
├── DOC/
│   ├── poster.pdf
│   └── Final_Report.pdf
├── src/
│   ├── main.py                     # Full pipeline: calibration → policy analysis
│   │
│   ├── simulation.py               # Baseline outbreak simulator (no policy)
│   ├── calibration.py              # Grid search calibration utilities
│   ├── validation.py               # K-fold + holdout + full calibration workflow
│   │
│   ├── plotting.py                 # Calibration publication plots
│   ├── metrics.py                  # Extra validation metrics (KS, Wasserstein, etc.)
│   │
│   ├── policy_simulation.py        # Policy-enabled outbreak simulator
│   ├── policy_analysis.py          # 16-scenario policy analysis + Figures 1–5
│   │
│   └── NORS_JS1.csv                # Real CDC NORS outbreak data (input)
│
└── results/                        # (Optional) Generated outputs
    ├── Comprehensive_Policy_Summary.csv
    ├── Figure1_Policy_Overview.png/pdf
    ├── Figure2_Hygiene_Comparison.png/pdf
    ├── Figure3_Policy_Interactions.png/pdf
    ├── Figure4_Cost_Effectiveness.png/pdf
    └── Figure5_Distribution_Comparisons.png/pdf

```

---

## 🦠➡️📉 Results

Our analysis shows that [add your key findings here!] combined interventions are most effective at reducing outbreak size, with compliance level being a critical factor.

