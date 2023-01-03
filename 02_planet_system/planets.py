import maya.cmds as cmds
import random as random

moon_list = []
planet_position = []
planet_shader = ''


def create_planets(planet_name='earth', planet_radius_min=3, planet_radius_max=6, moon_number_min=3, moon_number_max=10, moon_radius_min=1):

    planet_radius = random.randint(planet_radius_min, planet_radius_max)

    #creating groups
    main_grp = cmds.group(empty=1, n="PlanetSystem")
    planet_grp = cmds.group(empty=1, n="Earth_geo")
    moons_grp = cmds.group(empty=1, n="Moons_geo")
    cmds.parent(planet_grp, main_grp)
    cmds.parent(moons_grp, main_grp)

    #creating planet
    planet = cmds.polySphere(n=planet_name, r=planet_radius)
    apply_material_planet(planet[0])

    global planet_position
    planet_position = cmds.xform(planet, q=1, worldSpace=1, translation=1)
    cmds.parent(planet, planet_grp)

    distance = planet_radius

    #creating moons
    moon_number = random.randint(moon_number_min, moon_number_max)
    for i in range(0, moon_number):
        moon_radius = random.randint(moon_radius_min, planet_radius) / 2
        distance += moon_radius + random.randint(1,5)
        moon = cmds.polySphere(n="moon_{}".format(i), r=moon_radius)
        moon_list.append(moon)
        apply_material_moon(moon[0])

        moon_position_grp = cmds.group(empty=1, n="moon{}_position".format(i))
        moon_rotation_grp = cmds.group(empty=1, n="moon{}_rotation".format(i))
        moon_rotation_offset_grp = cmds.group(empty=1, n="moon{}_rotation_offset".format(i))

        cmds.parent(moon, moon_position_grp)
        cmds.parent(moon_position_grp, moon_rotation_grp)
        cmds.parent(moon_rotation_grp, moon_rotation_offset_grp)
        cmds.parent(moon_rotation_offset_grp, moons_grp)

        if i > 0:
            distance += moon_radius
        cmds.xform(moon_position_grp, translation=[distance, 0, 0])
        cmds.xform(moon_rotation_grp, worldSpace=1, rotatePivot=planet_position)
        cmds.xform(moon_rotation_grp, worldSpace=1, rotation=(random.randint(-10,10), random.randint(-0,360), random.randint(-10,10)))

        distance += moon_radius

def animate_planets():
    start_time = cmds.playbackOptions(q=1, minTime=1)
    end_time = cmds.playbackOptions(q=1, maxTime=1)

    for moon in moon_list:

        moon_position_grp = cmds.listRelatives(moon, parent=True)
        moon_rotation_grp = cmds.listRelatives(moon_position_grp, parent=True)

        #own orbit
        #check the initial rotation
        moon_rotation = cmds.xform(moon_rotation_grp, q=1, worldSpace=1, rotation=1)
        #animating rotating 10 times
        cmds.xform(moon_rotation_grp, worldSpace=1, rotatePivot=planet_position)
        cmds.setKeyframe(moon_rotation_grp, time=start_time, attribute='rx', value=moon_rotation[1])
        cmds.setKeyframe(moon_rotation_grp, time=end_time, attribute='rx', value=10*(moon_rotation[1]+360))
        cmds.keyTangent(moon_rotation_grp, itt='linear', ott='linear')
        cmds.currentTime(start_time)

        #rotating around the main planet
        moon_rotation_offset_grp = cmds.listRelatives(moon_rotation_grp, parent=True)
        cmds.setKeyframe(moon_rotation_offset_grp, time=start_time, attribute='ry', value=0)
        cmds.setKeyframe(moon_rotation_offset_grp, time=end_time, attribute='ry', value=360)
        cmds.keyTangent(moon_rotation_offset_grp, itt='linear', ott='linear')

def apply_material_planet(obj):
    colors = []
    for i in range(3):
        tmp = random.uniform(0.0, 1.0)
        colors.append(tmp)

    if cmds.objExists(obj):
        shader = cmds.shadingNode('lambert', name="{}_material".format(obj), asShader=True)
        cmds.setAttr(shader + '.color', colors[0], colors[1], colors[2], type="double3")
        cmds.select(obj)
        cmds.hyperShade(assign=shader)
        global planet_shader
        planet_shader = shader

def apply_material_moon(moon):
    global planet_shader
    colors_from_planet_R = cmds.getAttr(planet_shader + '.colorR')
    colors_from_planet_G = cmds.getAttr(planet_shader + '.colorG')
    colors_from_planet_B = cmds.getAttr(planet_shader + '.colorB')
    colors_from_planet_B_moon = 0.0

    if colors_from_planet_B > 0.5:
        colors_from_planet_B_moon = colors_from_planet_B - random.uniform(0.0, colors_from_planet_B)
    else:
        colors_from_planet_B_moon = colors_from_planet_B + random.uniform(colors_from_planet_B, 1-colors_from_planet_B)

    if cmds.objExists(moon):
        shader = cmds.shadingNode('lambert', name="{}_material".format(moon), asShader=True)
        cmds.setAttr(shader + '.color', colors_from_planet_R, colors_from_planet_G, colors_from_planet_B_moon, type="double3")
        cmds.select(moon)
        cmds.hyperShade(assign=shader)

def main():

    #deletes previous version of the system
    if cmds.objExists('PlanetSystem'):
        cmds.delete('PlanetSystem')

        mat = cmds.ls(materials=1)
        for i in mat:
            print(i)
            if i.startswith('moon') or i.startswith('earth'):
                cmds.delete(i)

    #planet_name, planet_radius_min, planet_radius_max, moon_number_min, moon_number_max, moon_radius_min
    create_planets('earth', 3, 10, 5, 10, 1)
    animate_planets()

main()