# festim-benchmark
Benchmark repo for HPC fusion conference

## Spack installation
For spack
```bash
. ./spack/share/spack/setup-env.sh
spack env create fenicsx-env-main
spack env activate fenicsx-env-main
spack add py-pip py-h5py py-scipy gmsh+opencascade py-meshio py-ipyparallel py-sympy py-numpy==1.26.4 py-pandas
spack add py-fenics-dolfinx@main fenics-dolfinx+adios2 py-tqdm ^petsc+mumps cflags="-O3" fflags="-O3"
spack install
```


Legacy
```bash
. ./spack/share/spack/setup-env.sh
spack env create legacy-env-main
spack env activate legacy-env-main
spack add py-pip py-h5py py-scipy py-gmsh gmsh+opencascade py-meshio py-ipyparallel py-sympy py-nump@1.26.4 petsc+mumps  py-tqdm py-pandas fenics@2019.1.0.post0 ^boost@1.84.0 cflags="-O3" fflags="-O3"
spack install
```