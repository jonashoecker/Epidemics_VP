import matplotlib.pyplot as plt

file_names = ['unconnected_results.txt', 'undirected_results.txt', 'clustering_results.txt', 'social_hubs_results.txt']
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

for i, file_name in enumerate(file_names):
    beta_values = []
    final_infections = []

    with open(file_name, "r") as file:
        next(file)
        for line in file:
            beta, infections = line.split("\t")
            beta_values.append(float(beta))
            final_infections.append(float(infections))

    axes[i].plot(beta_values, final_infections, linestyle='-')
    axes[i].set_title(f'Data from {file_name}')
    axes[i].set_xlabel("Beta")
    axes[i].set_ylabel("Final Infections")
    axes[i].grid(True)

plt.tight_layout()
plt.show()
