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
- Required packages: `numpy`, `pandas`, `scipy`, `matplotlib` (or your actual dependencies)

### Installation

```bash
git clone <your-repo-url>
cd norovirus-outbreak-modeling
pip install -r requirements.txt
```

### Running the Model

```bash
python simulate_outbreak.py
python validate_model.py
python evaluate_interventions.py
```

---

## 📁 Project Structure

```
.
├── README.md
├── requirements.txt
├── simulate_outbreak.py          # Core stochastic simulation
├── validate_model.py             # K-fold CV and calibration
├── evaluate_interventions.py     # Policy testing
├── data/
│   └── cdc_nors_data.csv        # Real outbreak data
└── results/
    └── outbreak_comparisons.csv  # Intervention results
```

---

## 🦠➡️📉 Results

Our analysis shows that [add your key findings here!] combined interventions are most effective at reducing outbreak size, with compliance level being a critical factor.

