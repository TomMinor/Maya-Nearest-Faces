import maya.cmds as cmds
import tom_utilities as util
from random import randint, uniform

#Set up the test scene
trunk = cmds.polyCylinder( r=1.2, h=12, sx=8, sy=8, sz=1) [0]
cmds.rotate(0, 20, 0, ws=True, r=True)

#Define the branches
branches = []

# Initial branches
branches.append(cmds.curve(bezier=True, d=1, p=[ (0, 2.509625, -1.322144), 
                                                 (0, 3.048276, -3.42778), 
                                                 (0, 4.737682, -5.337544)] ))
          
branches.append( cmds.duplicate(branches[0])[0] )
cmds.rotate(0, -135, 0, branches[1], ws=True, r=True)
cmds.move(0, -1.5, 0, branches[1], r=True)

branches.append( cmds.duplicate(branches[0])[0] )
cmds.rotate(0, 120, 0, branches[2], ws=True, r=True)
cmds.move(0, 2.4, 0, branches[2], r=True)

# Branch off another branch (I only need to place it near to an existing branch
# and the selectClosestPoints function will automatically figure out the nearest face when we extrude)
branches.append( cmds.duplicate(branches[0])[0] )
cmds.rotate(0, -45, 0, branches[3], ws=True, r=True)
cmds.move(-0.69, 0, -1.1, branches[3], r=True)


# Extrude each branch along the curve, most of the effort goes on in selectClosestPoints, which selects
# the best face to extrude from
for branch in branches:         
    # selectClosestPoints takes 2 objects (polymesh or curve) and selects the nearest points/faces
    # We only need the face we selected on the trunk, but i wanted the function to be reusable
    # so it works with pretty much any 2 polygonal object/curve
    selectedFace = util.selectClosestPoints(trunk, branch)[0] # <-- This is the new bit
    cmds.polyExtrudeFacet( "%s.f[%i]"%(trunk, selectedFace), inputCurve=branch, 
                            pvx=0.04835886825, pvy=2.25, pvz=-1.107600179, 
                            divisions=6, twist=uniform(20,40) , taper=uniform(0.05, 0.2) )
