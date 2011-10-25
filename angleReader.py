import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import math

pluginName = 'angleReader'
nodeId = om.MTypeId(0x101121)


class angleReader(ompx.MPxNode):
    def __init__(self):
        ompx.MPxNode.__init__(self)

    def compute(self, plug, dataBlock):
        if plug != angleReader.outAngle_uAttr and plug != angleReader.outWeights_nAttr :
            return om.kUnknownParameter


        baseMatrix_DH = om.MDataHandle()
        baseMatrix_DH = dataBlock.inputValue(angleReader.baseMatrix_mAttr)
	base_M = baseMatrix_DH.asMatrix()

        driverMatrix_DH = om.MDataHandle()
	driverMatrix_DH = dataBlock.inputValue(angleReader.driverMatrix_mAttr)
	driver_M = driverMatrix_DH.asMatrix()

	baseAxisX_DH = om.MDataHandle()
        baseAxisX_DH = data.inputValue(angleReader.baseAxisX_nAttr)
	baseAxisY_DH = om.MDataHandle()
	baseAxisY_DH = data.inputValue(angleReader.baseAxisY_nAttr)
	baseAxisZ_DH = om.MDataHandle()
	baseAxisZ_DH = data.inputValue(angleReader.baseAxisZ_nAttr)
        baseAxis_V = om.MVector(baseAxisX_DH.asDouble(), baseAxisY_DH.asDouble(), baseAxisZ_DH.asDouble())


        # frontAxisX_DH = om.MDataHandle()
	# frontAxisX_DH = data.inputValue(angleReader.frontAxisX_nAttr)
	# frontAxisY_DH = data.inputValue(angleReader.frontAxisY_nAttr)
	# frontAxisZ_DH = data.inputValue(angleReader.frontAxisZ_nAttr)
	# MVector frontAxis_V = om.MVector((frontAxisX_DH.asDouble(), frontAxisY_DH.asDouble(), frontAxisZ_DH.asDouble()))


def nodeCreator():
    return ompx.asMPxPtr(angleReader())

def nodeInit():
    nAttr = om.MFnNumericAttribute()
    mAttr = om.MFnMatrixAttribute()
    uAttr = om.MFnUnitAttribute()
    eAttr = om.MFnEnumAttribute()
    cAttr = om.MFnCompoundAttribute()

    # preStart
    angleReader.preStart_uAttr = uAttr.create("preStart", "pre", om.MFnUnitAttribute.kAngle, 0.0)
    uAttr.setMin(0.0)
    uAttr.setMax(math.pi)
    angleReader.addAttribute(angleReader.preStart_uAttr)

    # start
    angleReader.start_uAttr = uAttr.create("start", "st", om.MFnUnitAttribute.kAngle, math.pi * 0.35)
    uAttr.setMin(0.0)
    uAttr.setMax(math.pi)
    angleReader.addAttribute(angleReader.start_uAttr)

    # end
    angleReader.end_uAttr = uAttr.create("end", "eon", om.MFnUnitAttribute.kAngle, math.pi * 0.75)
    uAttr.setMin(0.0)
    uAttr.setMax(math.pi)
    angleReader.addAttribute(angleReader.end_uAttr)

    # postEnd
    angleReader.postEnd_uAttr = uAttr.create("postEnd", "eof", om.MFnUnitAttribute.kAngle, math.pi * 1.0)
    uAttr.setMin(0.0)
    uAttr.setMax(math.pi)
    angleReader.addAttribute(angleReader.postEnd_uAttr)

    # inputSettings
    angleReader.inputSettings_cAttr = cAttr.create("inputSettings", "is")
    cAttr.setArray(True)
    cAttr.addChild(angleReader.preStart_uAttr)
    cAttr.addChild(angleReader.start_uAttr)
    cAttr.addChild(angleReader.end_uAttr)
    cAttr.addChild(angleReader.postEnd_uAttr)
    angleReader.addAttribute(angleReader.inputSettings_cAttr)
    


    # baseMatrix_mAttr
    angleReader.baseMatrix_mAttr = mAttr.create("baseMatrix", "bm", om.MFnMatrixAttribute.kDouble)
    angleReader.addAttribute(angleReader.baseMatrix_mAttr)

    # driverMatrix_mAttr
    angleReader.driverMatrix_mAttr = mAttr.create("driverMatrix", "dm", om.MFnMatrixAttribute.kDouble)
    angleReader.addAttribute(angleReader.driverMatrix_mAttr)

    # baseAxisX  - this should be kDouble in C++
    angleReader.baseAxisX_nAttr = nAttr.create("baseAxisX", "bax", om.MFnNumericData.kFloat, 1.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.baseAxisX_nAttr)

    # baseAxisY
    angleReader.baseAxisY_nAttr = nAttr.create("baseAxisY", "bay", om.MFnNumericData.kFloat, 0.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.baseAxisY_nAttr)

    # baseAxisZ
    angleReader.baseAxisZ_nAttr = nAttr.create("baseAxisZ", "baz", om.MFnNumericData.kFloat, 0.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.baseAxisZ_nAttr)

    # baseAxis
    angleReader.baseAxis_nAttr = nAttr.create("baseAxis",
                                              "ba",
                                              angleReader.baseAxisX_nAttr,
                                              angleReader.baseAxisY_nAttr,
                                              angleReader.baseAxisZ_nAttr)
    nAttr.setDefault(1.0, 0.0, 0.0)
    angleReader.addAttribute(angleReader.baseAxis_nAttr)

    # frontAxisX
    angleReader.frontAxisX_nAttr = nAttr.create("frontAxisX", "fax", om.MFnNumericData.kFloat, 0.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.frontAxisX_nAttr)

    # frontAxisY
    angleReader.frontAxisY_nAttr = nAttr.create("frontAxisY", "fay", om.MFnNumericData.kFloat, 0.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.frontAxisY_nAttr)

    # frontAxisZ
    angleReader.frontAxisZ_nAttr = nAttr.create("frontAxisZ", "faz", om.MFnNumericData.kFloat, 0.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.frontAxisZ_nAttr)

    # frontAxis
    angleReader.frontAxis_nAttr = nAttr.create("frontAxis",
                                               "fa",
                                               angleReader.frontAxisX_nAttr,
                                               angleReader.frontAxisY_nAttr,
                                               angleReader.frontAxisZ_nAttr)
    nAttr.setDefault(0.0, 1.0, 0.0)
    angleReader.addAttribute(angleReader.frontAxis_nAttr)


    # outAngle
    angleReader.outAngle_uAttr = uAttr.create("outAngle", "oa", om.MFnUnitAttribute.kAngle, 0.0)
    uAttr.setWritable(False)
    uAttr.setStorable(False)
    angleReader.addAttribute(angleReader.outAngle_uAttr)


    # outWeights
    angleReader.outWeights_nAttr = nAttr.create("outWeights", "otw", om.MFnNumericData.kDouble, 0.0)
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    nAttr.setArray(True)
    nAttr.setUsesArrayDataBuilder(True)
    angleReader.addAttribute(angleReader.outWeights_nAttr)

	
    # attributeAffects calls
    angleReader.attributeAffects(angleReader.baseMatrix_mAttr, angleReader.outAngle_uAttr)
    angleReader.attributeAffects(angleReader.driverMatrix_mAttr, angleReader.outAngle_uAttr)
    angleReader.attributeAffects(angleReader.baseAxis_nAttr, angleReader.outAngle_uAttr)
    angleReader.attributeAffects(angleReader.frontAxis_nAttr, angleReader.outAngle_uAttr)
	
    angleReader.attributeAffects(angleReader.baseMatrix_mAttr, angleReader.outWeights_nAttr)
    angleReader.attributeAffects(angleReader.driverMatrix_mAttr, angleReader.outWeights_nAttr)
    angleReader.attributeAffects(angleReader.baseAxis_nAttr, angleReader.outWeights_nAttr)
    angleReader.attributeAffects(angleReader.frontAxis_nAttr, angleReader.outWeights_nAttr)
    # angleReader.attributeAffects(angleReader.inputSettings_cAttr, angleReader.outWeights_nAttr)

# initialize the plugin
def initializePlugin(mobject):
    mplugin = ompx.MFnPlugin(mobject,'Marin&Alex', '0.1', 'Any')
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


# helper function to calculate the weight
def computeWeight(angle, preStart, start, end, postEnd, negate=False):
    output = 0.0

    if negate:
        angle *= -1.0

    if start <= angle <= end:
        output = 1.0

    elif preStart <= angle < start:
        output = (angle - preStart) / (start - preStart)

    elif end < angle <= postEnd:
        output = (angle - postEnd) / (end - postEnd)


    return output




