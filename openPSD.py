import maya.OpenMaya as OM
import maya.OpenMayaMPx as OMMPx

pluginName = 'openPSD'
nodeId = OM.MTypeId(0x101121)


class openPSD(OMMPx.MPxNode):
    # constructor
    def __init__(self):
        print '__init__'
        OMMPx.MPxConstraint.__init__(self)

    def compute(self, plug, dataBlock):
        print ' compute '


def nodeCreator():
        return OMMPx.asMPxPtr(openPSD())

def nodeInit():
        nAttr = OM.MFnNumericAttribute()
        uAttr = OM.MFnUnitAttribute()


# initialize the plugin
def initializePlugin(mobject):
    mplugin = OMMPx.MFnPlugin(mobject,'Marin&Slavi', '0.1', 'Any')
    try:
        mplugin.registerNode(pluginName, nodeId, nodeCreator ,nodeInit, OMMPx.MPxNode)
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

