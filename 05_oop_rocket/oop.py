import maya.cmds as cmds

class Rocket(object):

    def __init__(self, bodyParts = 3, radius = 4, height = 8, noseConeHeight = 4, fuelTanks = 4):

        if fuelTanks<0 or fuelTanks>4:
            raise ValueError("fuel tank number should be in range from 1 to 4")

        self.bodyParts = bodyParts
        self.radius = radius
        self.height = height
        self.noseConeHeight = noseConeHeight
        self.fuelTanks = fuelTanks

    def generateBody(self):

        self.grp = cmds.group(em=True, name='Rocket')

        for i in range(self.bodyParts):
            bp = cmds.polyCylinder(n="rocket_part_" + str(i+1), r=self.radius, h=self.height)[0]
            cmds.parent(bp, self.grp)
            if i == 0:
                cmds.xform(bp, ws=1, t=[0, self.height/2 + self.height/4, 0])
            else:
                cmds.xform(bp, ws=1, t=[0, self.height/2 + self.height*i + self.height/4, 0])

    def generateCone(self):
        bp = cmds.polyCone(n="rocket_cone", r=self.radius, h=self.noseConeHeight)[0]
        self.bb_obj_name = "rocket_part_" + str(self.bodyParts)
        self.bb = cmds.xform(self.bb_obj_name, q=1, bb=1, ws=1)
        cmds.xform(bp, ws=1, t=[0, self.noseConeHeight / 2 + self.bb[4], 0])
        cmds.parent(bp, self.grp)


    def generateFuelTanks(self):
        if self.fuelTanks == 1:
            ft = cmds.polyCone(n="fuel_tank", r=self.radius/4, h=self.height/4)[0]
            cmds.xform(ft, ws=1, t=[0, self.height/8, 0])
            cmds.parent(ft, self.grp)

        elif self.fuelTanks == 2:
            ft1 = cmds.polyCone(n="fuel_tank1", r=self.radius / 4, h=self.height / 4)[0]
            ft2 = cmds.polyCone(n="fuel_tank2", r=self.radius / 4, h=self.height / 4)[0]

            cmds.xform(self.ft1, ws=1, t=[self.bb[0], self.height / 8, 0])
            cmds.xform(self.ft2, ws=1, t=[self.bb[3], self.height / 8, 0])
            cmds.parent(ft1, ft2, self.grp)

        elif self.fuelTanks == 3:
            pass

        elif self.fuelTanks == 4:
            ft1 = cmds.polyCone(n="fuel_tank1", r=self.radius / 4, h=self.height / 4)[0]
            ft2 = cmds.polyCone(n="fuel_tank2", r=self.radius / 4, h=self.height / 4)[0]
            ft3 = cmds.polyCone(n="fuel_tank3", r=self.radius / 4, h=self.height / 4)[0]
            ft4 = cmds.polyCone(n="fuel_tank4", r=self.radius / 4, h=self.height / 4)[0]

            cmds.xform(ft1, ws=1, t=[self.bb[0], self.height / 8, 0])
            cmds.xform(ft2, ws=1, t=[self.bb[3], self.height / 8, 0])
            cmds.xform(ft3, ws=1, t=[0, self.height / 8, self.bb[2]])
            cmds.xform(ft4, ws=1, t=[0, self.height / 8, self.bb[5]])

            cmds.parent(ft1, ft2, ft3, ft4, self.grp)


    def generateModel(self):
        self.generateBody()
        self.generateCone()
        self.generateFuelTanks()


class RocketNew(Rocket):
    def __init__(self,
                 bodyParts=3,
                 radius=4,
                 height=8,
                 noseConeHeight=4,
                 fuelTanks=4,
                 escapeSystem=True,
                 fins=True):

        super(RocketNew, self).__init__(bodyParts=bodyParts,
                                     radius=radius,
                                     height=height,
                                     noseConeHeight=noseConeHeight,
                                     fuelTanks=fuelTanks
                                     )
        self.generateModel()

        self.escapeSystem = escapeSystem
        self.fins = fins

        if self.escapeSystem == True:
            self.createEscapeSystem()
        if self.fins == True:
            self.createFins()


    def createFins(self):

        cube = cmds.polyCube(n="fins", w=self.height*2, h=self.height/2)[0]

        bb = cmds.xform("rocket_part_1", q=1, bb=1, ws=1)
        cy = (bb[4] - bb[1])/2 + self.height/4
        cmds.xform(cube, ws=1, t=[0, cy, 0])

        cmds.parent(cube, self.grp)

    def createEscapeSystem(self):

        cube = cmds.polyCube(n="escape_system", d=0.4, w=0.4, h=2)[0]

        bb = cmds.xform("rocket_cone", q=1, bb=1, ws=1)
        cmds.xform(cube, ws=1, t=[0, bb[4], 0])

        cmds.parent(cube, self.grp)



if cmds.objExists('Rocket'):
  cmds.delete("Rocket")


# myRocket = Rocket(bodyParts = 3, radius = 4, height = 8, noseConeHeight = 4, fuelTanks = 4)
# myRocket.generateModel()

myrocket = RocketNew(bodyParts = 3, radius = 4, height = 8, noseConeHeight = 4, fuelTanks = 4, escapeSystem=True, fins=True)