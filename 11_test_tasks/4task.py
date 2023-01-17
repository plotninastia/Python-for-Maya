"""
Task 4. Maya

There is a certain hierarchy of objects in Outliner.

The objects group called 'objects' is hidden (respectively, all objects inside too).

All locators (loc_inst_##) are located somewhere in the scene, have different coordinates, rotation, scales.

The task is to replace these locators with objects from the objects group. Objects in this group must be
randomly selected for each locator.

The replacement must occur either with copies of objects from the group (the originals remain in the hidden group),
or by the originals themselves (at the same time, the number of locators and objects must match - you will need to check this).
Note that locators can either be at the root of the Outliner or in a group.


"""

import maya.cmds as cmds
import random

objects = cmds.listRelatives('objects', f=True)
placed_objects = cmds.group(empty=1, n='placed_objects')

locators = cmds.ls(type=('locator'), l=True) or []

if not locators:
    raise Exception('there are no locators!')

if len(locators) != len(objects):
    raise Exception('the number of locators should be = the number of objects')

locators_transform = cmds.listRelatives(locators, parent=True, f=True)
random.shuffle(locators_transform)

for obj in objects:
    for loc in locators_transform:
        cmds.matchTransform(obj, loc, position=True, rotation=True, scale=True)
        cmds.showHidden(obj)
        cmds.parent(obj, placed_objects)
        locators_transform.remove(loc)
        break
