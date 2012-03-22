#ifndef _ANGLEREADER_H_
#define _ANGLEREADER_H_

#include <maya/MFnPlugin.h>
#include <maya/MGlobal.h>

#include <maya/MPxLocatorNode.h>
#include <maya/MBoundingBox.h>

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnCompoundAttribute.h>

#include <maya/M3dView.h>

#include <maya/MString.h> 
#include <maya/MVector.h>
#include <maya/MMatrix.h>
#include <maya/MAngle.h>

#include <maya/MTypes.h>
#include <maya/MTypeId.h> 
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>



class angleReader : public MPxLocatorNode {
public:
    // Methods
    angleReader();
    virtual ~angleReader();

    virtual MStatus compute(const MPlug& plug,
			    MDataBlock& data);

    virtual void draw(M3dView& view,
		      const MDagPath& path,
		      M3dView::DisplayStyle dispStyle,
		      M3dView::DisplayStatus displayStat);


    virtual bool isBounded() const;

    static void *creator();
    static MTypeId nodeId;
    static MString nodeName;
    static MStatus initialize();

    //Data members
    static MObject draw_nAttr;
    static MObject text_eAttr;
    static MObject radius_nAttr;
    static MObject segment_nAttr;
    static MObject negate_nAttr;
    static MObject preStart_uAttr;
    static MObject start_uAttr;
    static MObject end_uAttr;
    static MObject postEnd_uAttr;

    static MObject baseMatrix_mAttr;
    static MObject driverMatrix_mAttr;

    static MObject rotateAxisX_nAttr;
    static MObject rotateAxisY_nAttr;
    static MObject rotateAxisZ_nAttr;
    static MObject rotateAxis_nAttr;

    static MObject frontAxisX_nAttr;
    static MObject frontAxisY_nAttr;
    static MObject frontAxisZ_nAttr;
    static MObject frontAxis_nAttr;

    static MObject outAngle_uAttr;
    static MObject outWeight_nAttr;

private:    
    static double computeWeight(double& angle,
				double& preStart,
				double& start,
				double& end,
				double& postEnd,
				bool negate);

};


#endif
    
    
