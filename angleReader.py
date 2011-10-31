import math
import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.OpenMayaRender as omRender
import maya.OpenMayaUI as omUI

pluginName = 'angleReader'
nodeId = om.MTypeId(0x101121)


class angleReader(ompx.MPxLocatorNode):
    
    glRenderer = omRender.MHardwareRenderer.theRenderer()
    glFT = glRenderer.glFunctionTable()


    def __init__(self):
        ompx.MPxLocatorNode.__init__(self)


    def compute(self, plug, dataBlock):
        print 'computing'
        dataBlock.setClean(plug)


        # if plug != angleReader.outAngle_nAttr and plug != angleReader.outWeight_nAttr :
        #     return om.kUnknownParameter


        baseMatrix_DH = om.MDataHandle()
        baseMatrix_DH = dataBlock.inputValue(angleReader.baseMatrix_mAttr)
        base_M = baseMatrix_DH.asMatrix()

        driverMatrix_DH = om.MDataHandle()
        driverMatrix_DH = dataBlock.inputValue(angleReader.driverMatrix_mAttr)
        driver_M = driverMatrix_DH.asMatrix()

        rotateAxisX_DH = om.MDataHandle()
        rotateAxisX_DH = dataBlock.inputValue(angleReader.rotateAxisX_nAttr)
        rotateAxisY_DH = om.MDataHandle()
        rotateAxisY_DH = dataBlock.inputValue(angleReader.rotateAxisY_nAttr)
        rotateAxisZ_DH = om.MDataHandle()
        rotateAxisZ_DH = dataBlock.inputValue(angleReader.rotateAxisZ_nAttr)
        rotateAxis_V = om.MVector(rotateAxisX_DH.asFloat(), rotateAxisY_DH.asFloat(), rotateAxisZ_DH.asFloat())

#         print rotateAxis_V.x, rotateAxis_V.y, rotateAxis_V.z


        frontAxisX_DH = om.MDataHandle()
        frontAxisX_DH = dataBlock.inputValue(angleReader.frontAxisX_nAttr)
        frontAxisY_DH = om.MDataHandle()
        frontAxisY_DH = dataBlock.inputValue(angleReader.frontAxisY_nAttr)
        frontAxisZ_DH = om.MDataHandle()
        frontAxisZ_DH = dataBlock.inputValue(angleReader.frontAxisZ_nAttr)
        frontAxis_V = om.MVector(frontAxisX_DH.asFloat(), frontAxisY_DH.asFloat(), frontAxisZ_DH.asFloat())


        # compute the angle

        # first get the local axis of the matrices
        driverFront_V = frontAxis_V * driver_M
        driverFront_V.normalize()

#         print 'DriverFront_V: ', driverFront_V.x, driverFront_V.y, driverFront_V.z
        baseRotate_V = rotateAxis_V * base_M
        baseRotate_V.normalize()
        baseFront_V = frontAxis_V * base_M
        baseFront_V.normalize()

        # then calculate the third axis for the baseMatrix
        upAxis_V = baseRotate_V ^ baseFront_V

        # then make a projection from driver's frontAxis to the base rotate vector
        projected_V = driverFront_V ^ baseRotate_V
        dotProjBaseFront = projected_V * baseFront_V
        dotProjUp = projected_V * upAxis_V
        angle = math.degrees(math.atan2(dotProjBaseFront, dotProjUp))
        mAngle = om.MAngle(angle, om.MAngle.kRadians)

        outAngle_DH = om.MDataHandle()
        outAngle_DH = dataBlock.outputValue(angleReader.outAngle_nAttr)
        outAngle_DH.setMAngle(mAngle)
        outAngle_DH.setClean()

        print pluginName + ' : ' + str(angle)



    def draw( self, view, path, dispStyle, status ):
        print 'drawing'
                
        thisNode = self.thisMObject()
        plugDraw = om.MPlug(thisNode, self.draw_nAttr)
        draw = plugDraw.asInt()
        plugSegment = om.MPlug(thisNode, self.segment_nAttr)
        segment = plugSegment.asInt()
        plugPreStart = om.MPlug(thisNode, self.preStart_nAttr)
        preStart = plugPreStart.asFloat()
        plugStart = om.MPlug(thisNode, self.start_nAttr)
        start = plugStart.asFloat()
        plugEnd = om.MPlug(thisNode, self.end_nAttr)
        end = plugEnd.asFloat()
        plugPostEnd = om.MPlug(thisNode, self.postEnd_nAttr)
        postEnd = plugPostEnd.asFloat()
        plugRadius = om.MPlug(thisNode, self.radius)
        radius = plugRadius.asFloat()
        plugAngle = om.MPlug(thisNode, self.outAngle_nAttr)
        angle = plugAngle.asMAngle()
        print angle.asDegrees()


        if (draw == 0):
            return


        view.beginGL()  

        self.glFT.glPushAttrib(omRender.MGL_CURRENT_BIT | omRender.MGL_POINT_BIT | omRender.MGL_LINE_BIT)
        self.glFT.glBegin(omRender.MGL_LINE_STRIP)

        arc_angl = math.radians(preStart-postEnd)
        start_ang = math.radians(postEnd)

        theta = arc_angl/(segment-1)
        tag = math.tan(theta)
        rad = math.cos(theta)
        x = radius * math.cos(start_ang)
        y = radius * math.sin(start_ang)

        for i in range(segment):
            self.glFT.glVertex3d(x, y, 0.0)
            tx = -y
            ty = x
            x += tx*tag
            y += ty*tag
            x *= rad
            y *= rad



        self.glFT.glEnd()


        text = ("Angle : "+str(angle.asDegrees()))
        view.drawText(text,om.MPoint(0,0,0), omUI.M3dView().kLeft)

        self.glFT.glLineWidth(3)
        self.glFT.glColor3f(1,0,0)
        self.glFT.glBegin(omRender.MGL_LINES)

        x = radius * math.cos(start_ang)
        y = radius * math.sin(start_ang)

        self.glFT.glVertex3d(x*1.05, y*1.05, 0.0)
        self.glFT.glVertex3d(x*0.95, y*0.95, 0.0)

        x = radius * math.cos(math.radians(preStart))
        y = radius * math.sin(math.radians(preStart))

        self.glFT.glVertex3d(x*1.05, y*1.05, 0.0)
        self.glFT.glVertex3d(x*0.95, y*0.95, 0.0)

        x = radius * math.cos(math.radians(start))
        y = radius * math.sin(math.radians(start))

        self.glFT.glVertex3d(x*1.05, y*1.05, 0.0)
        self.glFT.glVertex3d(x*0.95, y*0.95, 0.0)

        x = radius * math.cos(math.radians(end))
        y = radius * math.sin(math.radians(end))

        self.glFT.glVertex3d(x*1.05, y*1.05, 0.0)
        self.glFT.glVertex3d(x*0.95, y*0.95, 0.0)

        self.glFT.glEnd()
        self.glFT.glLineWidth(1.0);
        self.glFT.glPopAttrib()
        view.endGL()


def isBounded( self ):
    return True
        
        
def nodeCreator():
    return ompx.asMPxPtr(angleReader())



def nodeInit():
    nAttr = om.MFnNumericAttribute()
    mAttr = om.MFnMatrixAttribute()
    uAttr = om.MFnUnitAttribute()
    eAttr = om.MFnEnumAttribute()
    cAttr = om.MFnCompoundAttribute()

    # draw
    angleReader.draw_nAttr = nAttr.create("draw", "drw", om.MFnNumericData.kBoolean, 1)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.draw_nAttr)
        
    # segment
    angleReader.segment_nAttr = nAttr.create("segment", "seg", om.MFnNumericData.kInt, 9)
    nAttr.setKeyable(True)
    nAttr.setMin(2)
    angleReader.addAttribute(angleReader.segment_nAttr)
        
    # preStart
    angleReader.preStart_nAttr = nAttr.create("preStart", "pre", om.MFnNumericData.kFloat, 0.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.preStart_nAttr)
        
    # start
    angleReader.start_nAttr = nAttr.create("start", "str", om.MFnNumericData.kFloat, 75.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.start_nAttr)
        
    # end
    angleReader.end_nAttr = nAttr.create("end", "end", om.MFnNumericData.kFloat, 100.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.end_nAttr)
        
    # postEnd
    angleReader.postEnd_nAttr = nAttr.create("postEnd", "sta", om.MFnNumericData.kFloat, 180.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute( angleReader.postEnd_nAttr )
        
    # radius
    angleReader.radius = nAttr.create("radius", "rad", om.MFnNumericData.kFloat, 2.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute( angleReader.radius )
        
    # baseMatrix_mAttr
    angleReader.baseMatrix_mAttr = mAttr.create("baseMatrix", "bm", om.MFnMatrixAttribute.kDouble)
    angleReader.addAttribute(angleReader.baseMatrix_mAttr)

    # driverMatrix_mAttr
    angleReader.driverMatrix_mAttr = mAttr.create("driverMatrix", "dm", om.MFnMatrixAttribute.kDouble)
    angleReader.addAttribute(angleReader.driverMatrix_mAttr)

    # rotateAxisX  - this should be kDouble in C++
    angleReader.rotateAxisX_nAttr = nAttr.create("rotateAxisX", "rax", om.MFnNumericData.kFloat, 1.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.rotateAxisX_nAttr)

    # rotateAxisY
    angleReader.rotateAxisY_nAttr = nAttr.create("rotateAxisY", "ray", om.MFnNumericData.kFloat, 0.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.rotateAxisY_nAttr)

    # rotateAxisZ
    angleReader.rotateAxisZ_nAttr = nAttr.create("rotateAxisZ", "raz", om.MFnNumericData.kFloat, 0.0)
    nAttr.setKeyable(True)
    angleReader.addAttribute(angleReader.rotateAxisZ_nAttr)

    # rotateAxis
    angleReader.rotateAxis_nAttr = nAttr.create("rotateAxis", "ra",
                                                angleReader.rotateAxisX_nAttr,
                                                angleReader.rotateAxisY_nAttr,
                                                angleReader.rotateAxisZ_nAttr)
    nAttr.setDefault(1.0, 0.0, 0.0)
    angleReader.addAttribute(angleReader.rotateAxis_nAttr)

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
    angleReader.frontAxis_nAttr = nAttr.create("frontAxis", "fa",
                                               angleReader.frontAxisX_nAttr,
                                               angleReader.frontAxisY_nAttr,
                                               angleReader.frontAxisZ_nAttr)
    
    nAttr.setDefault(0.0, 1.0, 0.0)
    angleReader.addAttribute(angleReader.frontAxis_nAttr)


#     # outAngle
#     angleReader.outAngle_nAttr = nAttr.create("outAngle", "oa", om.MFnNumericData.kFloat, 0.0)
#     nAttr.setWritable(False)
#     nAttr.setStorable(False)
#     angleReader.addAttribute(angleReader.outAngle_nAttr)

    # outAngle
    angleReader.outAngle_nAttr = uAttr.create("outAngle", "oa", om.MFnUnitAttribute.kAngle, 0.0)
    uAttr.setWritable(False)
    uAttr.setStorable(False)
    angleReader.addAttribute(angleReader.outAngle_nAttr)


    # outWeight
    angleReader.outWeight_nAttr = nAttr.create("outWeight", "otw", om.MFnNumericData.kFloat, 0.0)
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    angleReader.addAttribute(angleReader.outWeight_nAttr)

        
    # attributeAffects calls
    angleReader.attributeAffects(angleReader.baseMatrix_mAttr, angleReader.outAngle_nAttr)
    angleReader.attributeAffects(angleReader.driverMatrix_mAttr, angleReader.outAngle_nAttr)
    angleReader.attributeAffects(angleReader.rotateAxis_nAttr, angleReader.outAngle_nAttr)
    angleReader.attributeAffects(angleReader.frontAxis_nAttr, angleReader.outAngle_nAttr)

    angleReader.attributeAffects(angleReader.baseMatrix_mAttr, angleReader.outWeight_nAttr)
    angleReader.attributeAffects(angleReader.driverMatrix_mAttr, angleReader.outWeight_nAttr)
    angleReader.attributeAffects(angleReader.rotateAxis_nAttr, angleReader.outWeight_nAttr)
    angleReader.attributeAffects(angleReader.frontAxis_nAttr, angleReader.outWeight_nAttr)



# initialize the plugin
def initializePlugin(mobject):
    mplugin = ompx.MFnPlugin(mobject,'Marin&Alex', '0.1', 'Any')
    try:
        mplugin.registerNode(pluginName, nodeId, nodeCreator ,nodeInit,ompx.MPxNode.kLocatorNode)

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

