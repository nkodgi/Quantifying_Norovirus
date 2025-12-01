
import numpy as np
import pandas as pd
from tqdm import tqdm

from simulation import simulate_restaurant_outbreak_v3
from calibration import (
    calculate_score,
    calibrate_fast_for_kfold,
    calibrate_model
)

def step1_kfold_validation(all_sizes, k=5):

    print("="*70)
    print(" STEP 1: K-FOLD (FAST GRID) ")
    print("="*70)

    # Compute bins
    bins = np.percentile(all_sizes, [0,20,40,60,80,100])
    labels = np.digitize(all_sizes, bins[1:-1])

    # Group indices
    bin_groups = {b: [] for b in np.unique(labels)}
    for idx, lab in enumerate(labels):
        bin_groups[lab].append(idx)

    # Shuffle inside bins
    for b in bin_groups:
        np.random.shuffle(bin_groups[b])

    # Build folds
    folds = [[] for _ in range(k)]
    for b in bin_groups:
        group = bin_groups[b]
        size = len(group)
        seg = size // k

        for i in range(k):
            start = i * seg
            end = (i+1)*seg if i < k-1 else size
            folds[i].extend(group[start:end])

    results = []

    # Evaluate folds
    for fold in range(k):

        test_idx = np.array(folds[fold])
        train_idx = np.array([x for i,f in enumerate(folds) if i != fold for x in f])

        train_vals = all_sizes[train_idx]
        test_vals  = all_sizes[test_idx]

        print("\nFold", fold+1)

        # Fast calibration
        par, train_sc = calibrate_fast_for_kfold(train_vals)

        out = np.array([
            simulate_restaurant_outbreak_v3(**par)
            for _ in range(200)
        ])

        test_sc = calculate_score(test_vals, out)
        ratio = test_sc/train_sc

        print(" train_score:", train_sc)
        print(" test_score:", test_sc)
        print(" ratio:", ratio)

        results.append({
            'fold': fold+1,
            'train_score': train_sc,
            'test_score': test_sc,
            'ratio': ratio,
            'params': par
        })

    return results, np.mean([r['ratio'] for r in results]), np.std([r['ratio'] for r in results])

def step2_holdout_validation(all_sizes):

    print("\n" + "="*70)
    print(" STEP 2: HOLDOUT (FULL GRID) ")
    print("="*70)
    
    n_train = int(len(all_sizes)*0.8)

    shuf = np.random.permutation(len(all_sizes))
    train_vals = all_sizes[shuf[:n_train]]
    test_vals  = all_sizes[shuf[n_train:]]

    par, sim_train, train_sc = calibrate_model(train_vals, n_sims=300,
                                               desc="Holdout calibration")

    out = np.array([
        simulate_restaurant_outbreak_v3(**par)
        for _ in tqdm(range(300))
    ])

    test_sc = calculate_score(test_vals, out)
    ratio = test_sc/train_sc

    return par, sim_train, train_vals, out, test_vals, ratio

def step3_full_calibration(all_sizes):

    print("\n" + "="*70)
    print(" STEP 3: FULL CALIBRATION ")
    print("="*70)

    par, sim_sizes, sc = calibrate_model(all_sizes, n_sims=500,
                                         desc="Full calibration")

    print("\nFinal parameters:")
    for kk,vv in par.items():
        print(" ", kk, ":", vv)
    print("Calibration score:", sc)

    return par, sim_sizes
