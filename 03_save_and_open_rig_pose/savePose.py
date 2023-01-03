import maya.cmds as cmds
import json

def getAllControlls():

    rig = cmds.ls(sl=1)
    #rig = 'zoma_hi_base_vanilla_rig_v6:zoma_base_rig'

    if not rig:
        cmds.error('Choose the rig')

    #p = parent
    #curves transforms
    curves = cmds.listRelatives(rig, cmds.ls(type='nurbsCurve'), p=1, f=1)

    return curves

def getPose():

    curves = getAllControlls()

    all_curves = {}

    for curve in curves:
        all_values = {}
        if cmds.listAttr(curve, keyable=1):
            keyable_channels = cmds.listAttr(curve, keyable=1)
            #channel = rotateX, rotateY, rotateZ
            for channel in keyable_channels:
                full_path = '{}.{}'.format(curve, channel)
                values = cmds.getAttr(full_path)
                all_values[channel] = values
                # print(channel, values)
            all_curves[curve] = all_values

    return all_curves


def saveToJson(path_to_file):

    json_data = getPose()
    with open(path_to_file, 'w') as outfile:
        json.dump(json_data, outfile, indent=4)


def main():
    path_to_save = cmds.fileDialog2(fileFilter="*.json", dialogStyle=2, caption="Save")[0]
    saveToJson(path_to_file=path_to_save)



if __name__ == "__main__":
    main()
