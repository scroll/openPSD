import maya.OpenMaya as OM
import maya.OpenMayaMPx as OMMPx

pluginName = 'openPSD'
nodeId = OM.MTypeId(0x101121)


class openPSD(OMMPx.MPxNode):
    # constructor
    def __init__(self):
        OMMPx.MPxNode.__init__(self)
        print '__init__'

    def compute(self, plug, dataBlock):
        print ' compute '


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
    print 'Initializing plugin'
    mplugin = OMMPx.MFnPlugin(mobject,'Marin&Slavi', '0.1', 'Any')
    print 'Before try...'
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

