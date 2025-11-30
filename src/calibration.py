
import numpy as np
from tqdm import tqdm
from simulation import simulate_restaurant_outbreak_v3

def calculate_score(real_sizes, sim_sizes):
    r = np.percentile(real_sizes, [10,25,50,75,90,95,99])
    s = np.percentile(sim_sizes,  [10,25,50,75,90,95,99])
    w = np.array([1,1.5,2.5,1.5,2,2.5,3.5])
    return np.average(np.abs(r - s), weights=w)

def calibrate_fast_for_kfold(train_sizes):

    betas_handler = np.linspace(0.015,0.035,5)
    probs = np.linspace(0.10,0.22,4)
    means = np.linspace(35,65,3)
    betas_staff = [0.01, 0.05, 0.1, 0.2]

    best_sc = np.inf
    best_par = None

    for bh in betas_handler:
        for p in probs:
            for m in means:
                for bs in betas_staff:

                    sims = np.array([
                        simulate_restaurant_outbreak_v3(
                            beta_handler_patron=bh,
                            prob_food_contamination=p,
                            contamination_size_mean=m,
                            contamination_size_std=30,
                            beta_staff_staff=bs
                        )
                        for _ in range(200)
                    ])

                    sc = calculate_score(train_sizes, sims)

                    if sc < best_sc:
                        best_sc = sc
                        best_par = {
                            'beta_handler_patron': bh,
                            'prob_food_contamination': p,
                            'contamination_size_mean': m,
                            'beta_staff_staff': bs
                        }

    return best_par, best_sc

def calibrate_model(train_sizes, n_sims=500, desc="Calibrating full grid"):

    betas_handler = np.linspace(0.015,0.035,8)
    probs = np.linspace(0.10,0.22,6)
    means = np.linspace(35,65,5)
    betas_staff = [0.01, 0.03, 0.05, 0.1, 0.2]

    best_score = np.inf
    best_params = None
    best_sim = None

    total_it = len(betas_handler)*len(probs)*len(means)*len(betas_staff)
    pbar = tqdm(total=total_it, desc=desc)

    for bh in betas_handler:
        for p in probs:
            for m in means:
                for bs in betas_staff:

                    sims = np.array([
                        simulate_restaurant_outbreak_v3(
                            beta_handler_patron=bh,
                            prob_food_contamination=p,
                            contamination_size_mean=m,
                            contamination_size_std=30,
                            beta_staff_staff=bs
                        )
                        for _ in range(n_sims)
                    ])

                    sc = calculate_score(train_sizes, sims)

                    if sc < best_score:
                        best_score = sc
                        best_params = {
                            'beta_handler_patron': bh,
                            'beta_staff_staff': bs,
                            'prob_food_contamination': p,
                            'contamination_size_mean': m,
                            'contamination_size_std': 30
                        }
                        best_sim = sims

                    pbar.update(1)

    pbar.close()
    return best_params, best_sim, best_score
