import maya.OpenMaya as om
import maya.OpenMayaMPx as ommpx
import math

pluginName = 'openPSD'
nodeId = om.MTypeId(0x101121)



class openPSD(ommpx.MPxNode):
    def __init__(self):
        ompx.MPxNode.__init__(self)

    def compute(self, plug, dataBlock):
        pass


def nodeCreator():
    return ompx.asMPxPtr(openPSD())

def nodeInit():
    nAttr = om.MFnNumericAttribute()
    mAttr = om.MFnMatrixAttribute()
    uAttr = om.MFnUnitAttribute()
    eAttr = om.MFnEnumAttribute()
    cAttr = om.MFnCompountAttribute()


# initialize the plugin
def initializePlugin(mobject):
    mplugin = ompx.MFnPlugin(mobject,'Marin&Slavi', '0.1', 'Any')
    try:
        mplugin.registerNode(pluginName, nodeId, nodeCreator ,nodeInit)

    except:
        raise Exception, 'Unable to register node: %s' %pluginName


# uninitializePlugin
def uninitializePlugin(mobject):
    mplugin = ompx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(nodeId)
    except:
        sys.stderr.write( 'Failed to deregister node: %s' %pluginName)
        raise



def computeWeight(angle, startOff, startOn, endOn, endOff, negateRange=False):
    output = 0.0

    if negateRange:
        angle *= -1.0

    if startOn <= angle <= endOn:
        output = 1.0

    elif startOff <= angle < startOn:
        output = (angle - startOff) / (startOn - startOff)

    elif endOn < angle <= endOff:
        output = (angle - endOff) / (endOn - endOff)


    return output




