import maya.cmds as cmds


def PolyCreate(*args):

    #name
    polyName = cmds.textField("objName", q=1, text=1)


    #radio buttons

    #sphere
    rb1 = cmds.radioButton("rb1", q=1, select=1)
    #cube
    rb2 = cmds.radioButton("rb2", q=1, select=1)
    #cone
    rb3 = cmds.radioButton("rb3", q=1, select=1)

    obj = None

    if rb1:
        obj = cmds.polySphere(name=polyName)[0]
    elif rb2:
        obj = cmds.polyCube(name=polyName)[0]
    else:
        obj = cmds.polyCone(name=polyName)[0]

    #checkboxes

    chb_grp = cmds.checkBox("grpCheckBox", q=1, value=1)
    chb_move = cmds.checkBox("moveCheckBox", q=1, value=1)
    chb_display = cmds.checkBox("displayLayerCheckBox", q=1, value=1)

    if chb_grp:
        grp = cmds.group(em=True, name=polyName+'_grp')
        cmds.parent(obj, grp)

    if chb_move:
        cmds.xform(obj, translation=[0, 10, 0])

    if chb_display:
        dl = cmds.createDisplayLayer(name=polyName+'_layer')
        cmds.editDisplayLayerMembers(dl, obj)



def main():

    if cmds.window("PolyCreator", exists=1):
        cmds.deleteUI("PolyCreator")

    if cmds.windowPref("PolyCreator", exists=1):
        cmds.windowPref("PolyCreator", remove=1)

    cmds.window("PolyCreator", title="Poly Creator", width=245, height=170, tlb=1, sizeable=0)

    mainLayout = cmds.columnLayout(rowSpacing=10, columnOffset=["both", 5])

    # ----------------------------

    nameLayout = cmds.columnLayout(adjustableColumn=1,
                                   columnAlign="left",
                                   columnOffset=["both", 10],
                                   rowSpacing=10,
                                   parent=mainLayout
                                   )

    objNameField = cmds.textField("objName", placeholderText="Object name", parent=nameLayout)

    # ----------------------------

    rowLayout = cmds.rowLayout(numberOfColumns=3,
                               columnWidth3=(80, 80, 80),
                               columnAlign=(1, 'both'),
                               columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])

    radioCollection = cmds.radioCollection()
    rb1 = cmds.radioButton("rb1", label="Sphere")
    rb2 = cmds.radioButton("rb2", label="Cube")
    rb3 = cmds.radioButton("rb3", label="Cone")
    cmds.radioCollection(radioCollection, e=1, select=rb1)

    # ----------------------------

    checkboxesLayout = cmds.columnLayout(adjustableColumn=1,
                                   columnAlign="left",
                                   columnOffset=["both", 12],
                                   rowSpacing=5,
                                   parent=mainLayout
                                   )
    grpCheckBox = cmds.checkBox("grpCheckBox", label="Put into a group")
    moveCheckBox = cmds.checkBox("moveCheckBox", label="Move up by 10 uni")
    displayLayerCheckBox = cmds.checkBox("displayLayerCheckBox", label="Display Layer / Template")

    #----------------------------

    buttonLayout = cmds.rowLayout(numberOfColumns=2,
                               columnWidth2=(130, 130),
                               columnAttach=[(1, 'both', 0), (2, 'both', 0)], parent=mainLayout)

    cmds.button(label='Create', parent=buttonLayout, command=PolyCreate)
    cmds.button(label='Cancel', parent=buttonLayout, command="cmds.deleteUI(\"PolyCreator\")")




    cmds.showWindow("PolyCreator")

main()