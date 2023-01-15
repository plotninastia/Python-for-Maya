This is a project from Master Class!!!

---

The scripts go through objects in a scene/scenes, validates them and can fix object which have not passed the validation.

It can work in a GUI mode from Maya or from command line (batch mode).

---
Put the folder 'scene_validator' to C:\Users\admin\Documents\maya\2020\scripts or wherever you store your Maya scripts.

To run from Maya with GUI, use this code in Python tab:

import scene_validator.main
scene_validator.main.main()

- - -

To run for terminal:

here's an example of the command

!!! first part should be your path to mayapy.exe

!!! second part should be path where you store this script

!!! -p parameter - path to your folder with maya files fot checking

!!! -pr - preset. now available: modeling, animation, test

!!! -af - auto-fix. whether to fix wrond objects

D:\SOFT\AutodeskMayaInstalled\Maya2020\bin\mayapy.exe C:\Users\admin\Documents\maya\2020\scripts\scene_validator\main_batch.py -p"C:\Users\admin\Desktop\testBatch" -pr "modeling" -af True


