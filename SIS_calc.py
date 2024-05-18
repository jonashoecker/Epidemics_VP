import numpy as np
from tqdm import tqdm

def unconected(N, k):
    # create dictionnary to initialize the network
    network = {}

    # generating connections for each individual
    for person in range(N):
        contacts = np.random.choice(np.delete(np.arange(N), person), k, replace=False)
        network[person] = contacts

    return network

def undirected(N, k):
    # create dictionnary to initialize the network
    network = {i: [] for i in range(N)}

    # generating connections for each individual
    for person in range(N):
        if len(network[person]) >= k:
            continue
        available_contacts = np.setdiff1d(np.arange(N), [person] + network[person])
        available_contacts = available_contacts[[len(network[contact]) < k for contact in available_contacts]]
        new_contacts = np.random.choice(available_contacts, min(k - len(network[person]), len(available_contacts)),
                                        replace=False)
        network[person].extend(new_contacts)
        for contact in new_contacts:
            network.setdefault(contact, []).append(person)

    return network

def clustering(N, k):
    # create dictionnary to initialize the network
    network = {i: [] for i in range(N)}
    friend_proba = 0.3

    # generating connections for each individual
    for person in range(N):
        if len(network[person]) >= k:
            continue
        available_contacts = np.setdiff1d(np.arange(N), [person] + network[person])
        available_contacts = available_contacts[[len(network[contact]) < k for contact in available_contacts]]
        new_contacts = np.random.choice(available_contacts, min(k - len(network[person]), len(available_contacts)),
                                        replace=False)
        network[person].extend(new_contacts)
        for contact in new_contacts:
            network.setdefault(contact, []).append(person)
        for contact in new_contacts:
            for potential_friend in new_contacts:
                if (potential_friend not in network[contact]) and (contact != potential_friend):
                    if (len(network[contact]) < k and len(network[potential_friend]) < k):
                        if (np.random.rand() < friend_proba):
                            network.setdefault(contact, []).append(potential_friend)
                            network.setdefault(potential_friend, []).append(contact)

    return network

def social_hubs(N):
    # create dictionnary to initialize the network
    network = {i: [] for i in range(N)}

    pareto = np.random.pareto(2, N) * 20
    pareto = pareto.astype(int)
    for i, value in enumerate(pareto):
        if value == 0:
            pareto[i] += 1

    # generating connections for each individual
    for person in range(N):
        if len(network[person]) >= pareto[person]:
            continue
        available_contacts = np.setdiff1d(np.arange(N), [person] + network[person])
        available_contacts = available_contacts[
            [len(network[contact]) < pareto[contact] for contact in available_contacts]]
        new_contacts = np.random.choice(available_contacts,
                                        min(pareto[person] - len(network[person]), len(available_contacts)),
                                        replace=False)
        network[person].extend(new_contacts)
        for contact in new_contacts:
            network.setdefault(contact, []).append(person)

    return network


def simulate_epidemics(N, k, beta, delta, days):
    #network = unconected(N, k)
    #network = undirected(N, k)
    #network = clustering(N, k)
    network = social_hubs(N)

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
N = 10000 # number of individuals
k = 3 # number of links between individuals
delta = 0.2 # recovery rate
days = 500 # number of days (ie. number of events)

beta_values = np.linspace(0, 0.7, 100) # beta values from 0 to 0.7
final_infections = np.empty(len(beta_values))
for i, beta in enumerate(tqdm(beta_values, desc="Calculating beta values")):
    final_infections[i] = simulate_epidemics(N, k, beta, delta, days)[0]

# writing results to a text file
with open("social_hubs_results.txt", "w") as file:
    file.write("Beta\tFinal Infections\n")
    for beta, infections in zip(beta_values, final_infections):
        file.write(f"{beta:.4f}\t{infections}\n")

print("Simulation results have been saved to 'social_hubs_results.txt' file.")