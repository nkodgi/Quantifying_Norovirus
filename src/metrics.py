
import numpy as np
from scipy.stats import ks_2samp, wasserstein_distance

def extra_validation_metrics(obs, sim):

    print("\n" + "="*70)
    print(" EXTRA VALIDATION METRICS")
    print("="*70)

    ks_stat, ks_p = ks_2samp(obs, sim)
    wd = wasserstein_distance(obs, sim)

    pct_list = [10,25,50,75,90,95,99]
    obs_p = np.percentile(obs, pct_list)
    sim_p = np.percentile(sim, pct_list)
    pct_err = np.abs(obs_p - sim_p)

    var_ratio = np.var(sim) / np.var(obs)

    boot = []
    for _ in range(200):
        boot.append(np.mean(np.random.choice(sim, size=len(sim), replace=True)))
    boot_std = np.std(boot)

    print("KS statistic:", ks_stat)
    print("KS p-value:", ks_p)
    print("Wasserstein:", wd)
    print("Overdispersion:", var_ratio)
    print("95th pct error:", pct_err[-2])
    print("99th pct error:", pct_err[-1])
    print("Bootstrap SD:", boot_std)

    return {
        "ks_stat": ks_stat,
        "ks_p": ks_p,
        "wd": wd,
        "var_ratio": var_ratio,
        "tail95": pct_err[-2],
        "tail99": pct_err[-1],
        "boot_sd": boot_std
    }
