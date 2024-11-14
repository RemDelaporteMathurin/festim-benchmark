import festim as F


# dolfinx.log.set_log_level(dolfinx.log.LogLevel.INFO)


def run_festim_2_nietsche(volume_file: str, facet_file: str, exports=False):
    assert hasattr(
        F, "HydrogenTransportProblem"
    ), "you should use FESTIM on the fenicsx branch"

    my_model = F.HTransportProblemDiscontinuous(
        petsc_options={
            "ksp_type": "preonly",
            "pc_type": "lu",
            "pc_factor_mat_solver_type": "mumps",
            "ksp_monitor": None,
            "ksp_error_if_not_converged": True,
            "mat_mumps_icntl_14": 120,
        }
    )
    my_model.mesh = F.MeshFromXDMF(
        volume_file=volume_file,
        facet_file=facet_file,
    )

    tungsten = F.Material(D_0=1, E_D=0, K_S_0=1, E_K_S=0)

    copper = F.Material(D_0=1, E_D=0, K_S_0=2, E_K_S=0)

    vol1 = F.VolumeSubdomain(id=1, material=tungsten)
    vol2 = F.VolumeSubdomain(id=2, material=copper)
    vol3 = F.VolumeSubdomain(id=3, material=copper)
    surface1 = F.SurfaceSubdomain(id=4)

    interface1 = F.Interface(id=6, subdomains=[vol1, vol2])
    interface2 = F.Interface(id=7, subdomains=[vol2, vol3])

    surface2 = F.SurfaceSubdomain(id=5)

    my_model.subdomains = [vol1, vol2, vol3, surface1, surface2]

    mobile = F.Species(name="H", subdomains=my_model.volume_subdomains, mobile=True)
    trapped_1 = F.Species(name="H_trapped_W", subdomains=[vol1], mobile=False)
    trapped_2 = F.Species(name="H_trapped_cu", subdomains=[vol2], mobile=False)
    empty_1 = F.ImplicitSpecies(n=0.5, others=[trapped_1])
    empty_2 = F.ImplicitSpecies(n=0.5, others=[trapped_2])

    my_model.species = [mobile, trapped_1, trapped_2]

    my_model.reactions = [
        F.Reaction(
            reactant=[mobile, empty_1],
            product=[trapped_1],
            k_0=1,
            E_k=tungsten.E_D,
            p_0=0.1,
            E_p=0.87,
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

    my_model.interfaces = [interface1, interface2]
    my_model.surface_to_volume = {
        surface1: vol1,
        surface2: vol3,
    }

    my_model.settings = F.Settings(
        atol=1e-6,
        rtol=1e-6,
        final_time=10,
        # transient=False,
    )
    my_model.settings.stepsize = F.Stepsize(1)

    if exports:
        folder = "results_festim_2/nietsche"
        my_model.exports = [
            F.VTXSpeciesExport(
                f"{folder}/mobile_{subdomain.id}.bp",
                field=mobile,
                subdomain=subdomain,
            )
            for subdomain in my_model.volume_subdomains
        ]
        my_model.exports += [
            F.VTXSpeciesExport(
                f"{folder}/trapped_{vol1.id}a.bp",
                field=trapped_1,
                subdomain=vol1,
            ),
            F.VTXSpeciesExport(
                f"{folder}/trapped_{vol2.id}.bp",
                field=trapped_2,
                subdomain=vol2,
            ),
        ]

    my_model.initialise()
    my_model.run()


def run_festim_2_penalty(volume_file: str, facet_file: str, exports=False):
    assert hasattr(
        F, "HydrogenTransportProblem"
    ), "you should use FESTIM on the fenicsx branch"

    my_model = F.HTransportProblemPenalty(
        petsc_options={
            "ksp_type": "preonly",
            "pc_type": "lu",
            "pc_factor_mat_solver_type": "mumps",
            "ksp_monitor": None,
            "ksp_error_if_not_converged": True,
            "mat_mumps_icntl_14": 120,
        }
    )
    my_model.mesh = F.MeshFromXDMF(
        volume_file=volume_file,
        facet_file=facet_file,
    )

    tungsten = F.Material(D_0=1, E_D=0, K_S_0=1, E_K_S=0)

    copper = F.Material(D_0=1, E_D=0, K_S_0=2, E_K_S=0)

    vol1 = F.VolumeSubdomain(id=1, material=tungsten)
    vol2 = F.VolumeSubdomain(id=2, material=copper)
    vol3 = F.VolumeSubdomain(id=3, material=copper)
    surface1 = F.SurfaceSubdomain(id=4)

    interface1 = F.Interface(id=6, subdomains=[vol1, vol2], penalty_term=500)
    interface2 = F.Interface(id=7, subdomains=[vol2, vol3], penalty_term=500)

    surface2 = F.SurfaceSubdomain(id=5)

    my_model.subdomains = [vol1, vol2, vol3, surface1, surface2]

    mobile = F.Species(name="H", subdomains=my_model.volume_subdomains, mobile=True)
    trapped_1 = F.Species(name="H_trapped_W", subdomains=[vol1], mobile=False)
    trapped_2 = F.Species(name="H_trapped_cu", subdomains=[vol2], mobile=False)
    empty_1 = F.ImplicitSpecies(n=0.5, others=[trapped_1])
    empty_2 = F.ImplicitSpecies(n=0.5, others=[trapped_2])

    my_model.species = [mobile, trapped_1, trapped_2]

    my_model.reactions = [
        F.Reaction(
            reactant=[mobile, empty_1],
            product=[trapped_1],
            k_0=1,
            E_k=tungsten.E_D,
            p_0=0.1,
            E_p=0.87,
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

    my_model.interfaces = [interface1, interface2]
    my_model.surface_to_volume = {
        surface1: vol1,
        surface2: vol3,
    }

    my_model.settings = F.Settings(
        atol=1e-6,
        rtol=1e-6,
        final_time=10,
        # transient=False,
    )
    my_model.settings.stepsize = F.Stepsize(1)

    if exports:
        folder = "results_festim_2/penalty"
        my_model.exports = [
            F.VTXSpeciesExport(
                f"{folder}/mobile_{subdomain.id}.bp",
                field=mobile,
                subdomain=subdomain,
            )
            for subdomain in my_model.volume_subdomains
        ]
        my_model.exports += [
            F.VTXSpeciesExport(
                f"{folder}/trapped_{vol1.id}a.bp",
                field=trapped_1,
                subdomain=vol1,
            ),
            F.VTXSpeciesExport(
                f"{folder}/trapped_{vol2.id}.bp",
                field=trapped_2,
                subdomain=vol2,
            ),
        ]

    my_model.initialise()
    my_model.run()


def run_festim_2_change_of_var(volume_file: str, facet_file: str, exports=False):
    my_model = F.HydrogenTransportProblemDiscontinuousChangeVar(
        petsc_options={
            "ksp_type": "preonly",
            "pc_type": "lu",
            "pc_factor_mat_solver_type": "mumps",
            "ksp_monitor": None,
            "ksp_error_if_not_converged": True,
            "mat_mumps_icntl_14": 120,
        }
    )
    my_model.mesh = F.MeshFromXDMF(
        volume_file=volume_file,
        facet_file=facet_file,
    )

    tungsten = F.Material(D_0=1, E_D=0, K_S_0=1, E_K_S=0)

    copper = F.Material(D_0=1, E_D=0, K_S_0=2, E_K_S=0)

    vol1 = F.VolumeSubdomain(id=1, material=tungsten)
    vol2 = F.VolumeSubdomain(id=2, material=copper)
    vol3 = F.VolumeSubdomain(id=3, material=copper)
    surface1 = F.SurfaceSubdomain(id=4)

    surface2 = F.SurfaceSubdomain(id=5)

    my_model.subdomains = [vol1, vol2, vol3, surface1, surface2]

    mobile = F.SpeciesChangeVar(
        name="H", subdomains=my_model.volume_subdomains, mobile=True
    )
    trapped_1 = F.Species(name="H_trapped_W1", subdomains=[vol1], mobile=False)
    trapped_2 = F.Species(name="H_trapped_cu", subdomains=[vol2], mobile=False)
    empty_1a = F.ImplicitSpecies(n=0.5, others=[trapped_1])
    empty_2 = F.ImplicitSpecies(n=0.5, others=[trapped_2])

    my_model.species = [mobile, trapped_1, trapped_2]

    my_model.reactions = [
        F.Reaction(
            reactant=[mobile, empty_1a],
            product=[trapped_1],
            k_0=1,
            E_k=tungsten.E_D,
            p_0=0.1,
            E_p=0.87,
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

    my_model.settings = F.Settings(
        atol=1e-6,
        rtol=1e-6,
        final_time=10,
        # transient=False,
    )
    my_model.settings.stepsize = F.Stepsize(1)

    if exports:
        folder = "results_festim_2/change_of_var"
        my_model.exports = [
            F.VTXSpeciesExport(
                f"{folder}/mobile.bp",
                field=mobile,
            ),
            F.VTXSpeciesExport(
                f"{folder}/trapped_1.bp",
                field=trapped_1,
            ),
            F.VTXSpeciesExport(
                f"{folder}/trapped_2.bp",
                field=trapped_2,
            ),
        ]

    my_model.initialise()
    my_model.run()


if __name__ == "__main__":
    from mesh import three_cubes

    size = 0.05
    filename = f"meshes/mesh_{size}.msh"

    three_cubes(filename, size=size)

    from convert_mesh import convert_mesh

    volume_file = f"meshes/mesh_{size}.xdmf"
    facet_file = f"meshes/mesh_{size}_facet.xdmf"

    print(filename, volume_file, facet_file)
    nb_cells, nb_facets = convert_mesh(filename, volume_file, facet_file)

    run_festim_2_nietsche(volume_file, facet_file, exports=True)
    run_festim_2_penalty(volume_file, facet_file, exports=True)
    run_festim_2_change_of_var(volume_file, facet_file, exports=True)
