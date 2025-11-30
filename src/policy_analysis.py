
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from matplotlib.gridspec import GridSpec

from policy_simulation import simulate_outbreak_policy


# SCENARIO RUNNER


def run_comprehensive_policy_analysis(calibrated_params, N_runs=1500):

    print("=" * 70)
    print("COMPREHENSIVE POLICY ANALYSIS - 16 SCENARIOS")
    print("=" * 70)
    print(f"\nSimulations per scenario: {N_runs}")
    print(f"\nCalibrated parameters:")
    for k, v in calibrated_params.items():
        print(f"  {k}: {v}")
    print()

    scenarios = {}
    compliances = [0.3, 0.6, 1.0]
    hygiene_levels = {
        'Moderate': 0.7,
        'Strict': 0.4
    }

    # SCENARIO A: Baseline
    print("Running A: Baseline (no intervention)...")
    scenarios["A_Baseline"] = np.array([
        simulate_outbreak_policy(**calibrated_params)
        for _ in tqdm(range(N_runs), desc="Baseline", leave=False)
    ])

    # SCENARIO B: Exclusion only
    for c in compliances:
        c_pct = int(c * 100)
        print(f"Running B: Exclusion {c_pct}% compliance...")
        scenarios[f"B_Exclusion_{c_pct}%"] = np.array([
            simulate_outbreak_policy(
                **calibrated_params,
                policy_exclusion=True,
                compliance=c
            ) for _ in tqdm(range(N_runs), desc=f"Exclusion {c_pct}%", leave=False)
        ])

    # SCENARIO C: Hygiene only (Moderate + Strict)
    for hygiene_name, beta_mult in hygiene_levels.items():
        for c in compliances:
            c_pct = int(c * 100)
            print(f"Running C: {hygiene_name} Hygiene {c_pct}% compliance...")
            scenarios[f"C_{hygiene_name}_{c_pct}%"] = np.array([
                simulate_outbreak_policy(
                    **calibrated_params,
                    policy_hygiene=True,
                    compliance=c,
                    beta_mult=beta_mult
                ) for _ in tqdm(range(N_runs), desc=f"{hygiene_name} {c_pct}%", leave=False)
            ])

    # SCENARIO D: Combined (Moderate + Strict)
    for hygiene_name, beta_mult in hygiene_levels.items():
        for c in compliances:
            c_pct = int(c * 100)
            print(f"Running D: {hygiene_name} + Exclusion {c_pct}% compliance...")
            scenarios[f"D_{hygiene_name}_Combined_{c_pct}%"] = np.array([
                simulate_outbreak_policy(
                    **calibrated_params,
                    policy_exclusion=True,
                    policy_hygiene=True,
                    compliance=c,
                    beta_mult=beta_mult
                ) for _ in tqdm(range(N_runs), desc=f"{hygiene_name}+Excl {c_pct}%", leave=False)
            ])

    print("\n✓ All scenarios completed!")
    return scenarios


# SUMMARY TABLE

def create_summary_table(scenarios):

    baseline = scenarios["A_Baseline"]
    baseline_mean = np.mean(baseline)
    baseline_median = np.median(baseline)

    rows = []
    for name, data in scenarios.items():
        mean_val = np.mean(data)
        median_val = np.median(data)
        std_val = np.std(data)
        p25 = np.percentile(data, 25)
        p75 = np.percentile(data, 75)
        p95 = np.percentile(data, 95)

        mean_reduction = (baseline_mean - mean_val) / baseline_mean * 100
        median_reduction = (baseline_median - median_val) / baseline_median * 100
        cases_averted = baseline_mean - mean_val

        rows.append({
            'Scenario': name,
            'Mean': f"{mean_val:.1f}",
            'Median': f"{median_val:.1f}",
            'Std': f"{std_val:.1f}",
            '25th': f"{p25:.1f}",
            '75th': f"{p75:.1f}",
            '95th': f"{p95:.1f}",
            'Mean_Reduction_%': f"{mean_reduction:.1f}",
            'Median_Reduction_%': f"{median_reduction:.1f}",
            'Cases_Averted': f"{cases_averted:.1f}"
        })

    return pd.DataFrame(rows)

# FIGURE 1

def create_figure1_overview(scenarios, summary_df):
    """
    FIGURE 1: Policy Overview
    4-panel figure showing distributions and main effects
    """

    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    # Colors
    color_baseline = '#E74C3C'
    color_exclusion = '#3498DB'
    color_moderate = '#27AE60'
    color_strict = '#9B59B6'
    color_combined_mod = '#F39C12'
    color_combined_strict = '#E67E22'

    # Panel A: Baseline vs Best of Each Policy Type
    ax1 = fig.add_subplot(gs[0, 0])

    data_to_plot = [
        scenarios['A_Baseline'],
        scenarios['B_Exclusion_100%'],
        scenarios['C_Moderate_100%'],
        scenarios['C_Strict_100%'],
        scenarios['D_Moderate_Combined_100%'],
        scenarios['D_Strict_Combined_100%']
    ]
    labels = ['Baseline', 'Exclusion\n(100%)', 'Moderate\nHygiene',
              'Strict\nHygiene', 'Moderate\nCombined', 'Strict\nCombined']
    colors = [color_baseline, color_exclusion, color_moderate,
              color_strict, color_combined_mod, color_combined_strict]

    bp = ax1.boxplot(data_to_plot, labels=labels, patch_artist=True,
                     showfliers=False, widths=0.6)

    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
        patch.set_linewidth(1.5)

    for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bp[element], linewidth=1.5)

    ax1.set_ylabel('Outbreak Size (cases)', fontweight='bold', fontsize=13)
    ax1.set_title('A. Policy Effectiveness at 100% Compliance',
                  fontweight='bold', fontsize=14, pad=15)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_xticklabels(labels, rotation=0, fontsize=10)

    # Panel B: Compliance Dose-Response
    ax2 = fig.add_subplot(gs[0, 1])

    compliances = [0, 30, 60, 100]

    # Exclusion
    excl_means = [
        np.mean(scenarios['A_Baseline']),
        np.mean(scenarios['B_Exclusion_30%']),
        np.mean(scenarios['B_Exclusion_60%']),
        np.mean(scenarios['B_Exclusion_100%'])
    ]

    # Moderate hygiene
    mod_means = [
        np.mean(scenarios['A_Baseline']),
        np.mean(scenarios['C_Moderate_30%']),
        np.mean(scenarios['C_Moderate_60%']),
        np.mean(scenarios['C_Moderate_100%'])
    ]

    # Strict hygiene
    strict_means = [
        np.mean(scenarios['A_Baseline']),
        np.mean(scenarios['C_Strict_30%']),
        np.mean(scenarios['C_Strict_60%']),
        np.mean(scenarios['C_Strict_100%'])
    ]

    # Combined moderate
    comb_mod_means = [
        np.mean(scenarios['A_Baseline']),
        np.mean(scenarios['D_Moderate_Combined_30%']),
        np.mean(scenarios['D_Moderate_Combined_60%']),
        np.mean(scenarios['D_Moderate_Combined_100%'])
    ]

    # Combined strict
    comb_strict_means = [
        np.mean(scenarios['A_Baseline']),
        np.mean(scenarios['D_Strict_Combined_30%']),
        np.mean(scenarios['D_Strict_Combined_60%']),
        np.mean(scenarios['D_Strict_Combined_100%'])
    ]

    ax2.plot(compliances, excl_means, marker='o', linewidth=3, markersize=10,
             label='Exclusion Only', color=color_exclusion)
    ax2.plot(compliances, mod_means, marker='s', linewidth=3, markersize=10,
             label='Moderate Hygiene', color=color_moderate)
    ax2.plot(compliances, strict_means, marker='^', linewidth=3, markersize=10,
             label='Strict Hygiene', color=color_strict)
    ax2.plot(compliances, comb_mod_means, marker='D', linewidth=3, markersize=9,
             label='Moderate Combined', color=color_combined_mod, linestyle='--')
    ax2.plot(compliances, comb_strict_means, marker='v', linewidth=3, markersize=10,
             label='Strict Combined', color=color_combined_strict, linestyle='--')

    ax2.set_xlabel('Compliance Level (%)', fontweight='bold', fontsize=13)
    ax2.set_ylabel('Mean Outbreak Size (cases)', fontweight='bold', fontsize=13)
    ax2.set_title('B. Compliance Dose-Response Curves',
                  fontweight='bold', fontsize=14, pad=15)
    ax2.legend(frameon=True, shadow=True, fontsize=10, loc='upper right')
    ax2.grid(alpha=0.3, linestyle='--')
    ax2.set_xlim(-5, 105)

    # Panel C: Percent Reduction Heatmap
    ax3 = fig.add_subplot(gs[1, 0])

    baseline_mean = np.mean(scenarios['A_Baseline'])

    # Create reduction matrix
    policies = ['Exclusion', 'Moderate\nHygiene', 'Strict\nHygiene',
                'Moderate\nCombined', 'Strict\nCombined']
    comp_levels = ['30%', '60%', '100%']

    reduction_matrix = []

    for policy_type in ['B_Exclusion', 'C_Moderate', 'C_Strict',
                        'D_Moderate_Combined', 'D_Strict_Combined']:
        row = []
        for comp in comp_levels:
            key = f"{policy_type}_{comp}"
            mean_val = np.mean(scenarios[key])
            reduction = (baseline_mean - mean_val) / baseline_mean * 100
            row.append(reduction)
        reduction_matrix.append(row)

    reduction_matrix = np.array(reduction_matrix)

    im = ax3.imshow(reduction_matrix, cmap='RdYlGn', aspect='auto',
                    vmin=0, vmax=80)

    ax3.set_xticks(np.arange(len(comp_levels)))
    ax3.set_yticks(np.arange(len(policies)))
    ax3.set_xticklabels(comp_levels, fontsize=11)
    ax3.set_yticklabels(policies, fontsize=11)

    ax3.set_xlabel('Compliance Level', fontweight='bold', fontsize=13)
    ax3.set_ylabel('Policy Type', fontweight='bold', fontsize=13)
    ax3.set_title('C. Outbreak Reduction Heatmap (%)',
                  fontweight='bold', fontsize=14, pad=15)

    # Add text annotations
    for i in range(len(policies)):
        for j in range(len(comp_levels)):
            text = ax3.text(j, i, f'{reduction_matrix[i, j]:.0f}%',
                            ha="center", va="center", color="black",
                            fontsize=12, fontweight='bold')

    cbar = plt.colorbar(im, ax=ax3)
    cbar.set_label('Reduction (%)', fontweight='bold', fontsize=11)

    # Panel D: Cases Averted
    ax4 = fig.add_subplot(gs[1, 1])

    cases_averted_data = []
    policy_labels = []
    policy_colors = []

    for comp in comp_levels:
        # Exclusion
        cases = baseline_mean - np.mean(scenarios[f'B_Exclusion_{comp}'])
        cases_averted_data.append(cases)
        policy_labels.append(f'Excl\n{comp}')
        policy_colors.append(color_exclusion)

        # Moderate
        cases = baseline_mean - np.mean(scenarios[f'C_Moderate_{comp}'])
        cases_averted_data.append(cases)
        policy_labels.append(f'Mod\n{comp}')
        policy_colors.append(color_moderate)

        # Strict
        cases = baseline_mean - np.mean(scenarios[f'C_Strict_{comp}'])
        cases_averted_data.append(cases)
        policy_labels.append(f'Strict\n{comp}')
        policy_colors.append(color_strict)

        # Mod Combined
        cases = baseline_mean - np.mean(scenarios[f'D_Moderate_Combined_{comp}'])
        cases_averted_data.append(cases)
        policy_labels.append(f'M+E\n{comp}')
        policy_colors.append(color_combined_mod)

        # Strict Combined
        cases = baseline_mean - np.mean(scenarios[f'D_Strict_Combined_{comp}'])
        cases_averted_data.append(cases)
        policy_labels.append(f'S+E\n{comp}')
        policy_colors.append(color_combined_strict)

    x_pos = np.arange(len(cases_averted_data))
    bars = ax4.bar(x_pos, cases_averted_data, color=policy_colors, alpha=0.8,
                   edgecolor='black', linewidth=1.2)

    ax4.set_xlabel('Policy and Compliance', fontweight='bold', fontsize=13)
    ax4.set_ylabel('Cases Averted per Outbreak', fontweight='bold', fontsize=13)
    ax4.set_title('D. Public Health Impact', fontweight='bold', fontsize=14, pad=15)
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(policy_labels, fontsize=9)
    ax4.grid(axis='y', alpha=0.3, linestyle='--')
    ax4.axhline(y=0, color='black', linestyle='-', linewidth=0.8)

    plt.savefig('Figure1_Policy_Overview.png', dpi=300, bbox_inches='tight')
    plt.savefig('Figure1_Policy_Overview.pdf', bbox_inches='tight')
    plt.show()

    print("✓ Saved: Figure1_Policy_Overview.png/pdf")


# FIGURE 2

def create_figure2_hygiene_comparison(scenarios):
    """
    FIGURE 2: Moderate vs Strict Hygiene Comparison
    Shows whether intensity or compliance matters more
    """

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    baseline_mean = np.mean(scenarios['A_Baseline'])
    compliances = [30, 60, 100]

    # Panel A: Outbreak size by hygiene intensity
    ax1 = axes[0]

    x = np.arange(len(compliances))
    width = 0.35

    moderate_means = [np.mean(scenarios[f'C_Moderate_{c}%']) for c in compliances]
    strict_means = [np.mean(scenarios[f'C_Strict_{c}%']) for c in compliances]

    moderate_std = [np.std(scenarios[f'C_Moderate_{c}%']) for c in compliances]
    strict_std = [np.std(scenarios[f'C_Strict_{c}%']) for c in compliances]

    bars1 = ax1.bar(
        x - width/2, moderate_means, width,
        label='Moderate (30% reduction)',
        color='#27AE60', alpha=0.8, edgecolor='black', linewidth=1.5,
        yerr=moderate_std, capsize=5, error_kw={'linewidth': 2}
    )

    bars2 = ax1.bar(
        x + width/2, strict_means, width,
        label='Strict (60% reduction)',
        color='#9B59B6', alpha=0.8, edgecolor='black', linewidth=1.5,
        yerr=strict_std, capsize=5, error_kw={'linewidth': 2}
    )

    ax1.axhline(
        y=baseline_mean, color='#E74C3C', linestyle='--', linewidth=2.5,
        label='Baseline', alpha=0.7
    )

    ax1.set_ylabel('Mean Outbreak Size (cases)', fontweight='bold', fontsize=13)
    ax1.set_xlabel('Compliance Level (%)', fontweight='bold', fontsize=13)
    ax1.set_title('A. Hygiene Intensity Comparison',
                  fontweight='bold', fontsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels(compliances)
    ax1.legend(frameon=True, shadow=True, fontsize=11)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')

    # Panel B: Percent reduction
    ax2 = axes[1]

    moderate_reduction = [
        (baseline_mean - m) / baseline_mean * 100 for m in moderate_means
    ]
    strict_reduction = [
        (baseline_mean - s) / baseline_mean * 100 for s in strict_means
    ]

    ax2.plot(
        compliances, moderate_reduction, marker='o', linewidth=3.5, markersize=12,
        label='Moderate Hygiene', color='#27AE60'
    )
    ax2.plot(
        compliances, strict_reduction, marker='s', linewidth=3.5, markersize=12,
        label='Strict Hygiene', color='#9B59B6'
    )

    ax2.set_ylabel('Outbreak Reduction (%)', fontweight='bold', fontsize=13)
    ax2.set_xlabel('Compliance Level (%)', fontweight='bold', fontsize=13)
    ax2.set_title('B. Reduction vs Compliance', fontweight='bold', fontsize=14)
    ax2.legend(frameon=True, shadow=True, fontsize=11)
    ax2.grid(alpha=0.3, linestyle='--')
    ax2.set_xlim(20, 110)

    # Panel C: Incremental benefit of strict over moderate
    ax3 = axes[2]

    incremental_benefit = [
        s - m for m, s in zip(moderate_reduction, strict_reduction)
    ]

    bars = ax3.bar(
        compliances, incremental_benefit,
        color='#9B59B6', alpha=0.7, edgecolor='black', linewidth=1.5, width=20
    )

    ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax3.set_ylabel(
        'Additional Reduction from\nStrict vs Moderate (%)',
        fontweight='bold', fontsize=13
    )
    ax3.set_xlabel('Compliance Level (%)', fontweight='bold', fontsize=13)
    ax3.set_title('C. Incremental Benefit of Strict Hygiene',
                  fontweight='bold', fontsize=14)
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    ax3.set_xlim(15, 115)

    # Add value labels on bars
    for bar, val in zip(bars, incremental_benefit):
        height = bar.get_height()
        ax3.text(
            bar.get_x() + bar.get_width()/2., height + 1,
            f'+{val:.1f}%', ha='center', va='bottom',
            fontweight='bold', fontsize=11
        )

    plt.tight_layout()
    plt.savefig('Figure2_Hygiene_Comparison.png', dpi=300, bbox_inches='tight')
    plt.savefig('Figure2_Hygiene_Comparison.pdf', bbox_inches='tight')
    plt.show()

    print("✓ Saved: Figure2_Hygiene_Comparison.png/pdf")


# FIGURE 3

def create_figure3_policy_interactions(scenarios):
    """
    FIGURE 3: Policy Interactions and Synergy
    Shows whether combined policies are additive, synergistic, or antagonistic
    """

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    baseline_mean = np.mean(scenarios['A_Baseline'])
    compliances = [30, 60, 100]

    # Panel A: Moderate hygiene interactions
    ax1 = axes[0]

    x = np.arange(len(compliances))
    width = 0.25

    excl_only = [np.mean(scenarios[f'B_Exclusion_{c}%']) for c in compliances]
    mod_only = [np.mean(scenarios[f'C_Moderate_{c}%']) for c in compliances]
    mod_combined = [np.mean(scenarios[f'D_Moderate_Combined_{c}%']) for c in compliances]

    # Expected additive effect
    expected_additive = []
    for e, m in zip(excl_only, mod_only):
        excl_red = (baseline_mean - e) / baseline_mean
        mod_red = (baseline_mean - m) / baseline_mean
        expected = baseline_mean * (1 - (excl_red + mod_red))
        expected_additive.append(expected)

    bars1 = ax1.bar(x - width, excl_only, width, label='Exclusion Only',
                    color='#3498DB', alpha=0.8, edgecolor='black', linewidth=1.2)
    bars2 = ax1.bar(x, mod_only, width, label='Moderate Hygiene Only',
                    color='#27AE60', alpha=0.8, edgecolor='black', linewidth=1.2)
    bars3 = ax1.bar(x + width, mod_combined, width, label='Combined (Observed)',
                    color='#F39C12', alpha=0.8, edgecolor='black', linewidth=1.2)

    ax1.plot(x, expected_additive, marker='x', markersize=15, linewidth=0,
             color='red', label='Expected (Additive)', markeredgewidth=3)

    ax1.set_ylabel('Mean Outbreak Size (cases)', fontweight='bold', fontsize=13)
    ax1.set_xlabel('Compliance Level (%)', fontweight='bold', fontsize=13)
    ax1.set_title('A. Moderate Hygiene + Exclusion Interactions',
                  fontweight='bold', fontsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels(compliances)
    ax1.legend(frameon=True, shadow=True, fontsize=11)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')

    # Panel B: Synergy quantification
    ax2 = axes[1]

    mod_synergy = []
    strict_synergy = []

    for c in compliances:
        # Moderate
        excl = np.mean(scenarios[f'B_Exclusion_{c}%'])
        mod = np.mean(scenarios[f'C_Moderate_{c}%'])
        mod_comb = np.mean(scenarios[f'D_Moderate_Combined_{c}%'])

        excl_effect = baseline_mean - excl
        mod_effect = baseline_mean - mod
        expected_additive = baseline_mean - (excl_effect + mod_effect)

        synergy = ((expected_additive - mod_comb) / baseline_mean) * 100
        mod_synergy.append(synergy)

        # Strict
        strict = np.mean(scenarios[f'C_Strict_{c}%'])
        strict_comb = np.mean(scenarios[f'D_Strict_Combined_{c}%'])

        strict_effect = baseline_mean - strict
        expected_additive_strict = baseline_mean - (excl_effect + strict_effect)

        synergy_strict = ((expected_additive_strict - strict_comb) / baseline_mean) * 100
        strict_synergy.append(synergy_strict)

    width = 0.35
    x_pos = np.arange(len(compliances))

    bars1 = ax2.bar(x_pos - width/2, mod_synergy, width, label='Moderate + Exclusion',
                    color='#F39C12', alpha=0.8, edgecolor='black', linewidth=1.2)
    bars2 = ax2.bar(x_pos + width/2, strict_synergy, width, label='Strict + Exclusion',
                    color='#E67E22', alpha=0.8, edgecolor='black', linewidth=1.2)

    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1.5)
    ax2.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5,
                label='Purely Additive')

    ax2.set_ylabel('Synergy (%)\n(Positive = Synergistic)',
                   fontweight='bold', fontsize=13)
    ax2.set_xlabel('Compliance Level (%)', fontweight='bold', fontsize=13)
    ax2.set_title('B. Policy Synergy Quantification', fontweight='bold', fontsize=14)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(compliances)
    ax2.legend(frameon=True, shadow=True, fontsize=11)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')

    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            label_y = height + 0.5 if height > 0 else height - 1.5
            ax2.text(bar.get_x() + bar.get_width()/2., label_y,
                     f'{height:.1f}%', ha='center',
                     va='bottom' if height > 0 else 'top',
                     fontweight='bold', fontsize=10)

    plt.tight_layout()
    plt.savefig('Figure3_Policy_Interactions.png', dpi=300, bbox_inches='tight')
    plt.savefig('Figure3_Policy_Interactions.pdf', bbox_inches='tight')
    plt.show()

    print("✓ Saved: Figure3_Policy_Interactions.png/pdf")


# FIGURE 4

def create_figure4_cost_effectiveness(scenarios):
    """
    FIGURE 4: Policy Efficiency Analysis
    Shows cost-effectiveness and optimal strategies
    """

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    baseline_mean = np.mean(scenarios['A_Baseline'])
    compliances = [30, 60, 100]

    # Panel A: Efficiency frontier (reduction per compliance %)
    ax1 = axes[0]

    policies = {
        'Exclusion': ('B_Exclusion', '#3498DB'),
        'Moderate Hygiene': ('C_Moderate', '#27AE60'),
        'Strict Hygiene': ('C_Strict', '#9B59B6'),
        'Moderate Combined': ('D_Moderate_Combined', '#F39C12'),
        'Strict Combined': ('D_Strict_Combined', '#E67E22')
    }

    for policy_name, (policy_key, color) in policies.items():
        reductions = []
        for c in compliances:
            mean_val = np.mean(scenarios[f'{policy_key}_{c}%'])
            reduction = (baseline_mean - mean_val) / baseline_mean * 100
            reductions.append(reduction)

        efficiency = [r / c for r, c in zip(reductions, compliances)]

        ax1.plot(compliances, efficiency, marker='o', linewidth=3, markersize=10,
                 label=policy_name, color=color)

    ax1.set_xlabel('Compliance Level (%)', fontweight='bold', fontsize=13)
    ax1.set_ylabel('Efficiency\n(% Reduction per % Compliance)',
                   fontweight='bold', fontsize=13)
    ax1.set_title('A. Policy Efficiency Curves', fontweight='bold', fontsize=14)
    ax1.legend(frameon=True, shadow=True, fontsize=11)
    ax1.grid(alpha=0.3, linestyle='--')
    ax1.set_xlim(20, 110)

    # Panel B: Pareto frontier
    ax2 = axes[1]

    cost_per_compliance = {
        'B_Exclusion': 1.5,
        'C_Moderate': 0.8,
        'C_Strict': 1.2,
        'D_Moderate_Combined': 2.0,
        'D_Strict_Combined': 2.5
    }

    all_points = []

    for policy_key, cost_factor in cost_per_compliance.items():
        for c in compliances:
            scenario_name = f'{policy_key}_{c}%'
            mean_val = np.mean(scenarios[scenario_name])
            reduction = (baseline_mean - mean_val) / baseline_mean * 100

            cost = c * cost_factor

            all_points.append({
                'policy': scenario_name,
                'cost': cost,
                'reduction': reduction,
                'compliance': c
            })

    # Plot points
    for point in all_points:
        policy_name = point['policy']
        c = point['compliance']

        if 'B_Exclusion' in policy_name:
            color, marker, size = '#3498DB', 'o', 100
        elif 'C_Moderate' in policy_name:
            color, marker, size = '#27AE60', 's', 100
        elif 'C_Strict' in policy_name and 'Combined' not in policy_name:
            color, marker, size = '#9B59B6', '^', 100
        elif 'D_Moderate' in policy_name:
            color, marker, size = '#F39C12', 'D', 120
        else:
            color, marker, size = '#E67E22', 'v', 120

        alpha = 0.4 + (c / 100) * 0.5

        ax2.scatter(point['cost'], point['reduction'],
                    c=color, marker=marker, s=size, alpha=alpha,
                    edgecolors='black', linewidths=1.5)

    # Pareto frontier
    sorted_points = sorted(all_points, key=lambda x: x['cost'])
    pareto_points = []
    max_reduction = -float('inf')

    for point in sorted_points:
        if point['reduction'] > max_reduction:
            pareto_points.append(point)
            max_reduction = point['reduction']

    pareto_costs = [p['cost'] for p in pareto_points]
    pareto_reductions = [p['reduction'] for p in pareto_points]

    ax2.plot(pareto_costs, pareto_reductions, 'r--', linewidth=3,
             label='Efficiency Frontier', alpha=0.7)

    ax2.set_xlabel('Relative Implementation Cost', fontweight='bold', fontsize=13)
    ax2.set_ylabel('Outbreak Reduction (%)', fontweight='bold', fontsize=13)
    ax2.set_title('B. Cost-Effectiveness Frontier', fontweight='bold', fontsize=14)
    ax2.grid(alpha=0.3, linestyle='--')

    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#3498DB',
               markersize=10, label='Exclusion', markeredgecolor='black'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#27AE60',
               markersize=10, label='Moderate Hygiene', markeredgecolor='black'),
        Line2D([0], [0], marker='^', color='w', markerfacecolor='#9B59B6',
               markersize=10, label='Strict Hygiene', markeredgecolor='black'),
        Line2D([0], [0], marker='D', color='w', markerfacecolor='#F39C12',
               markersize=10, label='Moderate Combined', markeredgecolor='black'),
        Line2D([0], [0], marker='v', color='w', markerfacecolor='#E67E22',
               markersize=10, label='Strict Combined', markeredgecolor='black'),
        Line2D([0], [0], color='red', linewidth=3, linestyle='--',
               label='Efficiency Frontier')
    ]
    ax2.legend(handles=legend_elements, frameon=True, shadow=True, fontsize=10)

    plt.tight_layout()
    plt.savefig('Figure4_Cost_Effectiveness.png', dpi=300, bbox_inches='tight')
    plt.savefig('Figure4_Cost_Effectiveness.pdf', bbox_inches='tight')
    plt.show()

    print("✓ Saved: Figure4_Cost_Effectiveness.png/pdf")

def create_figure5_distribution_comparisons(scenarios):
    """
    FIGURE 5: Distribution Comparisons
    Detailed distributional effects of key policies
    """

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # Panel A: Baseline vs best interventions (full distributions)
    ax1 = axes[0, 0]

    policies_to_compare = [
        ('A_Baseline', 'Baseline', '#E74C3C'),
        ('B_Exclusion_100%', 'Exclusion (100%)', '#3498DB'),
        ('C_Strict_100%', 'Strict Hygiene (100%)', '#9B59B6'),
        ('D_Strict_Combined_100%', 'Strict Combined (100%)', '#E67E22')
    ]

    for key, label, color in policies_to_compare:
        data = scenarios[key]
        ax1.hist(data, bins=50, alpha=0.5, label=label, color=color,
                edgecolor='black', linewidth=0.5, density=True)

    ax1.set_xlabel('Outbreak Size (cases)', fontweight='bold', fontsize=12)
    ax1.set_ylabel('Probability Density', fontweight='bold', fontsize=12)
    ax1.set_title('A. Distribution Comparison (100% Compliance)',
                  fontweight='bold', fontsize=13)
    ax1.legend(frameon=True, shadow=True, fontsize=11)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_xlim(0, 150)

    # Panel B: CDFs
    ax2 = axes[0, 1]

    for key, label, color in policies_to_compare:
        data = scenarios[key]
        sorted_data = np.sort(data)
        cdf = np.arange(1, len(sorted_data)+1) / len(sorted_data)
        ax2.plot(sorted_data, cdf, label=label, color=color, linewidth=3)

    ax2.set_xlabel('Outbreak Size (cases)', fontweight='bold', fontsize=12)
    ax2.set_ylabel('Cumulative Probability', fontweight='bold', fontsize=12)
    ax2.set_title('B. Cumulative Distribution Functions',
                  fontweight='bold', fontsize=13)
    ax2.legend(frameon=True, shadow=True, fontsize=11)
    ax2.grid(alpha=0.3, linestyle='--')
    ax2.set_xlim(0, 150)

    # Panel C: Percentile reduction across all policies
    ax3 = axes[1, 0]

    baseline = scenarios['A_Baseline']
    baseline_percentiles = np.percentile(baseline, [25, 50, 75, 90, 95, 99])

    percentile_labels = ['25th', '50th', '75th', '90th', '95th', '99th']

    compare_policies = [
        ('B_Exclusion_100%', 'Exclusion', '#3498DB'),
        ('C_Moderate_100%', 'Moderate Hyg', '#27AE60'),
        ('C_Strict_100%', 'Strict Hyg', '#9B59B6'),
        ('D_Strict_Combined_100%', 'Strict Comb', '#E67E22')
    ]

    x = np.arange(len(percentile_labels))
    width = 0.18

    for i, (key, label, color) in enumerate(compare_policies):
        policy_percentiles = np.percentile(scenarios[key], [25, 50, 75, 90, 95, 99])
        reductions = (baseline_percentiles - policy_percentiles) / baseline_percentiles * 100

        offset = (i - 1.5) * width
        ax3.bar(x + offset, reductions, width, label=label, color=color,
               alpha=0.8, edgecolor='black', linewidth=1)

    ax3.set_ylabel('Reduction (%)', fontweight='bold', fontsize=12)
    ax3.set_xlabel('Percentile', fontweight='bold', fontsize=12)
    ax3.set_title('C. Reduction by Outbreak Size Percentile',
                  fontweight='bold', fontsize=13)
    ax3.set_xticks(x)
    ax3.set_xticklabels(percentile_labels)
    ax3.legend(frameon=True, shadow=True, fontsize=10, ncol=2)
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)

    # Panel D: Tail prevention (>50 cases, >100 cases)
    ax4 = axes[1, 1]

    thresholds = [50, 100, 150]
    threshold_labels = ['>50', '>100', '>150']

    policies_for_tail = [
        ('A_Baseline', 'Baseline', '#E74C3C'),
        ('B_Exclusion_100%', 'Exclusion', '#3498DB'),
        ('C_Strict_100%', 'Strict Hyg', '#9B59B6'),
        ('D_Strict_Combined_100%', 'Strict Comb', '#E67E22')
    ]

    x = np.arange(len(threshold_labels))
    width = 0.2

    for i, (key, label, color) in enumerate(policies_for_tail):
        data = scenarios[key]
        percentages = []
        for threshold in thresholds:
            pct = (np.sum(data > threshold) / len(data)) * 100
            percentages.append(pct)

        offset = (i - 1.5) * width
        ax4.bar(x + offset, percentages, width, label=label, color=color,
               alpha=0.8, edgecolor='black', linewidth=1)

    ax4.set_ylabel('Probability of Large Outbreak (%)', fontweight='bold', fontsize=12)
    ax4.set_xlabel('Outbreak Size Threshold (cases)', fontweight='bold', fontsize=12)
    ax4.set_title('D. Large Outbreak Prevention', fontweight='bold', fontsize=13)
    ax4.set_xticks(x)
    ax4.set_xticklabels(threshold_labels)
    ax4.legend(frameon=True, shadow=True, fontsize=10, ncol=2)
    ax4.grid(axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig('Figure5_Distribution_Comparisons.png', dpi=300, bbox_inches='tight')
    plt.savefig('Figure5_Distribution_Comparisons.pdf', bbox_inches='tight')
    plt.show()

    print("✓ Saved: Figure5_Distribution_Comparisons.png/pdf")


# FULL WORKFLOW

def run_complete_analysis(calibrated_params, n_sims=1500):
    """
    Run complete comprehensive policy analysis.
    """

    print("\n" + "="*70)
    print("COMPREHENSIVE POLICY ANALYSIS")
    print("Testing 16 scenarios with publication-quality figures")
    print("="*70)

    # Run scenarios
    scenarios = run_comprehensive_policy_analysis(calibrated_params, N_runs=n_sims)

    # Create summary table
    print("\n" + "="*70)
    print("CREATING SUMMARY TABLE")
    print("="*70)
    summary_df = create_summary_table(scenarios)
    print("\n" + summary_df.to_string(index=False))
    summary_df.to_csv('Comprehensive_Policy_Summary.csv', index=False)
    print("\n✓ Saved: Comprehensive_Policy_Summary.csv")

    # Generate all figures
    print("\n" + "="*70)
    print("GENERATING PUBLICATION FIGURES")
    print("="*70)

    create_figure1_overview(scenarios, summary_df)
    create_figure2_hygiene_comparison(scenarios)
    create_figure3_policy_interactions(scenarios)
    create_figure4_cost_effectiveness(scenarios)
    create_figure5_distribution_comparisons(scenarios)

    print("\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)
    print("\nOutput files:")
    print("  - Comprehensive_Policy_Summary.csv")
    print("  - Figure1_Policy_Overview.png/pdf")
    print("  - Figure2_Hygiene_Comparison.png/pdf")
    print("  - Figure3_Policy_Interactions.png/pdf")
    print("  - Figure4_Cost_Effectiveness.png/pdf")
    print("  - Figure5_Distribution_Comparisons.png/pdf")
    print("\n" + "="*70)

    return scenarios, summary_df

# Example usage (standalone mode)

if __name__ == "__main__":

    # Example calibrated parameters
    calibrated_params = {
        'beta_handler_patron': 0.029285714285714286,
        'beta_staff_staff': 0.05,
        'prob_food_contamination': 0.10,
        'contamination_size_mean': 35.0,
        'contamination_size_std': 30
    }

    # Run complete analysis
    scenarios, summary = run_complete_analysis(calibrated_params, n_sims=1500)
