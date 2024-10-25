import pandas as pd
import matplotlib.pyplot as plt

# Define the filenames
filenames_festim_2 = [
    "festim_2_results_nprocs_1.csv",
    "festim_2_results_nprocs_2.csv",
    "festim_2_results_nprocs_3.csv",
    "festim_2_results_nprocs_4.csv",
]

filenames_festim_1 = [
    "festim_1_results_nprocs_1.csv",
    "festim_1_results_nprocs_2.csv",
    "festim_1_results_nprocs_3.csv",
    "festim_1_results_nprocs_4.csv",
]

# Read and process each CSV file
data_festim_2 = {}
for filename in filenames_festim_2:
    df = pd.read_csv(filename)
    nprocs = int(filename.split("_")[-1].split(".")[0])
    for size in df["size"].unique():
        if size not in data_festim_2:
            data_festim_2[size] = {"nb_cells": [], "times": [], "nb_procs": []}
        size_df = df[df["size"] == size]
        total_nb_cells = size_df["nb_cells"].sum()
        avg_time = size_df["time"].mean()
        data_festim_2[size]["nb_cells"].append(total_nb_cells)
        data_festim_2[size]["times"].append(avg_time)
        data_festim_2[size]["nb_procs"].append(nprocs)
print(data_festim_2)

data_festim_1 = {}
for filename in filenames_festim_1:
    df = pd.read_csv(filename)
    nprocs = int(filename.split("_")[-1].split(".")[0])
    for size in df["size"].unique():
        if size not in data_festim_1:
            data_festim_1[size] = {"nb_cells": [], "times": [], "nb_procs": []}
        size_df = df[df["size"] == size]
        total_nb_cells = size_df["nb_cells"].sum()
        avg_time = size_df["time"].mean()
        data_festim_1[size]["nb_cells"].append(total_nb_cells)
        data_festim_1[size]["times"].append(avg_time)
        data_festim_1[size]["nb_procs"].append(nprocs)
print(data_festim_1)
# Plotting
fig, ax = plt.subplots(ncols=2, nrows=2, figsize=(10, 10), sharex=True)
nb_proc = [1, 2, 3, 4]
sizes = list(data_festim_2.keys())

for i, size in enumerate(sizes):
    plt.sca(ax[i // 2, i % 2])
    plt.title(f"N = {data_festim_2[size]['nb_cells'][i]}")
    plt.plot(
        data_festim_2[size]["nb_procs"],
        data_festim_2[size]["times"],
        marker="o",
        label=f"fenicsx",
    )
    plt.plot(
        data_festim_1[size]["nb_procs"],
        data_festim_1[size]["times"],
        marker="o",
        label=f"1.3",
    )
    plt.xlabel("Number of Processes")
    plt.ylabel("Execution Time (s)")
    plt.ylim(bottom=0)

ax[0, 0].legend()

plt.tight_layout()
plt.show()
