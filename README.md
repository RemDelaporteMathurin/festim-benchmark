# festim-benchmark
Benchmark repo for HPC fusion conference

## Spack installation
For spack
```bash
. ./spack/share/spack/setup-env.sh
spack env create fenicsx-env-main
spack env activate fenicsx-env-main
spack add py-pip py-h5py py-scipy gmsh+opencascade py-meshio py-ipyparallel sympy py-numpy==1.26.4
spack add py-fenics-dolfinx@main fenics-dolfinx+adios2 py-tqdm ^petsc+mumps cflags="-O3" fflags="-O3"
spack install
```
From config
```
- py-pip
- py-h5py
- py-scipy
- gmsh
- py-fenics-dolfinx ^petsc cflags=-O3 fflags=-O3 +mumps
- gmsh+opencascade
- py-meshio
- py-ipyparallel
- py-sympy py-numpy==1.26.4
- fenics-dolfinx+adios2
- py-tqdm
```