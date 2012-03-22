'''
Description:
    This script is used to install an angleReader node based on selection.
    The first selected item will be used as base and the second as driver.

Arguments:
    rotateAxis(optional = [1,0,0]) - The axis that will be read by the angleReader.
    frontAxis(optional = [0,1,0]) - The front axis that will be used by the angleReader.

Output:
    Tuple (angleReaderTransform, angleReaderShape)

Authors:
    Marin Petrov
    www.scroll-lock.eu
'''


# imports
import maya.cmds as mc

# load plugin 
if not mc.pluginInfo('angleReader', q=True,  loaded=True):
    mc.loadPlugin('angleReader')



def installAngleReader(rotateAxis=[1,0,0], frontAxis=[0,1,0]):
    sel = mc.ls(sl=True)
    if len(sel) != 2:
        raise RuntimeError, 'Please select 2 transforms as base and driver in order to install angleReader'

    base, driver = sel

    # create the angleReader node
    readerShape = mc.createNode('angleReader', n=base+'ReaderShape')
    reader = mc.listRelatives(readerShape, p=True)
    mc.rename(reader, base+'Reader')
    print reader

    # create two transforms that will be used as input for the reader's matrices
    baseGrp = mc.createNode('transform', n=base+'ReaderGrp')
    driverGrp = mc.createNode('transform', n=driver+'ReaderGrp')

    # snap the reader to the driver's position and parent it to the base
    driverPos = mc.xform(driver, m=True, ws=True, q=True)
    mc.xform(reader, m=driverPos)
    mc.parent(reader, base)

    # snap the groups to the driver's position
    mc.xform(baseGrp, m=driverPos)
    mc.parent(baseGrp, base)
    mc.xform(driverGrp, m=driverPos)
    mc.parent(driverGrp, driver)

    # connect the base and driver to the angleReader's matrix attributes
    mc.connectAttr('%s.worldMatrix[0]'%baseGrp, '%s.baseMatrix'%readerShape)
    mc.connectAttr('%s.worldMatrix[0]'%driverGrp, '%s.driverMatrix'%readerShape)
    
    # set the rotate and front axis
    for axis, value in zip(['X', 'Y', 'Z'], rotateAxis):
        mc.setAttr('%s.rotateAxis%s' %(readerShape, axis), value)
            
    for axis, value in zip(['X', 'Y', 'Z'], frontAxis):
        mc.setAttr('%s.frontAxis%s' %(readerShape, axis), value)

    return (reader, readerShape)
    

    
