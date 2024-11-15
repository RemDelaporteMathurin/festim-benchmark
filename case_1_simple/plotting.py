import pandas
import matplotlib.pyplot as plt
import numpy as np
from os import PathLike
from pathlib import Path
def plot_runtime(
    size: float,
    modern_filename: PathLike| None = None,
    legacy_filename: PathLike | None= None,
    show_ideal: bool = True,
):
    if modern_filename is not None:    
        tab = pandas.read_csv("results.csv", sep=",")
        filtered_tab = tab[tab["MeshSize"]==mesh_size]
        procs = filtered_tab["NumProcs"].array
        sort = np.argsort(procs)

        runtimes_mixed = filtered_tab["Mixed"].array[sort]
        runtimes_change_of_var = filtered_tab["ChangeVar"].array[sort]
        runtimes_penalty = filtered_tab["Penalty"].array[sort]
        num_procs = procs[sort]

        lines = []
        (l_mixed,) = plt.plot(
            num_procs, runtimes_mixed, marker="*", label=f"mixed domain", color="navy"
        )
        lines.append(l_mixed)
        if show_ideal and len(runtimes_mixed)>0:
            n = np.linspace(1, 16, 100)
            (l_ideal,) = plt.plot(
                n, runtimes_mixed[0] * n**-1, linestyle="--", color="tab:grey"
            )
            lines.append(l_ideal)
        # another green
        (l_penalty,) = plt.plot(
            num_procs, runtimes_penalty, marker="s", label="penalty", color="firebrick"
        )
        lines.append(l_penalty)
        if show_ideal and len(runtimes_penalty)>0:
            n = np.linspace(1, 16, 100)
            (l_ideal,) = plt.plot(
                n, runtimes_penalty[0] * n**-1, linestyle="--", color="tab:grey"
            )
            lines.append(l_ideal)
        if runtimes_change_of_var is not None:
            (l_change_var,) = plt.plot(
                num_procs,
                runtimes_change_of_var,
                marker="o",
                label="change of variable",
                color="forestgreen",
            )
            lines.append(l_change_var)
        if show_ideal and len(runtimes_change_of_var)>0:
            n = np.linspace(1, 16, 100)
            (l_ideal,) = plt.plot(
                n,
                runtimes_change_of_var[0] * n**-1,
                label="ideal",
                linestyle="--",
                color="tab:grey",
            )
            lines.append(l_ideal)

        if legacy_filename is not None:
            from pathlib import Path
            import pandas as pd
            infile = Path(legacy_filename, sep=",")
            data = pd.read_csv(infile)
            filtered_tab = data[data["MeshSize"]==size]
            procs = filtered_tab["NumProcs"].array
            sort_leg = np.argsort(procs)
            legacy = filtered_tab["ChangeVar"].array[sort_leg]
            (l_festim1,) = plt.plot(
                procs[sort_leg],
                legacy,
                marker="o",
                label="FESTIM v1.3.1",
                color="tab:red",
            )
            

    # for line in lines:
    #     plt.annotate(
    #         f"{line.get_label()}",
    #         (num_procs[-1], line.get_ydata()[-1]),
    #         textcoords="offset points",
    #         xytext=(5, 0),
    #         ha="left",
    #         va="center",
    #         color=line.get_color(),
    #     )

    # if runtimes_mixed  is not None or runtimes_change_of_var is not None or runtimes_penalty is not None:
    #     plt.annotate(
    #         "FESTIM 2",
    #         (num_procs[2], runtimes_change_of_var[2]),
    #         textcoords="offset points",
    #         xytext=(5, 30),
    #         ha="left",
    #         va="center",
    #         color="tab:green",
    #     )

    # plt.legend()
    plt.xlabel("Number of processes")
    plt.ylabel("Runtime (s)")

    plt.xscale("log")
    plt.yscale("log")

    # xticks only at the powers of 2
    plt.xticks(num_procs, num_procs)

    # remove top and right spines
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.legend()

mesh_size = 0.05
plot_runtime(mesh_size,"results.csv", "results_legacy.csv", show_ideal=True)
# ylim = plt.gca().get_ylim()
# xlim = plt.gca().get_xlim()
plt.savefig(f"all_{mesh_size:.5e}.png")
