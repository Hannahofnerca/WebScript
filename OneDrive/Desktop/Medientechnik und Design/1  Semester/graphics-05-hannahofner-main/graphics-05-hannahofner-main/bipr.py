""" Blender utilities for IPR. 

This module contains utilities functions for Blender scripting as used in the IPR course at the FH Hagenberg.
"""
import bpy
import math
from typing import Optional


def add_mesh(
    name: str,
    vertices: list,
    faces: list,
    normals: Optional[list] = None,
    remove_existing: bool = True,
):
    """Adds a mesh to the scene.

    Args:
        name (str): Name of the mesh.
        vertices (list): List of vertices.
        faces (list): List of triangle indices.
        normals (list, optional): List of normals. Defaults to None.
        remove_existing (bool, optional): Remove existing mesh with the same name. Defaults to True.
    """
    # Create the mesh
    mesh = _create_empty_mesh(name, remove_existing)

    # make sure face's len is a multiple of 3
    assert len(faces) % 3 == 0
    # Create the face triplets by extracting consecutive triplets from the list of indices
    _faces = [faces[i : i + 3] for i in range(0, len(faces), 3)]

    # Add the vertices to the mesh
    mesh.from_pydata(vertices, [], _faces)

    # Update the mesh to reflect the changes
    mesh.update()

    # Validate the mesh
    mesh.validate(verbose=True, clean_customdata=False)

    # Add the normals to the mesh
    if normals:
        assert len(normals) == len(vertices)

        mesh.use_auto_smooth = True
        mesh.normals_split_custom_set_from_vertices(normals)

    # Update the mesh to reflect the changes
    mesh.update()


def add_line(name: str, outline: list, remove_existing: bool = True):
    """Adds a line to the scene.

    Args:
        name (str): Name of the line.
        outline (list): List of 3D vertices. For example: [[0, 0, 0], [1, 0, 0], [1, 1, 0]].
        remove_existing (bool, optional): Remove existing mesh with the same name. Defaults to True.
    """
    # Create the mesh
    mesh = _create_empty_mesh(name, remove_existing)
    
    if len(outline)<2:
        print("ERROR: add_line needs at least 2 vertices!")
        return

    # generate a list of edges
    edges = []
    for i in range(len(outline) - 1):
        edges.append([i, i + 1])
    # close the loop
    edges.append([len(outline) - 1, 0])

    # Add the vertices to the mesh
    mesh.from_pydata(outline, edges, [])

    # Update the mesh to reflect the changes
    mesh.update()


def _create_empty_mesh(name: str, remove_existing: bool = True):
    """Creates an empty mesh with the given name.

    Args:
        name (str): Name of the object.
        remove_existing (bool, optional): Remove existing object with the same name. Defaults to True.

    Returns:
        bpy.types.Object: The mesh.
    """

    # check if the mesh already exists
    if remove_existing and name in bpy.data.meshes:
        # remove the mesh
        bpy.data.meshes.remove(bpy.data.meshes[name])

    # Create the mesh
    mesh = bpy.data.meshes.new(name)

    # Create an object for the mesh
    obj = bpy.data.objects.new(name, mesh)

    # Add the object to the scene
    bpy.context.collection.objects.link(obj)

    return mesh


def create_icosahedron(subdivisions: int = 0, size: float = 1) -> tuple:
    """Creates an icosahedron and returns the vertices and triangle faces.

    # Example usage: `vertices, faces = create_icosahedron()`

    Args:
        subdivisions (int, optional): Number of subdivisions. Defaults to 0.
        size (float, optional): Radius of the icosahedron. Defaults to 1.

    Returns:
        tuple: A tuple containing the vertices and triangle faces.
    """
    # Create an icosahedron with the given subdivision
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=subdivisions, radius=size, location=(0, 0, 0)
    )

    # Get the newly created icosahedron object
    icosahedron = bpy.context.object

    # Access the mesh data of the icosahedron
    mesh = icosahedron.data

    # Get the vertices and faces of the icosahedron as a list
    vertices = [vertex.co for vertex in mesh.vertices]
    faces = [face.vertices for face in mesh.polygons]

    # flatten the faces list
    faces = [item for sublist in faces for item in sublist]

    # Delete the icosahedron again
    bpy.data.objects.remove(icosahedron)

    return vertices, faces


def write_obj_line_file(vertices: list, obj_file_name: str, print_obj: bool = True):
    """Write a polygon as OBJ line file.

    The polygon can have varying numbers of vertices (e.g., triangle, quad, ...).
    Only an outline is stored in the OBJ file.
    The file can be imported into Blender, Maya, or any other 3D modeling software.

    Args:
        vertices (list): a list of vertices (3D coordinates)
        obj_file_name (str): file name of the OBJ file
        print_obj (bool): if True, prints the OBJ file to the console. Defaults to True.
    """
    indices = list(range(1, len(vertices) + 1))  # indices start at 1
    indices.append(1)  # close the polygon by connecting the last with the first vertex

    with open(obj_file_name, "w") as f:
        f.write(
            "# List of vertices, with (x y z [w=1]) coordinates.\n"
        )  # comment on top of vertex list
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")  # write vertex

        # line
        f.write("# Line element (indices to vertices)\n")  # comment for line
        f.write("l " + " ".join(map(str, indices)) + "\n")

    # Debug output of the written file:
    if print_obj:
        with open(obj_file_name) as f:
            contents = f.read()
            print(contents)
