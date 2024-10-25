import festim as F
import numpy as np
from mpi4py import MPI
import time

assert hasattr(
    F, "HydrogenTransportProblem"
), "you should use FESTIM on the fenicsx branch"


import dolfinx

# dolfinx.log.set_log_level(dolfinx.log.LogLevel.INFO)


def run_festim_2(volume_file, facet_file):

    my_model = F.HTransportProblemDiscontinuous()
    my_model.show_progress_bar = False
    my_model.mesh = F.MeshFromXDMF(
        volume_file=volume_file,
        facet_file=facet_file,
    )

    tungsten = F.Material(D_0=1, E_D=0, K_S_0=1, E_K_S=0)

    copper = F.Material(D_0=1, E_D=0, K_S_0=2, E_K_S=0)

    vol1 = F.VolumeSubdomain(id=1, material=tungsten)
    vol2 = F.VolumeSubdomain(id=2, material=copper)
    surface1 = F.SurfaceSubdomain(id=3)

    interface1 = F.Interface(id=4, subdomains=[vol1, vol2], penalty_term=10.0)

    surface2 = F.SurfaceSubdomain(id=5)

    my_model.subdomains = [vol1, vol2, surface1, surface2]

    mobile = F.Species(name="H", subdomains=my_model.volume_subdomains, mobile=True)
    trapped_1a = F.Species(name="H_trapped_W1", subdomains=[vol1], mobile=False)
    trapped_1b = F.Species(name="H_trapped_W2", subdomains=[vol1], mobile=False)
    trapped_2 = F.Species(name="H_trapped_cu", subdomains=[vol2], mobile=False)
    empty_1a = F.ImplicitSpecies(n=0.5, others=[trapped_1a])
    empty_1b = F.ImplicitSpecies(n=0.5, others=[trapped_1b])
    empty_2 = F.ImplicitSpecies(n=0.5, others=[trapped_2])

    my_model.species = [mobile, trapped_1a, trapped_1b, trapped_2]

    my_model.reactions = [
        F.Reaction(
            reactant=[mobile, empty_1a],
            product=[trapped_1a],
            k_0=1,
            E_k=tungsten.E_D,
            p_0=0.1,
            E_p=0.87,
            volume=vol1,
        ),
        F.Reaction(
            reactant=[mobile, empty_1b],
            product=[trapped_1b],
            k_0=1,
            E_k=tungsten.E_D,
            p_0=0.1,
            E_p=1.0,
            volume=vol1,
        ),
        F.Reaction(
            reactant=[mobile, empty_2],
            product=[trapped_2],
            k_0=1,
            E_k=copper.E_D,
            p_0=0.1,
            E_p=0.5,
            volume=vol2,
        ),
    ]

    my_model.temperature = 600
    my_model.boundary_conditions = [
        F.FixedConcentrationBC(subdomain=surface1, species=mobile, value=2),
        F.FixedConcentrationBC(subdomain=surface2, species=mobile, value=0),
    ]

    my_model.interfaces = [interface1]
    my_model.surface_to_volume = {
        surface1: vol1,
        surface2: vol2,
    }

    my_model.settings = F.Settings(atol=1e-6, rtol=1e-6, final_time=10)
    my_model.settings.stepsize = F.Stepsize(1)

    # mobile_exports = [
    #     F.VTXExport(
    #         f"results_festim_2/mobile_{subdomain.id}.bp",
    #         field=mobile,
    #         subdomain=subdomain,
    #     )
    #     for subdomain in my_model.volume_subdomains
    # ]
    # trapped_exports = [
    #     F.VTXExport(
    #         f"results_festim_2/trapped_{vol1.id}a.bp",
    #         field=trapped_1a,
    #         subdomain=vol1,
    #     ),
    #     F.VTXExport(
    #         f"results_festim_2/trapped_{vol1.id}b.bp",
    #         field=trapped_1b,
    #         subdomain=vol1,
    #     ),
    #     F.VTXExport(
    #         f"results_festim_2/trapped_{vol2.id}.bp",
    #         field=trapped_2,
    #         subdomain=vol2,
    #     ),
    # ]

    # my_model.exports = mobile_exports + trapped_exports
    my_model.initialise()
    my_model.run()

    nb_cells = len(my_model.volume_meshtags.indices)
    return nb_cells


if __name__ == "__main__":
    import pandas as pd

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
        if rank == 0:
            print(f"Running for size {size}")
        volume_file = f"mesh/size_{size}/mesh.xdmf"
        facet_file = f"mesh/size_{size}/mf.xdmf"
        start_time = time.time()
        N = run_festim_2(volume_file=volume_file, facet_file=facet_file)
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
        df.to_csv(f"festim_2_results_nprocs_{num_procs}.csv", index=False)
        print(df)
