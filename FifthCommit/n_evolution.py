import matplotlib.pyplot as plt

# File sets for two different networks
file_names_set_undi = {
    "N = 1000": ['FINAL_UNDI_1000_1.txt', 'FINAL_UNDI_1000_2.txt', 'FINAL_UNDI_1000_3.txt'],
    "N = 3000": ['FINAL_UNDI_3000_1.txt', 'FINAL_UNDI_3000_2.txt'],
    "N = 10000": ["UNIDIRECTED_N10000.txt"]
}

file_names_set_hubs = {
    "N = 1000": ['HUBS_N1000.txt', 'HUBS_N1000_2.txt', 'HUBS_N1000_3.txt'],
    "N = 3000": ['HUBS_N3000.txt', 'HUBS_N3000_2.txt'],
    "N = 10000": ["FINAL_HUBS_10000_2.txt"]
}

# Define colors and line styles
colors = {"N = 1000": "blue", "N = 3000": "red", "N = 10000": "green"}
line_styles = ["-", "--", ":"]

# Create a figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot for Undirected Network
axes[0].grid(True, linestyle="--", alpha=0.5)
for label, file_names in file_names_set_undi.items():
    for i, file_name in enumerate(file_names):
        beta_values, final_infections = [], []
        with open(file_name, "r") as file:
            next(file)
            for line in file:
                beta, infections = line.split("\t")
                beta_values.append(float(beta))
                final_infections.append(float(infections))
        axes[0].plot(beta_values, final_infections, color=colors[label], alpha=0.6 if i > 0 else 1, label=label if i == 0 else "")
axes[0].set_xlim(0.05, 0.15)
axes[0].set_ylim(0, 4000)
axes[0].set_xlabel("Beta", fontsize=12)
axes[0].set_ylabel("Final Infections", fontsize=12)
axes[0].set_title("Undirected Network", fontsize=14, fontweight="bold")
axes[0].legend(fontsize=10)

# Plot for Social Hubs Network
axes[1].grid(True, linestyle="--", alpha=0.5)
for label, file_names in file_names_set_hubs.items():
    for i, file_name in enumerate(file_names):
        beta_values, final_infections = [], []
        with open(file_name, "r") as file:
            next(file)
            for line in file:
                beta, infections = line.split("\t")
                beta_values.append(float(beta))
                final_infections.append(float(infections))
        axes[1].plot(
            beta_values,
            final_infections,
            color=colors[label],
            linestyle=line_styles[i % len(line_styles)],  
            marker="o",
            markersize=4,
            alpha=0.7 if i > 0 else 1,
            label=label if i == 0 else ""
        )
axes[1].set_xlim(0.0, 0.01)
axes[1].set_ylim(0, 1000)
axes[1].set_xlabel("Beta", fontsize=12)
axes[1].set_title("Social Hubs Network", fontsize=14, fontweight="bold")
axes[1].legend(fontsize=10)

fig.suptitle("Network size analysis", fontsize=16, fontweight="bold")

# Adjust layout
plt.tight_layout()
plt.show()
