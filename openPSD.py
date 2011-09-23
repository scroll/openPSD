import maya.OpenMaya as OM
import maya.OpenMayaMPx as OMMPx

pluginName = 'openPSD'
nodeId = OM.MTypeId(0x101121)


class openPSD(OMMPx.MPxNode):
    # constructor
    def __init__(self):
        OMMPx.MPxNode.__init__(self)

    def compute(self, plug, dataBlock):
        pass


def nodeCreator():
    return OMMPx.asMPxPtr(openPSD())

def nodeInit():
    nAttr = OM.MFnNumericAttribute()
    openPSD.aTest = nAttr.create( "test", "tst" ,OM.MFnNumericData.kFloat)
    nAttr.setDefault(0.5)
    nAttr.setKeyable(True)
    openPSD.addAttribute(openPSD.aTest)


# initialize the plugin
def initializePlugin(mobject):
    mplugin = OMMPx.MFnPlugin(mobject,'Marin&Slavi', '0.1', 'Any')
    try:
        mplugin.registerNode(pluginName, nodeId, nodeCreator ,nodeInit)

    except:
        raise Exception, 'Unable to register node: %s' %pluginName


# uninitializePlugin
def uninitializePlugin(mobject):
    mplugin = OMMPx.MFnPlugin(mobject)
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




