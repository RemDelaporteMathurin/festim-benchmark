from mesh import three_cubes
import argparse
import numpy as np
from pathlib import Path

def run_legacy(volume_file: str, facet_file: str) -> float:
    from script_festim_1 import run_festim_1
    import time

    start = time.perf_counter()
    run_festim_1(volume_file, facet_file)
    end = time.perf_counter()

    elapsed_time = end - start


    return elapsed_time

def run(volume_file: str, facet_file: str) -> float:
    from mpi4py import MPI
    from script_festim_2 import run_festim_2
    import time
    MPI.COMM_WORLD.Barrier()
    start = time.perf_counter()
    run_festim_2(volume_file, facet_file)
    end = time.perf_counter()

    elapsed_time = end - start


    return elapsed_time

# +
def run_change_of_var(volume_file: str, facet_file: str) -> float:
    from mpi4py import MPI

    from script_festim_2 import run_festim_2_change_of_var
    import time
    MPI.COMM_WORLD.Barrier()
    start = time.perf_counter()
    run_festim_2_change_of_var(volume_file, facet_file)
    end = time.perf_counter()

    elapsed_time = end - start


    return elapsed_time

def run_penalty(volume_file: str, facet_file: str) -> float:
    from mpi4py import MPI
    from script_festim_2 import run_festim_2_penalty
    import time
    MPI.COMM_WORLD.Barrier()
    start = time.perf_counter()
    run_festim_2_penalty(volume_file, facet_file)
    end = time.perf_counter()

    elapsed_time = end - start


    return elapsed_time

parser = argparse.ArgumentParser(argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--size", "-s", type=float, dest="size", help="size of mesh", default=0.1)
parser.add_argument("--gmsh", "-g", action="store_true", dest="generate_mesh", default=False, help="Generate mesh with GMSH")
parser.add_argument("--legacy", "-l", action="store_true", dest="run_legacy", default=False, help="Run festim LEGACY (1)")
parser.add_argument("--modern", "-x", action="store_true", dest="run_dolfinx", default=False, help="Run festim 2")

if __name__ == "__main__":

    args = parser.parse_args()

    size = args.size

    filename = f"meshes/mesh_{size}.msh"
    # +

    volume_file = f"meshes/mesh_{size}.xdmf"
    facet_file = f"meshes/mesh_{size}_facet.xdmf"
    if args.generate_mesh:
        from mpi4py import MPI
        from convert_mesh import convert_mesh
        if MPI.COMM_WORLD.rank == 0:
            three_cubes(filename, size=size)
        MPI.COMM_WORLD.Barrier()

        if MPI.COMM_WORLD.rank == 0:
            nb_cells, nb_facets = convert_mesh(filename, volume_file, facet_file)
        MPI.COMM_WORLD.Barrier()


    if args.run_dolfinx:
        from mpi4py import MPI
        import dolfinx

        elapsed_times =  MPI.COMM_WORLD.gather(run(volume_file, facet_file), root=0)
        if MPI.COMM_WORLD.rank == 0:
            print(f"Mixed: {elapsed_times} seconds")

        runtime_changes = MPI.COMM_WORLD.gather(run_change_of_var(volume_file, facet_file), root=0)
        if MPI.COMM_WORLD.rank == 0:
            print(f"Change of var: {runtime_changes} seconds")

        runtimes_penalty = MPI.COMM_WORLD.gather(run_penalty(volume_file, facet_file), root=0)
        if MPI.COMM_WORLD.rank == 0:
            print(f"Penalty: {runtimes_penalty} seconds")

        if MPI.COMM_WORLD.rank == 0:
            from pathlib import Path
            output_file = Path("results.csv")
            if output_file.exists():
                with open(output_file, "a") as file:
                    file.write(f"{size:.5e},{MPI.COMM_WORLD.size},{np.max(elapsed_times):.5e},{np.max(runtime_changes):.5e},{np.max(runtimes_penalty):.5e}\n")
            else:
                with open(output_file, "w") as file:
                    file.write("MeshSize,NumProcs,Mixed,ChangeVar,Penalty\n")
                    file.write(f"{size:.5e},{MPI.COMM_WORLD.size},{np.max(elapsed_times):.5e},{np.max(runtime_changes):.5e},{np.max(runtimes_penalty):.5e}\n")
    if args.run_legacy:

        import dolfin
        comm_size = dolfin.MPI.comm_world.size
        rank = dolfin.MPI.comm_world.rank
        legacy_times = dolfin.MPI.comm_world.gather(run_legacy(volume_file, facet_file), root=0)
        if rank == 0:
            print(f"Legacy: {legacy_times} seconds")
            output_file = Path("results_legacy.csv")
            if output_file.exists():
                with open(output_file, "a") as file:
                    file.write(f"{size:.5e},{comm_size},{np.max(legacy_times):.5e}\n")
            else:
                with open(output_file, "w") as file:
                    file.write("MeshSize,NumProcs,ChangeVar\n")
                    file.write(f"{size:.5e},{comm_size},{np.max(legacy_times):.5e}\n")
 