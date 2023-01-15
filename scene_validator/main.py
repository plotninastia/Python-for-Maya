"""
Run from Maya with GUI, use:

import scene_validator.main
scene_validator.main.main()

- - -

Run for terminal:
here's an example of the command
!!! first part should be your path to mayapy.exe
!!! second part should be path where you store this script
!!! -p parameter - path to your folder with maya files fot checking
!!! -pr - preset. now available: modeling, animation, test
!!! -af - auto-fix. whether to fix wrond objects

D:\SOFT\AutodeskMayaInstalled\Maya2020\bin\mayapy.exe C:\Users\admin\Documents\maya\2020\scripts\scene_validator\main_batch.py -p"C:\Users\admin\Desktop\testBatch" -pr "modeling" -af True


"""

import os
from scene_validator.gui.main_gui import ValidatorGui, create_gui
from scene_validator.core.batchMode import BatchValidator

class Validator(object):

    GUI_MODE = 0
    BATCH_MODE = 1

    def __init__(self, mode, preset, auto_fix=False):

        if mode == Validator.GUI_MODE:
            create_gui()

        elif mode == Validator.BATCH_MODE:
            batch = BatchValidator()
            batch.start(preset=preset, auto_fix=auto_fix)

def main(preset='modeling', auto_fix=False, mode=Validator.GUI_MODE):
    # v = Validator(mode=Validator.GUI_MODE)
    v = Validator(mode=mode, preset=preset, auto_fix=auto_fix)

# if __name__ == '__main__':
#     main()

