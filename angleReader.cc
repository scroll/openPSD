/*
Description:
    Maya C++ plugin for creating an angleReader node.
    The angleReader node can be used to drive corrective blendshapes based on
    rotation between two transforms. Only one axis will be read by the angleReader,
    which can be specified in the angleReader's shape attributes.   

Authors:
    Marin Petrov (www.scroll-lock.eu)
    Alexander Tyemirov (www.tyemirov.blogspot.com)

*/

#include "angleReader.h"


MObject angleReader::draw_nAttr;
MObject angleReader::text_eAttr;
MObject angleReader::radius_nAttr;
MObject angleReader::segment_nAttr;
MObject angleReader::negate_nAttr;
MObject angleReader::preStart_uAttr;
MObject angleReader::start_uAttr;
MObject angleReader::end_uAttr;
MObject angleReader::postEnd_uAttr;
MObject angleReader::baseMatrix_mAttr;
MObject angleReader::driverMatrix_mAttr;
MObject angleReader::rotateAxisX_nAttr;
MObject angleReader::rotateAxisY_nAttr;
MObject angleReader::rotateAxisZ_nAttr;
MObject angleReader::rotateAxis_nAttr;
MObject angleReader::frontAxisX_nAttr;
MObject angleReader::frontAxisY_nAttr;
MObject angleReader::frontAxisZ_nAttr;
MObject angleReader::frontAxis_nAttr;
MObject angleReader::outAngle_uAttr;
MObject angleReader::outWeight_nAttr;

MString angleReader::nodeName("angleReader");
MTypeId angleReader::nodeId(0x101121);

// // constructor
angleReader::angleReader() {}

// // destructor
angleReader::~angleReader() {}

// creator
void* angleReader::creator(){
    return new angleReader();
}


// initialize 
MStatus angleReader::initialize() {

    // Function sets
    MFnNumericAttribute nAttr;
    MFnMatrixAttribute mAttr;
    MFnCompoundAttribute cAttr;
    MFnTypedAttribute tAttr;
    MFnUnitAttribute uAttr;
    MFnEnumAttribute eAttr;
    MStatus stat;

    // create Attributes

    // draw
    draw_nAttr = nAttr.create("draw", "drw", MFnNumericData::kBoolean);
    CHECK_MSTATUS(nAttr.setKeyable(true));
    CHECK_MSTATUS(nAttr.setDefault(true));

    // text
    text_eAttr = eAttr.create("text", "txt", 0, &stat);
    CHECK_MSTATUS(eAttr.addField("weight", 0));		
    CHECK_MSTATUS(eAttr.addField("angle", 1));		
    CHECK_MSTATUS(eAttr.addField("none", 2));		
    CHECK_MSTATUS(eAttr.setKeyable(true));

    // radius
    radius_nAttr = nAttr.create("radius", "rad", MFnNumericData::kFloat, 2.0);
    CHECK_MSTATUS(nAttr.setKeyable(true));
        
    // segment
    segment_nAttr = nAttr.create("segment", "seg", MFnNumericData::kInt, 9);
    CHECK_MSTATUS(nAttr.setKeyable(true));
    CHECK_MSTATUS(nAttr.setMin(2));

    // negate
    negate_nAttr = nAttr.create("negate", "neg", MFnNumericData::kBoolean, 0);
    CHECK_MSTATUS(nAttr.setKeyable(true));

    // preStart
    preStart_uAttr = uAttr.create("preStart", "pre", MFnUnitAttribute::kAngle, 0.0);
    CHECK_MSTATUS(uAttr.setKeyable(true));
        
    // start
    start_uAttr = uAttr.create("start", "str", MFnUnitAttribute::kAngle, 0.25 * M_PI);
    CHECK_MSTATUS(uAttr.setKeyable(true));

    // end
    end_uAttr = uAttr.create("end", "end", MFnUnitAttribute::kAngle, 0.5 * M_PI);
    CHECK_MSTATUS(uAttr.setKeyable(true));
        
    // postEnd
    postEnd_uAttr = uAttr.create("postEnd", "sta", MFnUnitAttribute::kAngle, 0.75 * M_PI);
    CHECK_MSTATUS(uAttr.setKeyable(true));
        
    // baseMatrix_mAttr
    baseMatrix_mAttr = mAttr.create("baseMatrix", "bm", MFnMatrixAttribute::kDouble);

    // driverMatrix_mAttr
    driverMatrix_mAttr = mAttr.create("driverMatrix", "dm", MFnMatrixAttribute::kDouble);

    // rotateAxisX  
    rotateAxisX_nAttr = nAttr.create("rotateAxisX", "rax", MFnNumericData::kDouble, 1.0);
    CHECK_MSTATUS(nAttr.setKeyable(true));

    // rotateAxisY
    rotateAxisY_nAttr = nAttr.create("rotateAxisY", "ray", MFnNumericData::kDouble, 1.0);
    CHECK_MSTATUS(nAttr.setKeyable(true));

    // rotateAxisZ
    rotateAxisZ_nAttr = nAttr.create("rotateAxisZ", "raz", MFnNumericData::kDouble, 1.0);
    CHECK_MSTATUS(nAttr.setKeyable(true));

    // rotateAxis
    rotateAxis_nAttr = nAttr.create("rotateAxis", "ra",
                                    rotateAxisX_nAttr,
                                    rotateAxisY_nAttr,
                                    rotateAxisZ_nAttr);

    CHECK_MSTATUS(nAttr.setDefault(1.0, 0.0, 0.0));

    // frontAxisX
    frontAxisX_nAttr = nAttr.create("frontAxisX", "fax", MFnNumericData::kDouble, 1.0);
    CHECK_MSTATUS(nAttr.setKeyable(true));

    // frontAxisY
    frontAxisY_nAttr = nAttr.create("frontAxisY", "fay", MFnNumericData::kDouble, 1.0);
    CHECK_MSTATUS(nAttr.setKeyable(true));

    // frontAxisZ
    frontAxisZ_nAttr = nAttr.create("frontAxisZ", "faz", MFnNumericData::kDouble, 1.0);
    CHECK_MSTATUS(nAttr.setKeyable(true));

    // frontAxis
    frontAxis_nAttr = nAttr.create("frontAxis", "fa",
                                    frontAxisX_nAttr,
                                    frontAxisY_nAttr,
                                    frontAxisZ_nAttr);

    CHECK_MSTATUS(nAttr.setDefault(0.0, 1.0, 0.0));


    // outAngle
    outAngle_uAttr = uAttr.create("outAngle", "oa", MFnUnitAttribute::kAngle, 0.0);
    CHECK_MSTATUS(uAttr.setWritable(false));
    CHECK_MSTATUS(uAttr.setStorable(false));

    // outWeight
    outWeight_nAttr = nAttr.create("outWeight", "otw", MFnNumericData::kDouble, 0.0);
    CHECK_MSTATUS(nAttr.setWritable(false));
    CHECK_MSTATUS(nAttr.setStorable(false));

    // addAttributes
    CHECK_MSTATUS(addAttribute(draw_nAttr));
    CHECK_MSTATUS(addAttribute(text_eAttr));
    CHECK_MSTATUS(addAttribute(radius_nAttr));
    CHECK_MSTATUS(addAttribute(segment_nAttr));
    CHECK_MSTATUS(addAttribute(negate_nAttr));
    CHECK_MSTATUS(addAttribute(preStart_uAttr));
    CHECK_MSTATUS(addAttribute(start_uAttr));
    CHECK_MSTATUS(addAttribute(end_uAttr));
    CHECK_MSTATUS(addAttribute(postEnd_uAttr));
    CHECK_MSTATUS(addAttribute(baseMatrix_mAttr));
    CHECK_MSTATUS(addAttribute(driverMatrix_mAttr));
    CHECK_MSTATUS(addAttribute(rotateAxis_nAttr));
    CHECK_MSTATUS(addAttribute(frontAxis_nAttr));
    CHECK_MSTATUS(addAttribute(outAngle_uAttr));
    CHECK_MSTATUS(addAttribute(outWeight_nAttr));
        
    // attributeAffects calls
    CHECK_MSTATUS(attributeAffects(baseMatrix_mAttr, outAngle_uAttr));
    CHECK_MSTATUS(attributeAffects(driverMatrix_mAttr, outAngle_uAttr));
    CHECK_MSTATUS(attributeAffects(rotateAxis_nAttr, outAngle_uAttr));
    CHECK_MSTATUS(attributeAffects(frontAxis_nAttr, outAngle_uAttr));
    CHECK_MSTATUS(attributeAffects(preStart_uAttr, outAngle_uAttr));
    CHECK_MSTATUS(attributeAffects(start_uAttr, outAngle_uAttr));
    CHECK_MSTATUS(attributeAffects(end_uAttr, outAngle_uAttr));
    CHECK_MSTATUS(attributeAffects(postEnd_uAttr, outAngle_uAttr));

    CHECK_MSTATUS(attributeAffects(baseMatrix_mAttr, outWeight_nAttr));
    CHECK_MSTATUS(attributeAffects(driverMatrix_mAttr, outWeight_nAttr));
    CHECK_MSTATUS(attributeAffects(rotateAxis_nAttr, outWeight_nAttr));
    CHECK_MSTATUS(attributeAffects(frontAxis_nAttr, outWeight_nAttr));
    CHECK_MSTATUS(attributeAffects(preStart_uAttr, outWeight_nAttr));
    CHECK_MSTATUS(attributeAffects(start_uAttr, outWeight_nAttr));
    CHECK_MSTATUS(attributeAffects(end_uAttr, outWeight_nAttr));
    CHECK_MSTATUS(attributeAffects(postEnd_uAttr, outWeight_nAttr));

    return MS::kSuccess;

}


// compute
MStatus angleReader::compute(const MPlug& plug, MDataBlock& data){

    MStatus stat;

    if (plug != outAngle_uAttr && plug != outWeight_nAttr){
        return MS::kUnknownParameter;
    }

	// get the values of the input attributes
    // base_M
	MDataHandle baseMatrix_DH = data.inputValue(baseMatrix_mAttr, &stat);
	CHECK_MSTATUS(stat);
	MMatrix base_M = baseMatrix_DH.asMatrix();

    // driver_M
    MDataHandle driverMatrix_DH = data.inputValue(driverMatrix_mAttr, &stat);
	CHECK_MSTATUS(stat);
	MMatrix driver_M = driverMatrix_DH.asMatrix();

    // rotateAxis_V
    MDataHandle rotateAxisX_DH = data.inputValue(rotateAxisX_nAttr, &stat);
	CHECK_MSTATUS(stat);
    MDataHandle rotateAxisY_DH = data.inputValue(rotateAxisY_nAttr, &stat);
	CHECK_MSTATUS(stat);
    MDataHandle rotateAxisZ_DH = data.inputValue(rotateAxisZ_nAttr, &stat);
	CHECK_MSTATUS(stat);
    MVector rotateAxis_V(rotateAxisX_DH.asDouble(), rotateAxisY_DH.asDouble(), rotateAxisZ_DH.asDouble());

    // frontAxis_V
    MDataHandle frontAxisX_DH = data.inputValue(frontAxisX_nAttr, &stat);
	CHECK_MSTATUS(stat);
    MDataHandle frontAxisY_DH = data.inputValue(frontAxisY_nAttr, &stat);
	CHECK_MSTATUS(stat);
    MDataHandle frontAxisZ_DH = data.inputValue(frontAxisZ_nAttr, &stat);
	CHECK_MSTATUS(stat);
    MVector frontAxis_V(frontAxisX_DH.asDouble(), frontAxisY_DH.asDouble(), frontAxisZ_DH.asDouble());

    // preStart
    MDataHandle preStart_DH = data.inputValue(preStart_uAttr, &stat);
	CHECK_MSTATUS(stat);
    double preStart_d = preStart_DH.asAngle().asRadians();

    // start
    MDataHandle start_DH = data.inputValue(start_uAttr, &stat);
	CHECK_MSTATUS(stat);
    double start_d = start_DH.asAngle().asRadians();

    // end
    MDataHandle end_DH = data.inputValue(end_uAttr, &stat);
	CHECK_MSTATUS(stat);
    double end_d = end_DH.asAngle().asRadians();

    // postEnd
    MDataHandle postEnd_DH = data.inputValue(postEnd_uAttr, &stat);
	CHECK_MSTATUS(stat);
    double postEnd_d = postEnd_DH.asAngle().asRadians();

    // negate
    MDataHandle negate_DH = data.inputValue(negate_nAttr, &stat);
	CHECK_MSTATUS(stat);
    bool negate_b = negate_DH.asBool();

    // compute the angle

    // first get the local axis of the matrices
    MVector driverFront_V = frontAxis_V * driver_M;
    driverFront_V.normalize();
    MVector baseRotate_V = rotateAxis_V * base_M;
    baseRotate_V.normalize();
    MVector baseFront_V = frontAxis_V * base_M;
    baseFront_V.normalize();

    // then calculate the third axis for the baseMatrix
    MVector upAxis_V = baseFront_V ^ baseRotate_V;

    // then make a projection from driver's frontAxis to the base rotate vector
    MVector projected_V = driverFront_V ^ baseRotate_V;
    double dotProjBaseFront_d = projected_V * baseFront_V;
    double dotProjUp_d = projected_V * upAxis_V;

    // compute the angle
    double angle_d = atan2(dotProjBaseFront_d, dotProjUp_d);
	MAngle outAngle_A(angle_d, MAngle::kRadians);
	MDataHandle outAngle_DH = data.outputValue(outAngle_uAttr, &stat);
	CHECK_MSTATUS(stat);
	outAngle_DH.setMAngle(outAngle_A);
	outAngle_DH.setClean();

    // compute the weight
    MDataHandle outWeight_DH = data.outputValue(outWeight_nAttr, &stat);
	CHECK_MSTATUS(stat);
    double weight_d = computeWeight(angle_d, preStart_d, start_d, end_d, postEnd_d, negate_b);
    outWeight_DH.setDouble(weight_d);
    outWeight_DH.setClean();

	// // return
	return MS::kSuccess;

}



void angleReader::draw(M3dView& view,
                       const MDagPath& path,
                       M3dView::DisplayStyle dispStyle,
                       M3dView::DisplayStatus displayStat){


	MObject thisNode = thisMObject();
    MPlug drawPlug(thisNode, draw_nAttr);
    bool draw_b = drawPlug.asBool();
    MPlug textPlug(thisNode, text_eAttr);
    double text_d = textPlug.asDouble();
    MPlug segmentPlug(thisNode, segment_nAttr);
    double segment_d = segmentPlug.asDouble();
    MPlug preStartPlug(thisNode, preStart_uAttr);
    double preStart_d = preStartPlug.asMAngle().asRadians();
    MPlug startPlug(thisNode, start_uAttr);
    double start_d = startPlug.asMAngle().asRadians();
    MPlug endPlug(thisNode, end_uAttr);
    double end_d = endPlug.asMAngle().asRadians();
    MPlug postEndPlug(thisNode, postEnd_uAttr);
    double postEnd_d = postEndPlug.asMAngle().asRadians();
    MPlug radiusPlug(thisNode, radius_nAttr);
    double radius_d = radiusPlug.asDouble();
    MPlug anglePlug(thisNode, outAngle_uAttr);
    MAngle angle_A = anglePlug.asMAngle();
    MPlug weightPlug(thisNode, outWeight_nAttr);
    double weight_d = weightPlug.asDouble();
    MPlug rotateAxisXPlug(thisNode, rotateAxisX_nAttr);
    double rotateAxisX_d = rotateAxisXPlug.asDouble();
    MPlug rotateAxisYPlug(thisNode, rotateAxisY_nAttr);
    double rotateAxisY_d = rotateAxisYPlug.asDouble();
    MPlug rotateAxisZPlug(thisNode, rotateAxisZ_nAttr);
    double rotateAxisZ_d = rotateAxisZPlug.asDouble();
    MPlug frontAxisXPlug(thisNode, frontAxisX_nAttr);
    double frontAxisX_d = frontAxisXPlug.asDouble();
    MPlug frontAxisYPlug(thisNode, frontAxisY_nAttr);
    double frontAxisY_d = frontAxisYPlug.asDouble();
    MPlug frontAxisZPlug(thisNode, frontAxisZ_nAttr);
    double frontAxisZ_d = frontAxisZPlug.asDouble();
    MPlug negatePlug(thisNode, negate_nAttr);
    bool negate_b = negatePlug.asBool();

    double flip = 1;
    MVector rotate_V;
    if (negate_b == true){
        flip = -1;
    }

    if (rotateAxisX_d == 1.0){
        rotate_V = MVector(90.0*flip, 90.0*flip, 0.0);
    }
    else if (rotateAxisY_d == 1.0){
        rotate_V = MVector(-90.0*flip, 0.0, 0.0);
    }
    else if (rotateAxisZ_d == 1.0){
        rotate_V = MVector(0.0, 0.0, 90.0*flip);
    }
    else{
        rotate_V = MVector(0.0, 0.0, 0.0);
    }


    if (draw_b == 0){
        return;
    }

    view.beginGL();  
    glPushMatrix();
    glRotatef(rotate_V[0], 1.0, 0.0, 0.0);
    glRotatef(rotate_V[1], 0.0, 1.0, 0.0);
    glRotatef(rotate_V[2], 0.0, 0.0, 1.0);

    glPushAttrib(GL_CURRENT_BIT | GL_POINT_BIT | GL_LINE_BIT);
    glBegin(GL_LINE_STRIP);

    double arcAng_d = preStart_d - postEnd_d;
    double startAng_d = postEnd_d;

    double theta_d = arcAng_d / (segment_d - 1);
    double tan_d = tan(theta_d);
    double rad_d = cos(theta_d);
    double x, y, tx, ty;
    x = radius_d * cos(startAng_d);
    y = radius_d * sin(startAng_d);

	for(unsigned int ii = 0; ii < segment_d; ++ii){
        glVertex3d(x, y, 0.0);
        tx = -y;
        ty = x;
        x += tx*tan_d;
        y += ty*tan_d;
        x *= rad_d;
        y *= rad_d;
    }

    glEnd();


    if (text_d == 0){
        MString txt("Weight : ");
        txt += weight_d;
        view.drawText(txt, MPoint(0,0,0), M3dView().kLeft);
    }
    else if (text_d == 1){
        MString txt("Angle : ");
        txt += angle_A.asDegrees();
        view.drawText(txt, MPoint(0,0,0), M3dView().kLeft);
    }


    glLineWidth(3);
    glColor3f(1,0,0);
    glBegin(GL_LINES);

    x = radius_d * cos(startAng_d);
    y = radius_d * sin(startAng_d);

    glVertex3d(x*1.06, y*1.06, 0.0);
    glVertex3d(x*0.94, y*0.94, 0.0);

    x = radius_d * cos(preStart_d);
    y = radius_d * sin(preStart_d);

    glVertex3d(x*1.06, y*1.06, 0.0);
    glVertex3d(x*0.94, y*0.94, 0.0);

    x = radius_d * cos(start_d);
    y = radius_d * sin(start_d);

    glVertex3d(x*1.04, y*1.04, 0.0);
    glVertex3d(x*0.96, y*0.96, 0.0);

    x = radius_d * cos(end_d);
    y = radius_d * sin(end_d);

    glVertex3d(x*1.04, y*1.04, 0.0);
    glVertex3d(x*0.96, y*0.96, 0.0);

    glEnd();
    glLineWidth(1.0);
    glPopAttrib();
    glPopMatrix();
    view.endGL();
}

bool angleReader::isBounded() const{

    return false;
}

        

MStatus initializePlugin( MObject obj ){

	MFnPlugin plugin(obj, "Marin Petrov & Alex Tyemirov", "1.0", "Any");

	CHECK_MSTATUS(plugin.registerNode(angleReader::nodeName, angleReader::nodeId, 
                                      &angleReader::creator, &angleReader::initialize,
                                      MPxNode::kLocatorNode));

	return MS::kSuccess;
}

MStatus uninitializePlugin( MObject obj){

	MFnPlugin plugin(obj);

	CHECK_MSTATUS(plugin.deregisterNode( angleReader::nodeId));
	return MS::kSuccess;
}


double angleReader::computeWeight(double& angle,
                                  double& preStart,
                                  double& start,
                                  double& end,
                                  double& postEnd,
                                  bool negate) {

    double output = 0.0;

    if (negate){
        angle *= -1.0;
    }

    if (start <= angle && angle <= end){
        output = 1.0;
    }

    else if (preStart <= angle && angle < start){
        output = (angle - preStart) / (start - preStart);
    }

    else if (end < angle && angle <= postEnd){
        output = (angle - postEnd) / (end - postEnd);
    }
    
    return output;
}
