"""
            SIS Epidemology calculation programm
            Author : Jonas Hoecker
            Email : jonas.hoecker@unifr.ch

"""

import numpy as np
from tqdm import tqdm

def unconected(N, k):
    # create dictionnary to initialize the network
    network = {}

    # generating connections for each individual
    for person in range(N):
        # chooses randomly beetween every contact except himself
        contacts = np.random.choice(np.delete(np.arange(N), person), k, replace=False)
        # adds the contacts to the person in the dictionnary
        network[person] = contacts

    return network

def undirected(N, k):
    # create dictionnary to initialize the network
    network = {i: [] for i in range(N)}

    # generating connections for each individual
    for person in range(N):
        # skips if the person has enough contacts
        if len(network[person]) >= k:
            continue
        # removes the person and current connections to create the possible new contacts
        available_contacts = np.setdiff1d(np.arange(N), [person] + network[person])
        # filter to only include contacts that  have less than k connections
        available_contacts = available_contacts[[len(network[contact]) < k for contact in available_contacts]]
        # randomly select new contacts
        new_contacts = np.random.choice(available_contacts, min(k - len(network[person]), len(available_contacts)),
                                        replace=False)
        # adds the contacts to the person in the dictionnary
        network[person].extend(new_contacts)
        # loop to ensure that that the connections are reciproqual
        for contact in new_contacts:
            network.setdefault(contact, []).append(person)

    return network

def clustering(N, k):
    # create dictionnary to initialize the network
    network = {i: [] for i in range(N)}
    # introducing the probability variable that B and C are also in contact
    friend_proba = 0.3

    # generating connections for each individual
    for person in range(N):
        # skips if the person has enough contacts
        if len(network[person]) >= k:
            continue
        # removes the person and current connections to create the possible new contacts
        available_contacts = np.setdiff1d(np.arange(N), [person] + network[person])
        # filter to only include contacts that  have less than k connections
        available_contacts = available_contacts[[len(network[contact]) < k for contact in available_contacts]]
        # randomly select new contacts
        new_contacts = np.random.choice(available_contacts, min(k - len(network[person]), len(available_contacts)),
                                        replace=False)
        # adds the contacts to the person in the dictionnary
        network[person].extend(new_contacts)
        # loop to ensure that that the connections are reciproqual
        for contact in new_contacts:
            network.setdefault(contact, []).append(person)
        # loop around every new contact
        for contact in new_contacts:
            for potential_friend in new_contacts:
                # checks if the potential friend is not the person itself and not already a friend
                if (potential_friend not in network[contact]) and (contact != potential_friend):
                    # check if the friend capacity is smaller than k
                    if (len(network[contact]) < k and len(network[potential_friend]) < k):
                        # random choice to determine if they are going to be friends
                        if (np.random.rand() < friend_proba):
                            #adding the potential friend to the contact
                            network.setdefault(contact, []).append(potential_friend)
                            # reciprocally adding the contact to the potential friend
                            network.setdefault(potential_friend, []).append(contact)

    return network

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


def simulate_epidemics(N, k, beta, delta, days):
    # Choose network to work on
    network = unconected(N, k)
    #network = undirected(N, k)
    #network = clustering(N, k)
    #network = social_hubs(N)

    # initialize states of individuals (true/false array)
    states = np.zeros(N, dtype=bool)
    # chooses 3 random people that are infected at the beginning
    states[np.random.choice(N, 3, replace=False)] = True

    # introduce variable of infected people
    infected_count = []
    # loop around every event
    for day in range(days):
        # duplication of array
        new_infections = np.zeros(N, dtype=bool)

        # new infections
        for person, is_infected in enumerate(states):
            # case of possible transfer if person if infected
            if is_infected:
                contacts = network[person]
                for contact in contacts:
                    # randomly determine if contact will be infected using beta variable
                    if np.random.rand() < beta:
                        new_infections[contact] = True
        # comparing arrays to maintain old and new infected people
        states = np.logical_or(states, new_infections)

        # recoveries
        for person, is_infected in enumerate(states):
            if is_infected:
                # randomly determine if person will be recovered using delta variable
                if np.random.rand() < delta:
                    states[person] = False

        # counting the number of infected people
        infected_count.append(np.sum(states))

    return infected_count[-1], infected_count

def main():

    # Parameters
    N = 10000 # number of individuals
    k = 3 # number of links between individuals
    delta = 0.17 # recovery rate
    days = 500 # number of days (ie. number of events)

    beta_values = np.linspace(0, 0.7, 100) # beta values from 0 to 0.7
    final_infections = np.empty(len(beta_values)) # array of the number of final infections
    # simulation with different beta values
    for i, beta in enumerate(tqdm(beta_values, desc="Calculating beta values")):
        final_infections[i] = simulate_epidemics(N, k, beta, delta, days)[0]

    # writing results to a text file
    with open("unconnected_results_BIS4.txt", "w") as file:
        file.write("Beta\tFinal Infections\n")
        for beta, infections in zip(beta_values, final_infections):
            file.write(f"{beta:.4f}\t{infections}\n")

    # information messsage
    print("Simulation results have been saved to 'unconnected_results_BIS4.txt' file.")

main()




