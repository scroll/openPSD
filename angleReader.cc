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

const MString angleReader::nodeName("angleReader");
const MTypeId angleReader::nodeId(0x101121)


// // constructor
// angleReader::angleReader() {}

// // destructor
// angleReader::~angleReader() {}

// creator
void* angleReader::creator(){
    return new angleReader();
}

// initialize 
MStatus angleReader::initialize(){

}

// compute
MStatus angleReader::compute(const MPlug& plug, MDataBlock& data){

}



MStatus angleReader::draw(M3dView& view,
                          const MDagPath& path,
                          M3dView::DisplayStyle dispStyle,
                          M3dView::DisplayStatus displayStat){
}

bool angleReader::isBounded() const{
    return true;
}
        
        
void* angleReader:: nodeCreator(){
    return new angleReader();
}

MStatus initializePlugin( MObject obj )
{
	MStatus stat;
	MFnPlugin plugin(obj, "Marin Petrov & Alex Tyemirov", "1.0", "Any");

	stat = plugin.registerNode(angleReader::nodeName, angleReader::nodeId, 
                               &angleReader::creator, &angleReader::initialize,
                               MPxNode::kDependNode );

    CHECK_STAT(stat, "Could not register 'angleReader' plugin")
	return stat;
}

MStatus uninitializePlugin( MObject obj)
{
	MStatus stat;
	MFnPlugin plugin(obj);

	stat = plugin.deregisterNode( angleReader::nodeId );
    CHECK_STAT(stat, "Could not deregister 'angleReader' plugin")
    return stat;
}


double angleReader::computeWeight(double& angle,
                                  double& preStart,
                                  double& start,
                                  bool negate){
    return 1.0;
}
