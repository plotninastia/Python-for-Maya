import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds

selectedMesh = cmds.ls(sl=1,l=1)[0]
cmds.hide(selectedMesh)
selectionList = OpenMaya.MSelectionList()
selectionList.add(selectedMesh)

mDagPath = selectionList.getDagPath(0)

edgeIterator = OpenMaya.MItMeshEdge(mDagPath)

grp = cmds.group(em=True, name='obj_processed')

while not edgeIterator.isDone():

    w_pos_egVert0 = edgeIterator.point(0, OpenMaya.MSpace.kWorld)
    w_pos_egVert1 = edgeIterator.point(1, OpenMaya.MSpace.kWorld)

    curve = cmds.curve(d=1, p=[(w_pos_egVert0[0], w_pos_egVert0[1], w_pos_egVert0[2]), (w_pos_egVert1[0], w_pos_egVert1[1], w_pos_egVert1[2])])

    #direction - returns the direction (tangent) of the curve, which are normals for the circle
    #eg: 0, 1, 0 = y
    direction = cmds.pointOnCurve(curve, p=0, normalizedTangent=1)

    circle = cmds.circle(r=0.09, nr=(direction[0], direction[1], direction[2]), d=3, s=8)[0]
    cmds.xform(circle, t=(w_pos_egVert0[0], w_pos_egVert0[1], w_pos_egVert0[2]), ws=1)

    extrusion = cmds.extrude(circle, curve, rn=0, po=1, et=2, ucp=0, fpt=1, upn=1, rotation=0, scale=1, rsp=1, ch=0)[0]

    cmds.delete(curve)
    cmds.delete(circle)
    cmds.parent(extrusion, grp)

    edgeIterator.next()

