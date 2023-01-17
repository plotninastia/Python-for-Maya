"""
Task 5. Maya

There is some geometric surface in the scene.

Write a script which will position other selected objects (spheres or locators, etc)
on the surface of the current object at random positions.

If objects, when placed on the surface, intersect with the surface, this is ok.

"""

import maya.cmds as cmds
import random


def get_vertex_positions(surface):
    output_all_positions = []

    vertexes = cmds.getAttr(surface + ".vrts", multiIndices=True)

    for i in vertexes:
        vtx_name = str(surface) + ".pnts[" + str(i) + "]"
        vert_position = cmds.xform(vtx_name, q=True, translation=True, worldSpace=True)
        output_all_positions.append(vert_position)

    return output_all_positions


def place_obj(surf):
    positions = get_vertex_positions(surf)
    objects = cmds.ls(sl=True, l=True)

    for obj in objects:
        pos = random.choice(positions)
        cmds.xform(obj, translation=pos, worldSpace=True)
        positions.remove(pos)


def main():
    surface = 'surface'
    place_obj(surface)


if __name__ == '__main__':
    main()

