from sys import maxint
import maya.cmds as cmds

def selectClosestPoints(a, b):
    ''' Selects the 2 faces/points on a polygonal/curve object that are the least distant from each other
        a : First name of a polygonal/curve object
        b : Second name of a polygonal/curve object
        Returns a tuple of the 2 selected point/face indices, (a,b)
    '''
    # There's no point trying to find the closest face between the same object
    if(a == b):
        return

    # We can't be sure what type of objects a or b are yet, so assume they are both curves
    # .cp is used to query for a curves point coordinate
    # .f is used to query for a poly object's face coordinate
    aType = bType = 'cp'

    ''' This is a dodgy way of checking if we're working with a curve or poly mesh
        I couldn't find a (working) method of checking an objects type, so feel free
        to modify this if you figure out something like cmds.objType(a) == 'polyMesh'
    '''
    # Assume the object is a curve and attempt to retrieve it's point coordinates,
    # if this fails assume it is a polygonal object and retrieve its face center positions
    try:
        objA = getCurvePoints(a)
    except:
        aType = 'f'
        objA = getFaceCenter(a)

    try:
        objB = getCurvePoints(b)
    except:
        aType = 'f'
        objB = getFaceCenter(b)

    maxDistance = maxint
    nearestPointAindex = nearestPointBindex = None

    # Simply check every face in the 1st object against every face in the 2nd object
    # and update maxDistance if they are closer than it's previous value
    for indexA, pointA in enumerate(objA):
        for indexB, pointB in enumerate(objB):
            distance = sqrmagnitude(pointA, pointB)
            if distance < maxDistance:
                nearestPointAindex = indexA
                nearestPointBindex = indexB
                maxDistance = distance

    # Select the 2 closest faces
    if None != [nearestPointAindex, nearestPointBindex]:
        cmds.select( "%s.%s[%i]"%(a, aType, nearestPointAindex),
                     "%s.%s[%i]"%(b, bType, nearestPointBindex) )

    return nearestPointAindex, nearestPointBindex


def drawLine(a, b):
    cmds.curve( p=[a, b], d = 1 )

#import math
#def magnitude(a, b):
#    return math.sqrt( (a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2 )

# Square roots are expensive, so we can normally make do with
# checking the squared distance instead
def sqrmagnitude(a, b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2

def getCurvePoints(name):
    curveIndices = cmds.getAttr('%s.cp'%name, s=1)
    return [cmds.xform('%s.cv[%s]'%(name,i), ws=True, q=True, t=True) for i in range(curveIndices)]

def getFaceCenter(name, makeLocators=False):
    ''' Calculates the center of each face and returns a list of [x,y,z]
        name : Object name
        makeLocators : If set to True, generate locators for each vertex position and face center
    '''
    faceIndices = cmds.polyEvaluate(name, f=True)
    # Store (x,y,z) lists for each face's centre
    faceCenters = []
    mesh = [cmds.xform('%s.f[%s]'%(name,i), ws=True, q=True, t=True) for i in range(faceIndices)]

    for face in mesh:
        centrePos = [0,0,0]
        vertexCount = len(face)

        for vertex in xrange(0, vertexCount, 3):
            pos = face[vertex : vertex+3]
            centrePos[0] += pos[0]
            centrePos[1] += pos[1]
            centrePos[2] += pos[2]

            if makeLocators:
                cmds.spaceLocator(p=pos)
                cmds.CenterPivot()
                cmds.scale(0.1,0.1,0.1)

        # Find the face center by dividing by the number of vertices
        centrePos = map(lambda x: x / (vertexCount/3), centrePos)

        faceCenters.append(centrePos)

        if makeLocators:
            avgLocator = cmds.spaceLocator(p=centrePos)[0]
            cmds.CenterPivot()
            cmds.scale(0.05, 0.05, 0.05)
            # Set the face average locator to a red colour
            cmds.setAttr("%s.overrideEnabled" % avgLocator, 1)
            cmds.setAttr("%s.overrideColor" % avgLocator, 13)

    return faceCenters