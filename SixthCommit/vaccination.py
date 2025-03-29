"""
            SIS Epidemology vaccination analysis programm
            Author : Jonas Hoecker
            Email : jonas.hoecker@unifr.ch

"""

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

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

def simulate_with_vaccin(network, N, k, beta, delta, days, vaccinated):

	# initialize states of individuals (true/false)
	states = np.zeros(N, dtype=bool)
	# get array of every people in the network who are not vaccinated
	non_vaccinated = np.setdiff1d(np.arange(N), vaccinated)
	# apply initially infected people
	initially_infected = np.random.choice(non_vaccinated, 2000, replace=False)
	states[initially_infected] = True

	# introduce variable of infected people
	infected_count = []
	# loop around every event
	for day in enumerate(tqdm(range(days), desc='Days')):
		# duplication of array
		new_infections = np.zeros(N, dtype=bool)

		# new infections
		for person, is_infected in enumerate(states):
			# case of possible transfer if person is infected
			if is_infected:
				contacts = network[person]
				for contact in contacts:
					# randomly determine if contact will be infected using beta variable 
					# add check if not vaccinated
					if contact not in vaccinated and np.random.rand() < beta:
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

	return infected_count


def main():

	# Parameters
	N = 10000 # number of individuals
	k = 3 # number of links between individuals
	delta = 0.17 # recovery rate
	days = 500 # number of days (ie/ number of events)

	# define single beta value
	beta = 0.1

	# define network
	network = social_hubs(N)

	# define single beta value
	beta = 0.1

	# define array for vaccinations values
	vaccination_levels = np.linspace(0.01, 0.1, 11)
	no_vac = []
	random_vac = []
	top_degree_vac = []
	friend_vac = []
	for v in vaccination_levels:
		v_N = int(v * N)

		# scenario 1 : no vaccination
		print('No vaccination calc ...')
		no_vaccin = simulate_with_vaccin(network, N, k, beta, delta, days, [])
		no_vac.append(no_vaccin[-1])

		# scenario 2 : v random nodes are vaccinated
		print('Random vaccination calc...')
		random_vaccinated = np.random.choice(N, v_N, replace=False)
		random_vaccin = simulate_with_vaccin(network, N, k, beta, delta, days, random_vaccinated)
		random_vac.append(random_vaccin[-1])

		# scenario 3 : top degree nodes are vaccinated
		print('High contact vaccination calc...')
		degrees = {node: len(neighbors) for node, neighbors in network.items()}
		top_degrees = sorted(degrees, key=degrees.get, reverse=True)[:v_N]
		top_degree_vaccin = simulate_with_vaccin(network, N, k, beta, delta, days, top_degrees)
		top_degree_vac.append(top_degree_vaccin[-1])

		# scenario 4 : random friends vaccinated
		print('Friends vaccination calc...')
		random_friends = set()
		while len(random_friends) < v_N:
			person = np.random.randint(N)
			friends = network[person]
			if friends:
				friend = np.random.choice(friends)
				random_friends.add(friend)
		random_friends = np.array(list(random_friends))
		friend_vaccin = simulate_with_vaccin(network, N, k, beta, delta, days, random_friends)
		friend_vac.append(friend_vaccin[-1])

	# plot results
	plt.figure(figsize=(10, 6))
	plt.plot(vaccination_levels * 100, no_vac, label='No vaccin', linestyle='--', marker='o')
	plt.plot(vaccination_levels * 100, random_vac, label='Random vaccin', linestyle='-', marker='s')
	plt.plot(vaccination_levels * 100, top_degree_vac, label='Top-degree vaccin', linestyle='-', marker='^')
	plt.plot(vaccination_levels * 100, friend_vac, label='Friends vaccin', linestyle='-', marker='d')

	plt.xlabel("Vaccination coverage (%)", fontsize=12)
	plt.ylabel("Number of infected individuals (final day)", fontsize=12)
	plt.title("Effectiveness of Vaccination Strategies", fontsize=14)
	plt.legend(fontsize=10)
	plt.grid(True, linestyle='--', alpha=0.6)
	plt.tight_layout()
	plt.show()


main()
