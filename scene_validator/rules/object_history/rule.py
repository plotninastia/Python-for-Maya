import maya.cmds as cmds
import maya.mel as mel

class Rule(object):
    def __init__(self):
        self.rule_name = 'Object history'
        self.rule_description = 'All objects should not have any history'
        self.output = [] #if output is not empty - the Rule has not been passed

    def check(self):
        self.output = []

        inputStd = ["joint", "tweak", "skinCluster", "mesh", "displayLayer"] #we are not checking history for these objects
        shapeArray = cmds.ls(type='mesh', dag=1, l=True)
        if shapeArray:
            polyArray = list(set(cmds.listRelatives(shapeArray, p=1, type='transform', f=True)))
            for obj in polyArray:
                tmpListOfInputs = cmds.listHistory(obj, lf=1, il=1) #List objects which have inputs
                for i in tmpListOfInputs:
                    type = cmds.nodeType(i)
                    if type not in inputStd:
                        self.output.append(obj)
                        break
            return self.output

    def fix(self):
        if self.output:
            for i in self.output:
                cmds.select(i)
                mel.eval("doBakeNonDefHistory( 1, {\"prePost\" });")
                #deleting polyBindData node
                tmpListOfInputs = cmds.listHistory(i, lf=1, il=1) #List objects which have inputs
                for j in tmpListOfInputs:
                    type = cmds.nodeType(j)
                    if type == "polyBindData":
                        try:
                            cmds.delete(j)
                        except:
                            pass
        output = self.check()
        return output