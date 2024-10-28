import gmsh
from pathlib import Path
from convert_mesh import convert_mesh


def three_cubes(filename, size=0.1):
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 1)

    cube1 = gmsh.model.occ.addBox(x=0, y=0, z=0, dx=1, dy=1, dz=1)
    cube2 = gmsh.model.occ.addBox(x=1, y=0, z=0, dx=1, dy=1, dz=1)
    cube3 = gmsh.model.occ.addBox(x=2, y=0, z=0, dx=1, dy=1, dz=1)

    gmsh.model.occ.synchronize()

    # Perform a Boolean union to merge the cubes and their shared surfaces
    gmsh.model.occ.fragment([(3, cube1), (3, cube2), (3, cube3)], [])
    gmsh.model.occ.synchronize()

    # Create physical groups
    gmsh.model.addPhysicalGroup(3, [cube1], 1)
    gmsh.model.addPhysicalGroup(3, [cube2], 2)
    gmsh.model.addPhysicalGroup(3, [cube3], 3)

    # Tagging the surfaces
    # Get the surfaces of each cube
    surfaces_cube1 = gmsh.model.getBoundary(
        [(3, cube1)], oriented=False, recursive=False
    )
    surfaces_cube2 = gmsh.model.getBoundary(
        [(3, cube2)], oriented=False, recursive=False
    )
    surfaces_cube3 = gmsh.model.getBoundary(
        [(3, cube3)], oriented=False, recursive=False
    )

    # Tag the left surface of cube 1
    left_surface_cube1 = None
    for surface in surfaces_cube1:
        com = gmsh.model.occ.getCenterOfMass(surface[0], surface[1])
        if com[0] == 0:  # Check if this surface is at x = 0
            left_surface_cube1 = surface[1]
            break

    if left_surface_cube1 is not None:
        gmsh.model.addPhysicalGroup(
            2, [left_surface_cube1], 4
        )  # Tag ID 4 for left surface of cube 1

    # Tag the right surface of cube 3
    right_surface_cube3 = None
    for surface in surfaces_cube3:
        com = gmsh.model.occ.getCenterOfMass(surface[0], surface[1])
        if com[0] == 3:  # Check if this surface is at x = 3 (right side of cube 3)
            right_surface_cube3 = surface[1]
            break

    if right_surface_cube3 is not None:
        gmsh.model.addPhysicalGroup(
            2, [right_surface_cube3], 5
        )  # Tag ID 5 for right surface of cube 3

    # Tag the interface between cube1 and cube2
    interface_cube1_cube2 = []
    for surface1 in surfaces_cube1:
        for surface2 in surfaces_cube2:
            if surface1[1] == surface2[1]:  # Check if the surfaces are the same
                interface_cube1_cube2.append(surface1[1])

    if interface_cube1_cube2:
        gmsh.model.addPhysicalGroup(
            2, interface_cube1_cube2, 6
        )  # Tag ID 6 for the interface between cube1 and cube2

    # Tag the interface between cube2 and cube3
    interface_cube2_cube3 = []
    for surface2 in surfaces_cube2:
        for surface3 in surfaces_cube3:
            if surface2[1] == surface3[1]:  # Check if the surfaces are the same
                interface_cube2_cube3.append(surface2[1])

    if interface_cube2_cube3:
        gmsh.model.addPhysicalGroup(
            2, interface_cube2_cube3, 7
        )  # Tag ID 7 for the interface between cube2 and cube3

    # set refinement
    gmsh.model.mesh.setSize(
        gmsh.model.getEntities(0), size
    )  # Set mesh size for all points

    # Generate the mesh
    gmsh.model.mesh.generate(3)

    # Save the mesh
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    gmsh.write(filename)
    print(f"Mesh saved to '{filename}'")

    # try:
    #     # If you want to visualize the mesh
    #     gmsh.fltk.run()
    # except:
    #     pass

    gmsh.finalize()
