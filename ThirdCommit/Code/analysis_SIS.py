"""
            SIS Epidemology analysis programm
            Author : Jonas Hoecker
            Email : jonas.hoecker@unifr.ch

"""


import matplotlib.pyplot as plt

# matrix contains every calculations
file_names_set = [
		["unconnected_results_BIS1.txt", "unconnected_results_BIS2.txt", "unconnected_results_BIS3.txt", "unconnected_results_BIS4.txt"],
		["undirected_results_BIS1.txt", "undirected_results_BIS2.txt", "undirected_results_BIS3.txt", "undirected_results_BIS4.txt"],
		["clustering_results_BIS1.txt", "clustering_results_BIS2.txt", "clustering_results_BIS3.txt", "clustering_results_BIS4.txt"],
		["sh_results_N1.txt", "sh_results_N2.txt", "sh_results_N3.txt", "sh_results_N4.txt"]
	]
# introducing the plotting organization
fig, axes = plt.subplots(2, 2, figsize=(12,8))
axes = axes.flatten()

# loop for every different network
for idx, file_names in enumerate(file_names_set):

	final_infections_1 = []
	final_infections_2 = []
	final_infections_3 = []
	final_infections_4 = []

	beta_values = None

	# loop for every different calculation
	for i, file_name in enumerate(file_names):
		final_infections_temp = []
		beta_values_temp = []


		# read data
		with open(file_name, "r") as file:
			# skip info line
			next(file)
			# read line by line
			for line in file:
				# scanning result to variable
				beta, infections = line.split("\t")
				beta_values_temp.append(float(beta))
				final_infections_temp.append(float(infections))

			# determine beta (x-axis) values
			if beta_values is None:
				beta_values = beta_values_temp

			# determine the 4 different y-axis values
			if i == 0:
				final_infections_1 = final_infections_temp
			elif i == 1:
				final_infections_2 = final_infections_temp
			elif i == 2:
				final_infections_3 = final_infections_temp
			elif i == 3:
				final_infections_4 = final_infections_temp

	# preparing final y-axis variable
	final_infections = []
	# loop around every results
	for i in range(len(final_infections_1)):
		values = [
			final_infections_1[i],
			final_infections_2[i],
			final_infections_3[i],
			final_infections_4[i]
		]

		# taking only non-zero values
		non_zero_values = [val for val in values if val != 0]

		# average of all non-zero values to determine final value
		if len(non_zero_values) >= 1:
			avg_infections = sum(non_zero_values) / len(non_zero_values)
		# if no non-zero values -> final value will be 0
		else:
			avg_infections = 0

		# append final y-axis values
		final_infections.append(avg_infections)

	# plot the results (as subplot)
	axes[idx].plot(beta_values, final_infections, linestyle='-', color=f'C{idx}', linewidth=2, markersize=6)
	if idx == 0:
		axes[idx].set_title(f'Unconnected network')
	elif idx == 1:
		axes[idx].set_title(f'Undirected network')
	elif idx == 2:
		axes[idx].set_title(f'Clustering network')
	elif idx == 3:
		axes[idx].set_title(f'Social hubs network')
	axes[idx].set_xlabel("Beta")
	axes[idx].set_ylabel("Final infections")
	axes[idx].grid(True)

plt.suptitle('Final Infections Across Different Networks', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()


