
import numpy as np


def simulate_outbreak_policy(
    # Staff + restaurant defaults
    n_food_handlers=None,
    n_other_staff=None,
    init_infected=None,
    patrons_per_shift=None,
    patrons_per_handler=30,
    shifts_per_day=2,
    max_days=5,

    # Disease parameters
    latent_period=1.0,
    infectious_period=3.0,
    prob_symptomatic=0.7,

    # Calibrated transmission parameters
    beta_staff_staff=0.1,
    beta_handler_patron=0.02,
    beta_other_patron=0.001,
    prob_food_contamination=0.15,
    contamination_size_mean=45,
    contamination_size_std=30,

    # POLICY CONTROLS
    policy_exclusion=False,
    policy_hygiene=False,
    compliance=0.0,
    xi_max=0.4,
    omega=0.2,
    beta_mult=0.70
):
    """Simulate outbreak with policy interventions."""

    # Sample restaurant characteristics
    if n_food_handlers is None:
        n_food_handlers = np.random.choice([3, 4, 5, 6, 7],
                                           p=[0.1, 0.2, 0.4, 0.2, 0.1])
    if n_other_staff is None:
        n_other_staff = np.random.choice([3, 4, 5, 6],
                                         p=[0.2, 0.3, 0.3, 0.2])
    if init_infected is None:
        init_infected = np.random.choice([1, 2, 3],
                                         p=[0.6, 0.3, 0.1])
    if patrons_per_shift is None:
        patrons_per_shift = np.random.choice(
            [100, 125, 150, 175, 200],
            p=[0.2, 0.2, 0.3, 0.2, 0.1]
        )

    # Apply hygiene policy
    if policy_hygiene:
        hygiene_factor = 1 - (1 - beta_mult) * compliance
        beta_ss_eff = beta_staff_staff * hygiene_factor
        beta_hp_eff = beta_handler_patron * hygiene_factor
        prob_contam_eff = prob_food_contamination * hygiene_factor
    else:
        beta_ss_eff = beta_staff_staff
        beta_hp_eff = beta_handler_patron
        prob_contam_eff = prob_food_contamination

    # Apply exclusion policy
    xi_eff = compliance * xi_max if policy_exclusion else 0

    # Initialize staff states
    total_staff = n_food_handlers + n_other_staff
    staff_states = ['S'] * total_staff
    staff_infection_day = [None] * total_staff
    is_handler = [True] * n_food_handlers + [False] * n_other_staff
    excluded = [False] * total_staff

    # Seed infections
    idx = np.random.choice(total_staff, init_infected, replace=False)
    for i in idx:
        staff_states[i] = 'E'
        staff_infection_day[i] = 0.0

    total_staff_inf = init_infected
    total_pat_inf = 0

    # Main simulation loop
    for day in range(max_days):

        # Disease progression
        for i in range(total_staff):
            if staff_states[i] == 'E':
                if (day - staff_infection_day[i]) >= latent_period:
                    staff_states[i] = (
                        'Is' if np.random.rand() < prob_symptomatic else 'Ia'
                    )
            elif staff_states[i] in ['Ia', 'Is']:
                if (day - staff_infection_day[i]) >= (latent_period + infectious_period):
                    staff_states[i] = 'R'

        # Staff exclusion
        if policy_exclusion:
            for i in range(total_staff):
                if staff_states[i] == "Is" and not excluded[i]:
                    if np.random.rand() < xi_eff:
                        excluded[i] = True

            for i in range(total_staff):
                if excluded[i] and np.random.rand() < omega:
                    excluded[i] = False
                    staff_states[i] = 'R'

        # Identify infectious & susceptible
        infectious = [
            i for i in range(total_staff)
            if staff_states[i] in ["Ia", "Is"] and not excluded[i]
        ]
        susceptible = [
            i for i in range(total_staff)
            if staff_states[i] == "S" and not excluded[i]
        ]

        # Staff-to-staff transmission
        for s in susceptible:
            for inf in infectious:
                if staff_states[inf] == 'Is' and np.random.rand() < 0.5:
                    continue
                if np.random.rand() < beta_ss_eff:
                    staff_states[s] = "E"
                    staff_infection_day[s] = day + np.random.uniform(0, 1)
                    total_staff_inf += 1
                    break

        # Shifts
        for sh in range(shifts_per_day):
            infectious_handlers = []
            infectious_other = []

            for i in infectious:
                if staff_states[i] == "Is" and np.random.rand() < 0.5:
                    continue
                if is_handler[i]:
                    infectious_handlers.append(i)
                else:
                    infectious_other.append(i)

            # Handler-patron transmission
            for _ in infectious_handlers:
                total_pat_inf += np.random.binomial(patrons_per_handler, beta_hp_eff)

            # Other staff-patron transmission
            if len(infectious_other) > 0:
                total_pat_inf += np.random.binomial(
                    patrons_per_shift,
                    beta_other_patron * len(infectious_other)
                )

            # Food contamination
            if len(infectious_handlers) > 0:
                if np.random.rand() < prob_contam_eff:
                    sig = np.sqrt(np.log(
                        1 + (contamination_size_std / contamination_size_mean) ** 2))
                    mu = np.log(contamination_size_mean) - sig ** 2 / 2
                    contam_size = int(np.random.lognormal(mu, sig))
                    contam_size = max(
                        10,
                        min(contam_size, int(patrons_per_shift * 0.9))
                    )
                    total_pat_inf += contam_size

    return total_staff_inf + total_pat_inf
