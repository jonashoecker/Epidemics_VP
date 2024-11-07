"""
            SIS Epidemology Social Hubs degree distribution programm
            Author : Jonas Hoecker
            Email : jonas.hoecker@unifr.ch

"""


import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# copy of the implemetation of the social_hubs network
def social_hubs(N):
    # create dictionnary to initialize the network
    network = {i: [] for i in range(N)}

    # create an array of N values randomly determined by the pareto distribution
    pareto = np.random.pareto(2, N) * 20
    # fixing the type to integer
    pareto = pareto.astype(int)
    # loop around every values such that every person has a least one contact
    for i, value in enumerate(pareto):
        if value == 0:
            pareto[i] += 1

    # generating connections for each individual
    for person in range(N):
        # skips if the person has enough contacts
        if len(network[person]) >= pareto[person]:
            continue
        # removes the person and current connections to create the possible new contacts
        available_contacts = np.setdiff1d(np.arange(N), [person] + network[person])
        # filter to only include contacts that  have less than k connections
        available_contacts = available_contacts[[len(network[contact]) < pareto[contact] for contact in available_contacts]]
        # randomly select new contacts
        new_contacts = np.random.choice(available_contacts,
                                        min(pareto[person] - len(network[person]), len(available_contacts)),
                                        replace=False)
        # adds the contacts to the person in the dictionnary
        network[person].extend(new_contacts)
        # loop to ensure that that the connections are reciproqual
        for contact in new_contacts:
            network.setdefault(contact, []).append(person)

    return network

# Generate the social hubs network with a specified number of nodes
N = 1000
network = social_hubs(N)

# Calculate degree distribution
degree_counts = [len(connections) for connections in network.values()]
mean_degree = np.mean(degree_counts)

# Plot degree distribution on a log-log scale
degree_distribution = Counter(degree_counts)
degrees, counts = zip(*degree_distribution.items())

plt.figure(figsize=(10, 6))
plt.loglog(degrees, counts, marker='.', linestyle='none', color='green')
plt.title("Degree Distribution for Social Hubs Network (Log-Log Scale)")
plt.xlabel("Degree (number of connections)")
plt.ylabel("Count")
plt.grid(True, which="both", linestyle="--", lw=0.5)
plt.show()

# Output the mean degree
print('The mean degree is : ', mean_degree)
