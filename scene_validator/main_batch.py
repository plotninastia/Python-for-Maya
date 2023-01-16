"""
Run command for terminal:
!!! first part should be your path to mayapy.exe!!!

D:\SOFT\AutodeskMayaInstalled\Maya2020\bin\mayapy.exe C:\Users\admin\Documents\maya\2020\scripts\scene_validator\main_batch.py -p"C:\Users\admin\Desktop\testBatch" -pr "modeling" -af True

"""

import maya.standalone
import sys
import os
import maya.cmds as cmds
from argparse import ArgumentParser

# FILEPATH = 'C:/Users/admin/Desktop/testBatch'


def main():
    # create arguments
    # action - means argument comes without value, we just add it >> hello.py --sui
    parser = ArgumentParser(description="Maya scene validator")
    parser.add_argument('-pr', '--preset', type=str, default='modeling', required=True, help='Defines which preset you want to use to check maya scene')
    parser.add_argument('-af', '--auto_fix', type=bool, default='False', help='Should it fix all wrong objects?')
    parser.add_argument('-p', '--path', type=str, required=True, default='C:/Users/admin/Desktop/testBatch', help='Folder path with maya files')
    args = parser.parse_args()

    # -----------------------------------------------------

    FILEPATH = args.path
    AUTO_FIX = args.auto_fix
    PRESET = args.preset

    if not os.path.isdir(FILEPATH):
        print "ERROR"
        return

    if not os.listdir(FILEPATH):
        print "ERROR"
        return

    mayaFiles = []

    for i in os.listdir(FILEPATH):

        filename, file_extension = os.path.splitext(i)

        if file_extension == '.mb' or file_extension == '.ma':
            full_path = os.path.join(FILEPATH, i)

            mayaFiles.append(full_path)

    if not mayaFiles:
        print "ERROR"
        return

    # -----

    maya.standalone.initialize()

    result = {}

    for i in mayaFiles:
        print('Checking - {}'.format(i))

        cmds.file(i, open=1)

        packages = ['scene_validator']
        for i in sys.modules.keys()[:]:
            for package in packages:
                if i.startswith(package):
                    del (sys.modules[i])

        import scene_validator.main
        from scene_validator.main import Validator
        scene_validator.main.main(auto_fix=AUTO_FIX, mode=Validator.BATCH_MODE)

        if AUTO_FIX:
            cmds.file(save=1)

    maya.standalone.uninitialize()


if __name__ == "__main__":
    main()