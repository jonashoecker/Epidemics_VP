"""
            SIS Epidemology social-hubs network analysis programm
            Author : Jonas Hoecker
            Email : jonas.hoecker@unifr.ch

"""


import matplotlib.pyplot as plt

# files array variable
file_names = ["sh_results_N1.txt", "sh_results_N2.txt", "sh_results_N3.txt", "sh_results_N4.txt"]

# loop around every calculations
for i, file_name in enumerate(file_names):
	# x-axis, y-axis variables
	beta_values = []
	final_infections = []

	# read data
	with open(file_name, "r") as file:
		# skip info line
		next(file)
		# read line by line
		for line in file:
			# scanning result to variable
			beta, infections = line.split("\t")
			beta_values.append(float(beta))
			final_infections.append(float(infections))

		# plot results
		plt.plot(beta_values, final_infections, linestyle='-')
		plt.grid(True)

# set x-axis limits to only see the start of the measurements
plt.xlim(0, 0.05)
# set y-axis for presentation reasons
plt.ylim(0, 6000)
plt.xlabel("Beta")
plt.ylabel("Final infections")
plt.title("Infections growth near zero in social hubs network", fontsize=16, fontweight='bold')
plt.show()