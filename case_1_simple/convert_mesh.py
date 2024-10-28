import meshio
import numpy as np


def convert_mesh(filename, volume_file="mesh/mesh.xdmf", boundary_file="mesh/mf.xdmf"):

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
    assert False

    return len(tetra_cells), len(triangle_cells)
