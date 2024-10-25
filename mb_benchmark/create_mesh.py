import gmsh
from pathlib import Path
import os


def save_mesh(filename):
    # Extract the directory from the filename

    directory = os.path.dirname(filename)
    # If directory doesn't exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")
    else:
        print(f"Directory '{directory}' already exists.")

    # Save the mesh
    gmsh.write(filename)
    print(f"Mesh saved to '{filename}'")


def three_cubes(filename, size=0.1):
    gmsh.initialize()

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

    try:
        # If you want to visualize the mesh
        gmsh.fltk.run()
    except:
        pass

    gmsh.finalize()


def two_cubes(filename, size=0.1):
    gmsh.initialize()

    cube1 = gmsh.model.occ.addBox(x=0, y=0, z=0, dx=1, dy=1, dz=1)
    cube2 = gmsh.model.occ.addBox(x=1, y=0, z=0, dx=1, dy=1, dz=1)

    gmsh.model.occ.synchronize()

    # Perform a Boolean union to merge the cubes and their shared surfaces
    gmsh.model.occ.fragment([(3, cube1), (3, cube2)], [])
    gmsh.model.occ.synchronize()

    # Create physical groups
    gmsh.model.addPhysicalGroup(3, [cube1], 1)
    gmsh.model.addPhysicalGroup(3, [cube2], 2)

    # Tagging the surfaces
    # Get the surfaces of each cube
    surfaces_cube1 = gmsh.model.getBoundary(
        [(3, cube1)], oriented=False, recursive=False
    )
    surfaces_cube2 = gmsh.model.getBoundary(
        [(3, cube2)], oriented=False, recursive=False
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
            2, [left_surface_cube1], 3
        )  # Tag ID 3 for left surface of cube 1

    # Tag the right surface of cube 2
    right_surface_cube2 = None
    for surface in surfaces_cube2:
        com = gmsh.model.occ.getCenterOfMass(surface[0], surface[1])
        if com[0] == 2:  # Check if this surface is at x = 2 (right side of cube 2)
            right_surface_cube2 = surface[1]
            break

    if right_surface_cube2 is not None:
        gmsh.model.addPhysicalGroup(
            2, [right_surface_cube2], 5
        )  # Tag ID 5 for right surface of cube 3

    # Tag the interface between cube1 and cube2
    interface_cube1_cube2 = []
    for surface1 in surfaces_cube1:
        for surface2 in surfaces_cube2:
            if surface1[1] == surface2[1]:  # Check if the surfaces are the same
                interface_cube1_cube2.append(surface1[1])

    if interface_cube1_cube2:
        gmsh.model.addPhysicalGroup(
            2, interface_cube1_cube2, 4
        )  # Tag ID 4 for the interface between cube1 and cube2

    # set refinement
    gmsh.model.mesh.setSize(
        gmsh.model.getEntities(0), size
    )  # Set mesh size for all points

    # Generate the mesh
    gmsh.model.mesh.generate(3)
    # Save the mesh
    save_mesh(filename)

    try:
        # If you want to visualize the mesh
        gmsh.fltk.run()
    except:
        pass

    gmsh.finalize()


def convert_mesh(filename, volume_file="mesh/mesh.xdmf", boundary_file="mesh/mf.xdmf"):
    import meshio
    import numpy as np

    # Convert mesh to XDMF
    msh = meshio.read(filename)

    # Initialize lists to store cells and their corresponding data
    triangle_cells_list = []
    tetra_cells_list = []
    triangle_data_list = []
    tetra_data_list = []

    # Extract cell data for all types
    for cell in msh.cells:
        if cell.type == "triangle":
            triangle_cells_list.append(cell.data)
        elif cell.type == "tetra":
            tetra_cells_list.append(cell.data)

    # Extract physical tags
    for key, data in msh.cell_data_dict["gmsh:physical"].items():
        if key == "triangle":
            triangle_data_list.append(data)
        elif key == "tetra":
            tetra_data_list.append(data)

    # Concatenate all tetrahedral cells and their data
    tetra_cells = np.concatenate(tetra_cells_list)
    tetra_data = np.concatenate(tetra_data_list)

    # Concatenate all triangular cells and their data
    triangle_cells = np.concatenate(triangle_cells_list)
    triangle_data = np.concatenate(triangle_data_list)

    # Create the tetrahedral mesh
    tetra_mesh = meshio.Mesh(
        points=msh.points,
        cells=[("tetra", tetra_cells)],
        cell_data={"f": [tetra_data]},
    )

    # Create the triangular mesh for the surface
    triangle_mesh = meshio.Mesh(
        points=msh.points,
        cells=[("triangle", triangle_cells)],
        cell_data={"f": [triangle_data]},
    )

    # Print unique surface and volume IDs
    print("Surface IDs: ", np.unique(triangle_data))
    print("Volume IDs: ", np.unique(tetra_data))

    # Write the mesh files
    meshio.write(volume_file, tetra_mesh)
    meshio.write(boundary_file, triangle_mesh)


if __name__ == "__main__":
    for size in [0.1, 0.07, 0.05, 0.04]:
        two_cubes(f"mesh/size_{size}/mesh.msh", size=size)
        volume_file = f"mesh/size_{size}/mesh.xdmf"
        facet_file = f"mesh/size_{size}/mf.xdmf"
        convert_mesh(
            f"mesh/size_{size}/mesh.msh",
            volume_file=volume_file,
            boundary_file=facet_file,
        )
