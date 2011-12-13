#ifndef _ANGLEREADER_H_
#define _ANGLEREADER_H_

#include <maya/MFnPlugin.h>
#include <maya/MGlobal.h>

#include <maya/MPxNode.h>

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnCompoundAttribute.h>

#include <maya/M3dView.h>

#include <maya/MVector.h>
#include <maya/MMatrix.h>
#include <maya/MAngle.h>

// CHECK_STAT Macro
#ifndef CHECK_STAT
#define CHECK_STAT(STAT, MSG)\
if(!STAT){\
    MGlobal::displayError(MString(MSG) + " --- " + STAT.errorString());\
}
#endif

class angleReader : public MPxNode {
public:
    // Methods
/*     angleReader(); */
/*     virtual ~angleReader(); */

    virtual MStatus compute(const MPlug& plug,
			    MDataBlock& data);

    virtual void draw(M3dView& view,
		      const MDagPath& path,
		      M3dView::DisplayStyle dispStyle,
		      M3dView::DisplayStatus displayStat);

    static double computeWeight(double& angle,
				double& preStart,
				double& start,
				bool negate);

    virtual bool isBounded() const;


    static void *creator();
    static MStatus initialize();
    static const MTypeId nodeId;
    static const MString nodeName;

    //Data members
    static MObject aDraw_nAttr;
    static MObject aText_eAttr;
    static MObject aRadius_nAttr;
    static MObject aSegment_nAttr;
    static MObject aNegate_nAttr;
    static MObject aPreStart_nAttr;
    static MObject aStart_nAttr;
    static MObject aEnd_nAttr;
    static MObject aPostEnd_nAttr;

    static MObject aBaseMatrix_mAttr;
    static MObject aDriverMatrix_mAttr;

    static MObject aRotateAxisX_nAttr;
    static MObject aRotateAxisY_nAttr;
    static MObject aRotateAxisZ_nAttr;
    static MObject aRotateAxis_nAttr;

    static MObject aFrontAxisX_nAttr;
    static MObject aFrontAxisY_nAttr;
    static MObject aFrontAxisZ_nAttr;
    static MObject aFrontAxis_nAttr;

    static MObject aOutAngle_uAttr;
    static MObject aOutWeight_nAttr;


#endif
    
    
