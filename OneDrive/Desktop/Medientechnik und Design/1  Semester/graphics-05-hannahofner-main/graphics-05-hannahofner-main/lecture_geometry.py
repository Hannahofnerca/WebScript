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

# outline: store 4 vertices in a list:
outlines = [v0, v3, v1, v2]

bipr.add_line("quad_outline", outlines)

# mesh: store 4 indices in a list:
vertices = [v0, v1, v2, v3]
indices = [0, 1, 2, 0, 3, 1]  # triangle 1 & 2

bipr.add_mesh("quad_mesh", vertices, indices)

# stop the script here for now. Remove later!!!
assert False

# --- Create a circle -------------------------------------

radius = 1
num_vertices = 20
alpha = 2 * math.pi / num_vertices

circle = []
for i in range(num_vertices):
    x, y = math.cos(alpha * i), math.sin(alpha * i)
    circle.append([x * radius, y * radius, 0])

bipr.add_line("circle_outline", circle)


# --- Writing OBJ (line) files ----------------------------


def write_obj_line_file(vertices, obj_file_name, print_obj=True):
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


# write the quad outline
write_obj_line_file(outlines, dir + "/quad_outline.obj")

# write the circle outline
write_obj_line_file(circle, dir + "/circle_outline.obj")
