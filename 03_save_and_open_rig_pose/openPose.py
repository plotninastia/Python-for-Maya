import maya.cmds as cmds
import json


def openFromJson(path_to_file='C:/Users/admin/Desktop/savedpose.json'):
    with open(path_to_file, 'r') as read_file:
        json_data = json.load(read_file)

    return json_data


def setPose(json_data):

    pose = json_data


    for curve_name, attributes_and_values in pose.items():
        for attributes, value in attributes_and_values.items():
            curve_and_attribute = str(curve_name) + '.' + str(attributes)
            cmds.setAttr(curve_and_attribute, value)


def main():
    path_to_open = cmds.fileDialog2(fileFilter="*.json", dialogStyle=2, fileMode=1, caption="Open Pose", okCaption="Open")[0]
    setPose(openFromJson(path_to_file=path_to_open))


if __name__ == "__main__":
    main()
