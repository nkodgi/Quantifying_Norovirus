
"""
main execution pipeline

This script runs:
1. Calibration (k-fold, holdout, full)
2. Publication plots for calibration
3. Full policy analysis (16 scenarios + 5 figures)

Make sure the following files exist in SRC/:
- calibration.py
- simulation.py
- plotting.py   (your create_publication_plots + extra_validation_metrics)
- policy_simulation.py
- policy_analysis.py
"""

import pandas as pd
import numpy as np
import random


# Import modules
from validation import (
    step1_kfold_validation,
    step2_holdout_validation,
    step3_full_calibration
)

# Import baseline publication plots
from plotting import create_publication_plots
from metrics import extra_validation_metrics

# Import policy analysis
from policy_analysis import run_complete_analysis


# main

def main():

    np.random.seed(20)
    random.seed(20)
    
    print("\n" + "="*70)
    print(" FULL EPIDEMIC PIPELINE: CALIBRATION → POLICY ANALYSIS ")
    print("="*70)

    # load outbreak data
    print("\n[1] Loading NORS data...")
    df = pd.read_csv("NORS_JS1.csv", header=None)
    sizes = df[0].dropna().astype(int).values
    print(f"Loaded {len(sizes)} outbreak sizes.")

    # STEP 1 — K-FOLD VALIDATION
    print("\n[2] Running Step 1: K-Fold Validation...")
    kfold_results, kmean, kstd = step1_kfold_validation(sizes)

    # STEP 2 — HOLDOUT VALIDATION
    print("\n[3] Running Step 2: Holdout Validation...")
    hold_params, sim_train, train_vals, sim_test, test_vals, hold_ratio = \
        step2_holdout_validation(sizes)

    # STEP 3 — FULL CALIBRATION
    print("\n[4] Running Step 3: Full Calibration...")
    final_params, sim_full = step3_full_calibration(sizes)

    print("\nCalibrated parameters (from Step 3):")
    for key, val in final_params.items():
        print(f"  {key}: {val}")


    # PLOTTING CALIBRATION RESULTS
    print("\n[5] Creating baseline publication plots...")
    create_publication_plots(sizes, sim_full, kfold_results, hold_ratio)
    extra_validation_metrics(sizes, sim_full)
    print("✓ Calibration figures saved.")

 
    # RUN POLICY ANALYSIS
    print("\n[6] Running comprehensive policy analysis...")
    scenarios, summary_df = run_complete_analysis(final_params, n_sims=1500)

    print("\nDONE. All calibration + policy results generated.")

    print("\n" + "="*70)
    print(" FULL PIPELINE COMPLETE ")
    print("="*70)



# ENTRY POINT
if __name__ == "__main__":
    main()
