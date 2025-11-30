
import numpy as np

def simulate_restaurant_outbreak_v3(
        n_food_handlers=None, n_other_staff=None, init_infected=None,
        patrons_per_shift=None, shift_hours=8, shifts_per_day=2,
        patrons_per_handler=30, max_days=5, latent_period=1.0,
        infectious_period=3.0, prob_symptomatic=0.7,
        beta_staff_staff=0.1, beta_handler_patron=0.02,
        beta_other_patron=0.001, prob_food_contamination=0.15,
        contamination_size_mean=45, contamination_size_std=30):

    # Random restaurant configuration if not specified
    if n_food_handlers is None:
        n_food_handlers = np.random.choice([3,4,5,6,7], p=[0.1,0.2,0.4,0.2,0.1])
    if n_other_staff is None:
        n_other_staff = np.random.choice([3,4,5,6], p=[0.2,0.3,0.3,0.2])
    if init_infected is None:
        init_infected = np.random.choice([1,2,3], p=[0.6,0.3,0.1])
    if patrons_per_shift is None:
        patrons_per_shift = np.random.choice([100,125,150,175,200],
                                             p=[0.2,0.2,0.3,0.2,0.1])

    total_staff = n_food_handlers + n_other_staff
    staff_states = ['S'] * total_staff
    staff_infection_day = [None] * total_staff
    is_handler = [True]*n_food_handlers + [False]*n_other_staff

    # Seed initial infections
    idxs = np.random.choice(total_staff, init_infected, replace=False)
    for x in idxs:
        staff_states[x] = 'E'
        staff_infection_day[x] = 0.0

    staff_inf_count = init_infected
    pat_inf = 0

    # Daily simulation
    for day in range(max_days):

        # Disease progression
        for i in range(total_staff):
            if staff_states[i] == 'E':
                if (day - staff_infection_day[i]) >= latent_period:
                    staff_states[i] = 'Is' if np.random.rand() < prob_symptomatic else 'Ia'

            elif staff_states[i] in ['Ia','Is']:
                if (day - staff_infection_day[i]) >= (latent_period + infectious_period):
                    staff_states[i] = 'R'

        # Staff-to-staff transmission
        inf_staff = [i for i in range(total_staff) if staff_states[i] in ['Ia','Is']]
        sus_staff = [i for i in range(total_staff) if staff_states[i] == 'S']

        for s in sus_staff:
            for z in inf_staff:
                if staff_states[z] == 'Is' and np.random.rand() < 0.5:
                    continue
                if np.random.rand() < beta_staff_staff:
                    staff_states[s] = 'E'
                    staff_infection_day[s] = day + np.random.uniform(0,1)
                    staff_inf_count += 1
                    break

        # Staff-to-patron transmission
        for sh in range(shifts_per_day):

            inf_handlers = []
            inf_other = []

            for i in range(total_staff):
                if staff_states[i] in ['Ia','Is']:
                    if staff_states[i]=='Is' and np.random.rand()<0.5:
                        continue
                    if is_handler[i]:
                        inf_handlers.append(i)
                    else:
                        inf_other.append(i)

            # Handler → patron
            for hh in inf_handlers:
                pat_inf += np.random.binomial(patrons_per_handler, beta_handler_patron)

            # Other staff → patron
            if len(inf_other)>0:
                pat_inf += np.random.binomial(patrons_per_shift,
                                              beta_other_patron*len(inf_other))

            # Food contamination event
            if len(inf_handlers)>0:
                if np.random.rand() < prob_food_contamination:
                    sig = np.sqrt(np.log(1+(contamination_size_std/contamination_size_mean)**2))
                    mu = np.log(contamination_size_mean) - sig**2/2
                    sizee = int(np.random.lognormal(mu, sig))
                    sizee = max(10, min(sizee, int(patrons_per_shift*0.9)))
                    pat_inf += sizee

    return staff_inf_count + pat_inf
