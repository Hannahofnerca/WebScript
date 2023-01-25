import bpy
import math
import os
import sys

# Hack to import ipr.py (see https://blender.stackexchange.com/questions/33603/importing-python-modules-and-text-files)
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
import bipr

# --- Create a simple quad --------------------------------

# a quad
v0 = [0.5, 1.0, 0.0]
v1 = [0.0, 0.0, 0.0]
v2 = [1.0, 0.3, 0.0]
v3 = [-0.5, 0.7, 0.0]

outlines = [v0, v3, v1, v2]
vertices = [v0, v1, v2, v3]
indices = [0, 1, 2, 0, 3, 1]  # triangle 1 & 2

bipr.add_line("quad_outline", outlines)
bipr.add_mesh("quad_mesh", vertices, indices)

# --------------------------------------------------------------------
# ## _Task 01:_ OBJ Triangle Writer [4 Points]
#
# Implement a function to write an OBJ file with indexed triangles.
# The function parameters are the vertices of the polygon as a list, the indices for the triangles as a list, and the name of the file as a string.
#
# A vertex in an OBJ file start with a `v` at the beginning of the line.
# A face (triangle) starts with an `f`. Make new line for every vertex and face.
# Note that indices in OBJ files start at 1.


def write_obj_file(vertices, indices, obj_file_name, print_obj=True):
    """Writes a mesh as OBJ file (outline and fill)

    Args:
        vertices (list): a list of vertices (3D coordinates)
        indices (list): a list of indices to the vertices. Indices start at 0 and are incremented by 1 before writting to the OBJ file.
        obj_file_name (str): file name of the OBJ file
    """
    with open(obj_file_name, "w") as f:
        f.write(
            "# List of vertices, with (x y z [w=1]) coordinates.\n"
        )  # comment on top of vertex list
        # Todo TASK 01: write vertices

        f.write(
            "# Polygonal face element (3 indices for a triangle) \n"
        )  # comment for face
        # Todo TASK 01: write faces (make sure indices start at 1!)

    # Debug output of the written file:
    if print_obj:
        with open(obj_file_name) as f:
            contents = f.read()
            print(contents)


write_obj_file(vertices, indices, dir+"/quad.obj")


# --------------------------------------------------------------------
## _Task 02_: Star Outline [4 Points]
#
# Implement the `create_star` function that creates a star with a defined number of points/peaks.
# Use the circle geometry as basis and use two radii to define the offset of the points (vertices at peaks and non-peaks).
# Create counter-clockwise ordered vertices of the star.
# The star is centered at the origin and extends +/- radius2 on the x and y axis.
#
# The number of points `num_peaks` for your star should be based on your birthday. Sum the digits of the day and month of your birthday. For example, if your birthday is 13.04. you should create a star with 1+3+4 = 10 points/peaks.
# Make sure, however, that the star drawing is correct for other numbers of points. If the sum is less than 5 use an arbitrary number!
#
# **Bonus:** [1 Extra-Point] make sure that a line connecting two peaks passes through the vertices on the inner circle (see slides for a visual picture). Explain the equation on a sheet of paper or in Markdown (in this file) and hand it in.


def create_star(num_peaks, r1, r2) -> list:
    """Creates a star polygon with num_peaks peaks/points.

    Args:
        num_peaks (int): number of peaks in the star
        r1 (float): radius of the inner circle
        r2 (float): radius of the outer circle

    Returns:
        list: a list of vertices (3D coordinates)
    """
    vertices = []
    # Todo TASK 02: create a star polygon with num_peaks peaks/points. Use the circle (from above) as basis.
    return vertices


r1 = 1  # inner radius
num_peaks = 5  # the digits of the day and month of your birthday summed up
r2 = 2  # outer radius [optional Bonus here!]

star = create_star(num_peaks, r1, r2)

bipr.add_line("star_outline", star)
bipr.write_obj_line_file(star, dir+"/star_outline.obj")


# --------------------------------------------------------------------
## _Task 03_: Star Mesh [4 Points]
# Reuse the vertices of the `create_star` function from the previous task and create a filled star mesh with triangles.
# Make sure that the front of the star is only made of counter-clockwise triangles.
# The triangles are defined by the indices of the vertices.
# Hint: you maybe need to add an additional vertex to close the inside of the star (inside the inner circle of radius `r1`).
# Make sure that triangles do not overlap, this causes problems for rendering.
# **Bonus:** [1 Extra-Point] Make the star 3D and not flat. For example, extrude the star mesh to create an object with depth (z!=0). For the extruded sides, you can ignore the winding-order (clockwise or counter-clockwise).


def create_star_mesh(num_peaks, r1, r2) -> tuple:
    """Creates a star mesh (triangles) with num_peaks peaks/points.

    Args:
        num_peaks (int): number of points in the star
        r1 (float): radius of the inner circle
        r2 (float): radius of the outer circle

    Returns:
        list: a list of vertices (3D coordinates)
        list: a list of indices to the vertices. Indices start at 0 and are incremented by 1 before writting to the OBJ file.
    """
    vertices = create_star(num_peaks, r1, r2)
    indices = list(range(len(vertices)))

    # Todo TASK 03: create a star mesh with vertices and triangle indices

    return (vertices, indices)


vertices, indices = create_star_mesh(num_peaks, r1, r2)

bipr.add_mesh("star_mesh", vertices, indices)
write_obj_file(vertices, indices, dir+"/star.obj")
