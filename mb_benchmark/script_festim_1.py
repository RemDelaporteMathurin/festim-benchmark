import festim as F
import numpy as np
import time

assert hasattr(F, "Simulation"), "you should use FESTIM v1.x.x"


def run_festim_1(volume_file, facet_file):
    my_model = F.Simulation()
    my_model.mesh = F.MeshFromXDMF(
        volume_file=volume_file,
        boundary_file=facet_file,
    )

    tungsten = F.Material(id=1, D_0=1, E_D=0, S_0=1, E_S=0)

    copper = F.Material(id=2, D_0=1, E_D=0, S_0=2, E_S=0)

    my_model.materials = [tungsten, copper]

    my_model.traps = F.Traps(
        [
            F.Trap(
                k_0=1,
                E_k=tungsten.E_D,
                p_0=0.1,
                E_p=0.87,
                density=0.5,
                materials=tungsten,
            ),
            F.Trap(
                k_0=[1, 1],
                E_k=[tungsten.E_D, copper.E_D],
                p_0=[0.1, 0.1],
                E_p=[1.0, 0.5],
                density=[0.5, 0.5],
                materials=[tungsten, copper],
            ),
        ]
    )

    my_model.T = 600

    my_model.boundary_conditions = [
        F.DirichletBC(surfaces=[3], value=2, field=0),
        F.DirichletBC(surfaces=[5], value=0, field=0),
    ]

    my_model.settings = F.Settings(
        absolute_tolerance=1e-10,
        relative_tolerance=1e-10,
        maximum_iterations=15,
        traps_element_type="DG",
        chemical_pot=True,
        transient=True,
        final_time=10,
        linear_solver="mumps",
    )

    my_model.dt = F.Stepsize(1)

    my_model.exports = F.Exports(
        [
            F.XDMFExport("solute", folder="results_festim_1", checkpoint=True),
            F.XDMFExport("1", folder="results_festim_1", checkpoint=True),
            F.XDMFExport("2", folder="results_festim_1", checkpoint=True),
        ]
    )
    my_model.initialise()
    my_model.run()


if __name__ == "__main__":
    import pandas as pd
    from mpi4py import MPI

    # Get the number of processes
    comm = MPI.COMM_WORLD
    num_procs = comm.Get_size()
    rank = comm.Get_rank()
    if rank == 0:
        print(f"Number of processes: {num_procs}")
    times = []
    sizes = [0.1, 0.07, 0.05, 0.04]
    nb_cells = []
    ranks = []
    for size in sizes:
        print(f"Running for size {size}")
        volume_file = f"mesh/size_{size}/mesh.xdmf"
        facet_file = f"mesh/size_{size}/mf.xdmf"
        start_time = time.time()
        N = run_festim_1(volume_file=volume_file, facet_file=facet_file)
        nb_cells.append(N)
        end_time = time.time()
        ellapsed_time = end_time - start_time
        times.append(ellapsed_time)
        ranks.append(rank)
    print(sizes)
    print(times)
    print(nb_cells)

    # Gather data from all processes
    all_sizes = comm.gather(sizes, root=0)
    all_nb_cells = comm.gather(nb_cells, root=0)
    all_times = comm.gather(times, root=0)
    all_ranks = comm.gather(ranks, root=0)

    if rank == 0:
        # Flatten the lists
        all_ranks = [item for sublist in all_ranks for item in sublist]
        all_sizes = [item for sublist in all_sizes for item in sublist]
        all_nb_cells = [item for sublist in all_nb_cells for item in sublist]
        all_times = [item for sublist in all_times for item in sublist]

        # Create a DataFrame and save to CSV
        df = pd.DataFrame(
            {
                "rank": all_ranks,
                "size": all_sizes,
                "nb_cells": all_nb_cells,
                "time": all_times,
            }
        )
        df.to_csv(f"festim_1_results_nprocs_{num_procs}.csv", index=False)
        print(df)
