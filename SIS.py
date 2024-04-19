import numpy as np
import matplotlib.pyplot as plt

def simulate_epidemics(N, k, beta, delta, days):
    # create dictionnary to initialize the network
    network = {}

    # generating connections for each individual
    for person in range(N):
        contacts = np.random.choice(np.delete(np.arange(N), person), k, replace=False)
        network[person] = contacts

    # initialize states of individuals (true/false array)
    states = np.zeros(N, dtype=bool)
    states[np.random.choice(N, 3, replace=False)] = True

    infected_count = []
    for day in range(days):
        new_infections = np.zeros(N, dtype=bool)

        # new infections
        for person, is_infected in enumerate(states):
            if is_infected:
                contacts = network[person]
                for contact in contacts:
                    if np.random.rand() < beta:
                        new_infections[contact] = True
        states = np.logical_or(states, new_infections)

        # recoveries
        for person, is_infected in enumerate(states):
            if is_infected:
                if np.random.rand() < delta:
                    states[person] = False

        infected_count.append(np.sum(states))

    return infected_count[-1], infected_count

# Parameters
N = 1000 # number of individuals
k = 3 # number of links between individuals
delta = 0.2 # recovery rate
days = 500 # number of days (ie. number of events)

beta_values = np.linspace(0, 0.7, 50) # beta values from 0 to 0.7
final_infections = np.empty(len(beta_values))

# Plot infected people as a function of time for two different beta values
for beta_value in [0.12, 0.2]:
    final_infection, infections_over_time = simulate_epidemics(N, k, beta_value, delta, days)
    plt.plot(range(days), infections_over_time, label=f'Beta = {beta_value}')
plt.xlabel("Days")
plt.ylabel("Number of infections")
plt.title("Infections over Time")
plt.legend()
plt.show()

for i, beta in enumerate(beta_values):
    final_infections[i] = simulate_epidemics(N, k, beta, delta, days)[0]

# Plot final number of infections as a function of beta
plt.plot(beta_values, final_infections)
plt.xlabel("Beta")
plt.ylabel("Final number of infections")
plt.title("Final Infections vs. Beta")
plt.show()