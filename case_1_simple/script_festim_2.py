import festim as F


# dolfinx.log.set_log_level(dolfinx.log.LogLevel.INFO)


def run_festim_2(volume_file: str, facet_file: str):
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

    # my_model.exports = [
    #     F.VTXSpeciesExport(
    #         f"results_festim_2/mobile_{subdomain.id}.bp",
    #         field=mobile,
    #         subdomain=subdomain,
    #     )
    #     for subdomain in my_model.volume_subdomains
    # ]
    # [
    #     F.VTXSpeciesExport(
    #         f"results_festim_2/trapped_{vol1.id}a.bp",
    #         field=trapped_1a,
    #         subdomain=vol1,
    #     ),
    #     F.VTXSpeciesExport(
    #         f"results_festim_2/trapped_{vol1.id}b.bp",
    #         field=trapped_1b,
    #         subdomain=vol1,
    #     ),
    #     F.VTXSpeciesExport(
    #         f"results_festim_2/trapped_{vol2.id}.bp",
    #         field=trapped_2,
    #         subdomain=vol2,
    #     ),
    # ]

    my_model.initialise()
    my_model.run()


def run_festim_2_penalty(volume_file: str, facet_file: str):
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

    interface1 = F.Interface(id=6, subdomains=[vol1, vol2])
    interface2 = F.Interface(id=7, subdomains=[vol2, vol3])

    surface2 = F.SurfaceSubdomain(id=5)

    my_model.subdomains = [vol1, vol2, vol3, surface1, surface2]

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

    # my_model.exports = [
    #     F.VTXSpeciesExport(
    #         f"results_festim_2/mobile_{subdomain.id}.bp",
    #         field=mobile,
    #         subdomain=subdomain,
    #     )
    #     for subdomain in my_model.volume_subdomains
    # ]
    # [
    #     F.VTXSpeciesExport(
    #         f"results_festim_2/trapped_{vol1.id}a.bp",
    #         field=trapped_1a,
    #         subdomain=vol1,
    #     ),
    #     F.VTXSpeciesExport(
    #         f"results_festim_2/trapped_{vol1.id}b.bp",
    #         field=trapped_1b,
    #         subdomain=vol1,
    #     ),
    #     F.VTXSpeciesExport(
    #         f"results_festim_2/trapped_{vol2.id}.bp",
    #         field=trapped_2,
    #         subdomain=vol2,
    #     ),
    # ]

    my_model.initialise()
    my_model.run()


def run_festim_2_change_of_var(volume_file: str, facet_file: str):
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

    my_model.settings = F.Settings(
        atol=1e-6,
        rtol=1e-6,
        final_time=10,
        # transient=False,
    )
    my_model.settings.stepsize = F.Stepsize(1)

    # my_model.exports = [
    #     F.VTXSpeciesExport(
    #         f"results_festim_2/mobile_{subdomain.id}.bp", field=mobile, subdomain=subdomain
    #     )
    #     for subdomain in my_model.volume_subdomains
    # ]
    # [
    #     F.VTXSpeciesExport(
    #         f"results_festim_2/trapped_{vol1.id}a.bp",
    #         field=trapped_1a,
    #         subdomain=vol1,
    #     ),
    #     F.VTXSpeciesExport(
    #         f"results_festim_2/trapped_{vol1.id}b.bp",
    #         field=trapped_1b,
    #         subdomain=vol1,
    #     ),
    #     F.VTXSpeciesExport(
    #         f"results_festim_2/trapped_{vol2.id}.bp",
    #         field=trapped_2,
    #         subdomain=vol2,
    #     ),
    # ]

    my_model.initialise()
    my_model.run()
