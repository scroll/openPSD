import maya.OpenMaya as OM
import maya.OpenMayaMPx as OMMPx
import math

pluginName = 'openPSD'
nodeId = OM.MTypeId(0x101121)



class openPSD(OMMPx.MPxNode):
    def __init__(self):
        OMMPx.MPxNode.__init__(self)

    def compute(self, plug, dataBlock):
        if plug != openPSD.outAngle_uAttr and plug != openPSD.outTargetWeights_nAttr :
            return OM.kUnknownParameter


        baseMatrix_DH = OM.MDataHandle()
        baseMatrix_DH = dataBlock.inputValue(openPSD.baseMatrix_mAttr)
	base_M = baseMatrix_DH.asMatrix()

        driverMatrix_DH = OM.MDataHandle()
	driverMatrix_DH = dataBlock.inputValue(openPSD.driverMatrix_mAttr)
	driver_M = driverMatrix_DH.asMatrix()

        
	baseAxisX_DH = OM.MDataHandle()
        baseAxisX_DH = data.inputValue(openPSD.baseAxisX_nAttr)

	
	MDataHandle baseAxisY_DH = data.inputValue(baseAxisY_nAttr)
	
	MDataHandle baseAxisZ_DH = data.inputValue(baseAxisZ_nAttr)

	
	MVector baseAxis_V(baseAxisX_DH.asDouble(), baseAxisY_DH.asDouble(), baseAxisZ_DH.asDouble())
	
	MDataHandle frontAxisX_DH = data.inputValue(frontAxisX_nAttr)

	
	MDataHandle frontAxisY_DH = data.inputValue(frontAxisY_nAttr)

	
	MDataHandle frontAxisZ_DH = data.inputValue(frontAxisZ_nAttr)

	
	MVector frontAxis_V = OM.MVector((frontAxisX_DH.asDouble(), frontAxisY_DH.asDouble(), frontAxisZ_DH.asDouble()))


def nodeCreator():
    return OMMPx.asMPxPtr(openPSD())

def nodeInit():
    nAttr = OM.MFnNumericAttribute()
    mAttr = OM.MFnMatrixAttribute()
    uAttr = OM.MFnUnitAttribute()
    eAttr = OM.MFnEnumAttribute()
    cAttr = OM.MFnCompountAttribute()

    # baseMatrix_mAttr
    openPSD.baseMatrix_mAttr = mAttr.create("baseMatrix", "bm", OM.MFnMatrixAttribute.kDouble)
    openPSD.addAttribute(openPSD.baseMatrix_mAttr)


    # driverMatrix_mAttr
    openPSD.driverMatrix_mAttr = mAttr.create("driverMatrix", "dm", OM.MFnMatrixAttribute.kDouble)
    openPSD.addAttribute(openPSD.driverMatrix_mAttr)

    # baseAxisX
    openPSD.baseAxisX_nAttr = nAttr.create("baseAxisX", "hax", OM.MFnNumericData.kDouble, 0.0)
    nAttr.setKeyable(True)
    openPSD.addAttribute(openPSD.baseAxisX_nAttr)

    # baseAxisY
    openPSD.baseAxisY_nAttr = nAttr.create("baseAxisY", "hay", OM.MFnNumericData.kDouble, 0.0)
    nAttr.setKeyable(True)
    openPSD.addAttribute(openPSD.baseAxisY_nAttr)

    # baseAxisZ
    openPSD.baseAxisZ_nAttr = nAttr.create("baseAxisZ", "haz", OM.MFnNumericData.kDouble, 0.0)
    nAttr.setKeyable(True)
    openPSD.addAttribute(openPSD.baseAxisZ_nAttr)

    # baseAxis
    openPSD.baseAxis_nAttr = nAttr.create("baseAxis", "ha", baseAxisX_nAttr, baseAxisY_nAttr, baseAxisZ_nAttr)
    nAttr.setDefault(1.0, 0.0, 0.0)
    openPSD.addAttribute(openPSD.baseAxis_nAttr)

    # frontAxisX
    openPSD.frontAxisX_nAttr = nAttr.create("frontAxisX", "fax", OM.MFnNumericData.kDouble, 0.0)
    nAttr.setKeyable(True)
    openPSD.addAttribute(openPSD.frontAxisX_nAttr)

    # frontAxisY
    openPSD.frontAxisY_nAttr = nAttr.create("frontAxisY", "fay", OM.MFnNumericData.kDouble, 0.0)
    nAttr.setKeyable(True)
    openPSD.addAttribute(openPSD.frontAxisY_nAttr)

    # frontAxisZ
    openPSD.frontAxisZ_nAttr = nAttr.create("frontAxisZ", "faz", OM.MFnNumericData.kDouble, 0.0)
    nAttr.setKeyable(True)
    openPSD.addAttribute(openPSD.frontAxisZ_nAttr)

    # frontAxis
    openPSD.frontAxis_nAttr = nAttr.create("frontAxis", "fa", frontAxisX_nAttr, frontAxisY_nAttr, frontAxisZ_nAttr)
    nAttr.setDefault(0.0, 1.0, 0.0)
    openPSD.addAttribute(openPSD.frontAxis_nAttr)

    # startOff
    openPSD.startOff_uAttr = uAttr.create("startOff", "sof", OM.MFnUnitAttribute.kAngle, 0.0)
    uAttr.setMin(0.0)
    uAttr.setMax(math.pi)
    openPSD.addAttribute(openPSD.startOff_uAttr)

    # startOn
    openPSD.startOn_uAttr = uAttr.create("startOn", "son", OM.MFnUnitAttribute.kAngle, math.pi * 0.25)
    uAttr.setMin(0.0)
    uAttr.setMax(math.pi)
    openPSD.addAttribute(openPSD.startOn_uAttr)

    # endOn
    openPSD.endOn_uAttr = uAttr.create("endOn", "eon", OM.MFnUnitAttribute.kAngle, math.pi * 0.5)
    uAttr.setMin(0.0)
    uAttr.setMax(math.pi)
    openPSD.addAttribute(openPSD.endOn_uAttr)

    # endOff
    openPSD.endOff_uAttr = uAttr.create("endOff", "eof", OM.MFnUnitAttribute.kAngle, math.pi * 0.75)
    uAttr.setMin(0.0)
    uAttr.setMax(math.pi)
    openPSD.addAttribute(openPSD.endOff_uAttr)


    # targetSettings
    openPSD.targetSettings_cAttr = cAttr.create("targetSettings", "ts")
    cAttr.addChild(startOff_uAttr)
    cAttr.addChild(startOn_uAttr)
    cAttr.addChild(endOn_uAttr)
    cAttr.addChild(endOff_uAttr)
    cAttr.setArray(True)
    openPSD.addAttribute(openPSD.targetSettings_cAttr)

    # outAngle
    openPSD.outAngle_uAttr = uAttr.create("outAngle", "oa", OM.MFnUnitAttribute.kAngle, 0.0)
    uAttr.setWritable(False)
    uAttr.setStorable(False)
    openPSD.addAttribute(openPSD.outAngle_uAttr)


    # outTargetWeights
    openPSD.outTargetWeights_nAttr = nAttr.create("outTargetWeights", "otw", OM.MFnNumericData.kDouble, 0.0)
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    nAttr.setArray(True)
    nAttr.setUsesArrayDataBuilder(True)
    openPSD.addAttribute(openPSD.outTargetWeights_nAttr)

	
    # attributeAffects calls
    attributeAffects(openPSD.baseMatrix_mAttr, openPSD.outAngle_uAttr)
    attributeAffects(openPSD.driverMatrix_mAttr, openPSD.outAngle_uAttr)
    attributeAffects(openPSD.baseAxis_nAttr, openPSD.outAngle_uAttr)
    attributeAffects(openPSD.frontAxis_nAttr, openPSD.outAngle_uAttr)
	
    attributeAffects(openPSD.baseMatrix_mAttr, openPSD.outTargetWeights_nAttr)
    attributeAffects(openPSD.driverMatrix_mAttr, openPSD.outTargetWeights_nAttr)
    attributeAffects(openPSD.baseAxis_nAttr, openPSD.outTargetWeights_nAttr)
    attributeAffects(openPSD.frontAxis_nAttr, openPSD.outTargetWeights_nAttr)
    attributeAffects(openPSD.targetSettings_cAttr, openPSD.outTargetWeights_nAttr)
	

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




