
import numpy as np
import matplotlib.pyplot as plt

def create_publication_plots(obs, sim, kfold_results, holdout_ratio):

    fig, axes = plt.subplots(2,2, figsize=(12,10))
    ax1, ax2, ax3, ax4 = axes.flatten()

    # A. Distribution comparison
    ax1.hist(obs, bins=40, density=True, alpha=0.6, label="Observed (NORS)")
    ax1.hist(sim, bins=40, density=True, alpha=0.6, label="Simulated (Model)")
    ax1.set_title("A. Distribution Comparison")
    ax1.set_xlabel("Outbreak Size (cases)")
    ax1.set_ylabel("Probability Density")
    ax1.legend()

    # B. CDF
    sorted_obs = np.sort(obs)
    sorted_sim = np.sort(sim)
    ax2.plot(sorted_obs, np.linspace(0,1,len(sorted_obs)), label="Observed")
    ax2.plot(sorted_sim, np.linspace(0,1,len(sorted_sim)), linestyle="--", label="Simulated")
    ax2.set_title("B. CDF")
    ax2.legend()

    # C. QQ plot
    q_obs = np.percentile(obs, np.linspace(0,100,120))
    q_sim = np.percentile(sim, np.linspace(0,100,120))
    ax3.scatter(q_obs, q_sim, alpha=0.6, color="purple")
    ax3.plot([0,max(q_obs)], [0,max(q_obs)], 'r--')
    ax3.set_title("C. QQ Plot")

    # D. Percentile comparison
    pct_list = [25,50,75,90,95,99]
    obs_p = np.percentile(obs, pct_list)
    sim_p = np.percentile(sim, pct_list)
    x = np.arange(len(pct_list))
    width = 0.35

    ax4.bar(x-width/2, obs_p, width, label="Observed")
    ax4.bar(x+width/2, sim_p, width, label="Simulated")
    ax4.set_xticks(x)
    ax4.set_xticklabels([f"{p}th" for p in pct_list])
    ax4.set_title("D. Percentile Comparison")
    ax4.legend()

    plt.tight_layout()
    plt.show()

    # K-fold ratios + holdout
    ratios = [r["ratio"] for r in kfold_results]
    folds  = [r["fold"] for r in kfold_results]

    fig, (axA, axB) = plt.subplots(1,2, figsize=(12,5))
    axA.bar(folds, ratios)
    axA.axhline(1.5, linestyle="--", color="red")
    axA.set_title("K-Fold Ratios")

    axB.bar(["K-Fold Avg","Holdout"], [np.mean(ratios), holdout_ratio])
    axB.axhline(1.5, linestyle="--", color="red")
    axB.set_title("Validation Summary")

    plt.tight_layout()
    fig.savefig("Calibration_Figure2_Validation.png", dpi=300, bbox_inches="tight")
    ig.savefig("Calibration_Figure2_Validation.pdf", bbox_inches="tight")
    plt.show()
