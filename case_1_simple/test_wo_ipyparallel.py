from mesh import three_cubes
from mpi4py import MPI

def run(volume_file: str, facet_file: str) -> float:
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
    from script_festim_2 import run_festim_2_change_of_var
    import time
    MPI.COMM_WORLD.Barrier()
    start = time.perf_counter()
    run_festim_2_change_of_var(volume_file, facet_file)
    end = time.perf_counter()

    elapsed_time = end - start


    return elapsed_time

def run_penalty(volume_file: str, facet_file: str) -> float:
    from script_festim_2 import run_festim_2_penalty
    import time
    MPI.COMM_WORLD.Barrier()

    start = time.perf_counter()
    run_festim_2_penalty(volume_file, facet_file)
    end = time.perf_counter()

    elapsed_time = end - start


    return elapsed_time



size = 0.1
filename = f"meshes/mesh_{size}.msh"
if MPI.COMM_WORLD.rank == 0:
    three_cubes(filename, size=size)
MPI.COMM_WORLD.Barrier()
# +
from convert_mesh import convert_mesh

volume_file = f"meshes/mesh_{size}.xdmf"
facet_file = f"meshes/mesh_{size}_facet.xdmf"

print(filename, volume_file, facet_file)
if MPI.COMM_WORLD.rank == 0:
    nb_cells, nb_facets = convert_mesh(filename, volume_file, facet_file)
MPI.COMM_WORLD.Barrier()

# -

# +
import numpy as np



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
        