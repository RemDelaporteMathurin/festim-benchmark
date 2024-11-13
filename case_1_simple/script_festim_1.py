import festim as F


def run_festim_1(volume_file: str, facet_file: str):
    my_model = F.Simulation()
    my_model.mesh = F.MeshFromXDMF(
        volume_file=volume_file,
        boundary_file=facet_file,
    )

    surface_1_id = 4
    surface_2_id = 5

    tungsten = F.Material(id=1, D_0=1, E_D=0, S_0=1, E_S=0)
    copper = F.Material(id=2, D_0=1, E_D=0, S_0=2, E_S=0)
    copper_bis = F.Material(id=3, D_0=1, E_D=0, S_0=2, E_S=0)

    my_model.materials = [tungsten, copper, copper_bis]

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
        F.DirichletBC(surfaces=[surface_1_id], value=2, field=0),
        F.DirichletBC(surfaces=[surface_2_id], value=0, field=0),
    ]

    my_model.settings = F.Settings(
        absolute_tolerance=1e-6,
        relative_tolerance=1e-6,
        traps_element_type="DG",  # NOTE this is to conserve discontinuity but maybe not fair to FESTIM1
        chemical_pot=True,
        transient=True,
        final_time=10,
        # transient=False,
        linear_solver="mumps",
    )

    my_model.dt = F.Stepsize(1)

    # my_model.exports = F.Exports(
    #     [
    #         F.XDMFExport("solute", folder="results_festim_1", checkpoint=True),
    #         F.XDMFExport("1", folder="results_festim_1", checkpoint=True),
    #         F.XDMFExport("2", folder="results_festim_1", checkpoint=True),
    #     ]
    # )
    # my_model.log_level = 20
    my_model.initialise()
    my_model.run()


if __name__ == "__main__":
    run_festim_1("meshes/mesh_0.05.xdmf", "meshes/mesh_0.05_facet.xdmf")
